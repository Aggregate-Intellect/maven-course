import os
import shutil
from typing import Any, Dict, List, Optional, TypedDict

import dotenv
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langgraph.graph import END, StateGraph
from tavily import TavilyClient

dotenv.load_dotenv()


class AgentState(TypedDict, total=False):
    """State definition for our agentic RAG system."""

    question: str  # User's current question
    arxiv_results: Optional[List[Document]]  # Results from ArXiv papers (if any)
    web_results: Optional[List[Dict]]  # Results from web search (if any)
    answer: str  # Final synthesized answer
    conversation_history: str  # Previous Q&A for context
    memory: Any  # ConversationBufferMemory instance
    arxiv_processor: Any  # Instance of ArXivProcessor
    web_searcher: Any  # Instance of WebSearcher


router_prompt = ChatPromptTemplate.from_template(
    """
You are a highly specialized research assistant with access to two information sources:
1. A collection of ArXiv research papers
2. A web search tool

Your task is to determine which source would be better to answer the user's question.
FIRST try to use ArXiv papers for scientific and academic questions.
ONLY use web search if:
- The question requires very recent information not likely in research papers
- The question is about general knowledge, news, or non-academic topics
- The question asks for information beyond what academic papers would contain

Consider the conversation history for context.

Question: {question}
Conversation History: {conversation_history}

Respond with ONLY ONE of these two options:
"arxiv" - if the question should be answered using research papers
"web" - if the question requires web search

Your decision:
"""
)


def router_node(state: AgentState) -> Dict[str, str]:
    """
    Determines whether to use ArXiv papers or web search based on the question.
    """
    # Use a lighter model for routing decisions
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Create a chain that outputs just the decision text
    chain = router_prompt | llm

    # Invoke the chain with our question and history
    # Get the content of the AIMessage object instead of directly calling strip()
    decision = (
        chain.invoke(
            {
                "question": state["question"],
                "conversation_history": state["conversation_history"],
            }
        )
        .content.strip()
        .lower()
    )

    print(f"Router decision: {decision}")
    return {"next": "web_search"} if "web" in decision else {"next": "arxiv_retrieval"}


def arxiv_retrieval_node(state: AgentState) -> Dict[str, Any]:
    """
    Retrieves relevant information from ArXiv papers based on the question.
    """
    relevant_docs = state["arxiv_processor"].retrieve(
        question=state["question"], confidence_threshold=0.5  # Adjusted threshold for better recall
    )
    return {"arxiv_results": relevant_docs}


def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    Searches the web for information using the Tavily API.
    """
    academic_domains = ["arxiv.org", "scholar.google.com", "researchgate.net", "edu"]
    results = state["web_searcher"].search(
        query=state["question"],
        max_results=5,
        include_domains=academic_domains,
    )
    return {"web_results": results}


def synthesize_answer_node(state: AgentState) -> Dict[str, Any]:
    """
    Synthesizes a comprehensive answer from retrieved information.
    """
    # Determine which source to use for synthesis
    if state["arxiv_results"] and len(state["arxiv_results"]) > 0:
        # Using ArXiv research papers
        sources = "\n\n".join(
            [
                f"--- Document: {d.metadata.get('source', 'Unknown')} (Page {d.metadata.get('page', 'Unknown')}) ---\n{d.page_content}"
                for d in state["arxiv_results"]
            ]
        )

        prompt_template = """
        You are a knowledgeable research assistant providing accurate information based on scientific papers.

        Question: {question}

        Here are relevant extracts from ArXiv research papers:
        {sources}

        Conversation History:
        {conversation_history}

        Instructions:
        1. Synthesize a comprehensive answer using ONLY the information provided above.
        2. If the papers don't contain sufficient information to answer the question completely, acknowledge the limitations.
        3. Cite specific paper sections using (Author et al., Page X) format.
        4. DO NOT make up information not present in the sources.
        5. If you absolutely cannot answer the question from the provided information, say so clearly.

        Your answer:
        """
    else:
        # Using web search results
        sources = "\n\n".join(
            [
                f"--- Source {i+1}: {res['title']} ---\n{res['content']}"
                for i, res in enumerate(state.get("web_results") or [])
            ]
        )

        prompt_template = """
        You are a knowledgeable research assistant providing accurate information based on web search results.

        Question: {question}

        Here are relevant web search results:
        {sources}

        Conversation History:
        {conversation_history}

        Instructions:
        1. Synthesize a comprehensive answer using ONLY the information provided above.
        2. Cite sources using [1], [2], etc. corresponding to the source numbers above.
        3. If the search results don't contain sufficient information, acknowledge the limitations.
        4. DO NOT make up information not present in the sources.
        5. Include only facts supported by the sources.

        Your answer:
        """

    # Create the prompt
    synthesis_prompt = ChatPromptTemplate.from_template(prompt_template)

    # Use a more capable model for synthesis
    llm = ChatOpenAI(model="gpt-4o")
    chain = synthesis_prompt | llm | StrOutputParser()
    response = chain.invoke(
        {
            "question": state["question"],
            "sources": sources,
            "conversation_history": state["conversation_history"],
        }
    )
    if state.get("web_results") and not state.get("arxiv_results"):
        answer_content = response

        # Add URL references at the end
        url_citations = "\n\nSources:\n" + "\n".join(
            [f"[{i+1}] {res['url']}" for i, res in enumerate(state["web_results"])]
        )

        answer_content += url_citations
    else:
        answer_content = response

    return {"answer": answer_content}


def update_memory_node(state: AgentState) -> Dict[str, Any]:
    """
    Updates the conversation memory with the current Q&A pair.
    """
    memory_instance = state.get("memory")
    if not memory_instance:
        memory_instance = ConversationBufferMemory(return_messages=False, output_key="answer", input_key="question")
    memory_instance.save_context({"question": state["question"]}, {"answer": state["answer"]})
    updated_history = memory_instance.load_memory_variables({}).get("history", "")
    return {"conversation_history": updated_history, "memory": memory_instance}


class ArXivProcessor:
    """
    Handles processing ArXiv PDFs for retrieval-augmented generation.
    """

    def __init__(self) -> None:
        """
        Initialize the processor with document-aware chunking strategies.
        """
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Section"),  # Main sections
                ("##", "Subsection"),  # Subsections
                ("###", "Subsubsection"),  # Sub-subsections
            ]
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )
        self.vector_store = None

    def load_and_process(self, pdf_urls: List[str], force_recreate: bool = False) -> None:
        """
        Process ArXiv PDFs with document-aware chunking.
        If a local vector store exists and force_recreate is False, load it from storage.
        """
        if os.path.exists("./arxiv_db") and not force_recreate:
            print("Loading existing vector store from ./arxiv_db")
            self.vector_store = Chroma(persist_directory="./arxiv_db", embedding_function=OpenAIEmbeddings())
            return

        if force_recreate and os.path.exists("./arxiv_db"):
            print("Force recreating vector store: deleting existing store")
            shutil.rmtree("./arxiv_db")

        all_chunks = []
        for url in pdf_urls:
            print(f"Loading PDF from {url}")
            loader = PyPDFLoader(url)
            pages = loader.load()
            for page in pages:
                page_text = f"# {page.metadata['source']}\n## Page {page.metadata['page']}\n{page.page_content}"
                header_chunks = self.header_splitter.split_text(page_text)
                small_chunks = self.text_splitter.split_documents(header_chunks)
                all_chunks.extend(small_chunks)

        print(f"Created {len(all_chunks)} chunks from {len(pdf_urls)} PDFs")
        self.vector_store = Chroma.from_documents(
            documents=all_chunks, embedding=OpenAIEmbeddings(), persist_directory="./arxiv_db"
        )

    def retrieve(self, question: str, confidence_threshold: float = 0.75, k: int = 5) -> List[Document]:
        """
        Retrieve relevant chunks with confidence scoring.
        """
        if not self.vector_store:
            raise ValueError("No ArXiv documents loaded. Run load_and_process first.")
        results = self.vector_store.similarity_search_with_relevance_scores(question, k=k)
        filtered_results = [doc for doc, score in results if score >= confidence_threshold]
        print(f"Found {len(filtered_results)} relevant chunks above threshold {confidence_threshold}")
        return filtered_results


class WebSearcher:
    """
    Handles web search functionality using the Tavily API.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = TavilyClient(api_key=api_key or os.environ["TAVILY_API_KEY"])

    def search(
        self, query: str, max_results: int = 5, include_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        domain_filter = ""
        if include_domains:
            domain_filter = " OR ".join([f"site:{domain}" for domain in include_domains])
            domain_filter = f"({domain_filter}) "
        optimized_query = f"{domain_filter}{query}"
        print(f"Searching with query: {optimized_query}")
        response = self.client.search(
            query=optimized_query,
            search_depth="advanced",
            include_answer=True,
            max_results=max_results,
        )
        results = [
            {"content": r["content"], "url": r["url"], "title": r.get("title", "Unknown Title")}
            for r in response["results"]
        ]
        print(f"Found {len(results)} web results")
        return results


class RAGAgent:
    """
    Agent class that encapsulates the RAG (Retrieval-Augmented Generation) functionality.
    Each instance has its own conversation memory (which starts clear) and grows with every question.
    """

    def __init__(self, arxiv_links: List[str], force_recreate: bool = False):
        # Initialize conversation memory (fresh for each agent instance)
        self.memory = ConversationBufferMemory(return_messages=False, output_key="answer", input_key="question")
        # Initialize ArXiv processor and load documents from provided links
        self.arxiv_processor = ArXivProcessor()
        self.arxiv_processor.load_and_process(arxiv_links, force_recreate=force_recreate)
        # Initialize Web Searcher
        self.web_searcher = WebSearcher()
        # Build the workflow state graph
        self.workflow = StateGraph(AgentState)
        self.workflow.add_node("router", router_node)
        self.workflow.add_node("arxiv_retrieval", arxiv_retrieval_node)
        self.workflow.add_node("web_search", web_search_node)
        self.workflow.add_node("synthesize", synthesize_answer_node)
        self.workflow.add_node("update_memory", update_memory_node)
        self.workflow.set_entry_point("router")
        self.workflow.add_conditional_edges(
            "router", lambda state: state["next"], {"web_search": "web_search", "arxiv_retrieval": "arxiv_retrieval"}
        )
        self.workflow.add_edge("arxiv_retrieval", "synthesize")
        self.workflow.add_edge("web_search", "synthesize")
        self.workflow.add_edge("synthesize", "update_memory")
        self.workflow.add_edge("update_memory", END)
        self.app = self.workflow.compile()

    def ask(self, question: str) -> str:
        """
        Ask a question to the RAG system. The agent will use its conversation memory,
        perform retrieval (via ArXiv or web), synthesize an answer, update the conversation history,
        and then return the answer.
        """
        initial_history = self.memory.load_memory_variables({}).get("history", "")
        initial_state: AgentState = {
            "question": question,
            "arxiv_results": None,
            "web_results": None,
            "answer": "",
            "conversation_history": initial_history,
            "memory": self.memory,
            "arxiv_processor": self.arxiv_processor,
            "web_searcher": self.web_searcher,
        }
        result = self.app.invoke(initial_state)
        if "memory" in result:
            self.memory = result["memory"]
        print("\n>>> Answer:")
        print(result["answer"])
        print("=" * 80)
        return result["answer"]


if __name__ == "__main__":
    agent = RAGAgent(
        arxiv_links=[
            "https://arxiv.org/pdf/2305.10343.pdf",  # Quantum computing paper
            "https://arxiv.org/pdf/2303.04137.pdf",  # LLM research paper
        ],
        force_recreate=False,
    )
    agent.ask("How do quantum algorithms impact modern cryptography?")
