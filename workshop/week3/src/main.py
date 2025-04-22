import os
import shutil
from typing import Any, Dict, List, Literal, Optional, TypedDict

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
from pyboxen import boxen
from tavily import TavilyClient

dotenv.load_dotenv()


class AgentState(TypedDict, total=False):
    question: str  # User query
    routing_decision: Literal["arxiv", "web", "both"]
    arxiv_results: Optional[List[Document]]
    web_results: Optional[List[Dict[str, Any]]]
    direct_answer: Optional[str]
    answer: str
    conversation_history: str
    memory: Any
    arxiv_processor: Any
    web_searcher: Any
    next_node: Optional[Literal["web_search", "synthesize"]]


# Router prompt with three-way decision
router_prompt = ChatPromptTemplate.from_template(
    """
You are a highly specialized research assistant with access to two information sources:
1. A collection of ArXiv research papers
2. A web search tool

Your task is to determine which source(s) would be better to answer the user's question.
FIRST try to use ArXiv papers for scientific and academic questions.
ONLY use web search if:
- The question requires very recent information not likely in research papers
- The question is about general knowledge, news, or non-academic topics
- The question asks for information beyond what academic papers would contain
Choose BOTH if the question requires integrating academic concepts with recent developments, practical applications, or comparing academic views with general information

Consider the conversation history for context.

Question: {question}
Conversation History: {conversation_history}

Respond with ONLY ONE of these two options:
"arxiv" - if the question should be answered using research papers
"web" - if the question requires web search
"both" - if both ArXiv and web search are needed

Your decision should be a single word only (either "arxiv", "web" or "both"). Do not include any explanation, reasoning, or additional text in your response.
"""
)


def router_node(state: AgentState) -> Dict[str, str]:
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = router_prompt | llm | StrOutputParser()
    decision = (
        chain.invoke(
            {
                "question": state["question"],
                "conversation_history": state["conversation_history"],
            }
        )
        .strip()
        .lower()
    )
    if decision not in ["arxiv", "web", "both"]:
        print(
            boxen(
                f"Router Warning: Unexpected decision '{decision}'. Defaulting to 'web'.",
                title=">>> Router Node",
                color="yellow",
                padding=1,
            )
        )
        decision = "web"
    print(boxen(f"Router raw decision: {decision}", title=">>> Router Node", color="blue", padding=1))
    return {"routing_decision": decision}


def arxiv_retrieval_node(state: AgentState) -> Dict[str, Any]:
    question = state["question"]
    decision = state["routing_decision"]
    chunks: List[Document] = []
    next_dest = "synthesize"
    try:
        chunks = state["arxiv_processor"].retrieve(
            question=question,
            confidence_threshold=0.5,
        )
        print(
            boxen(
                f"Found {len(chunks)} relevant ArXiv chunks.",
                title=">>> ArXiv Retrieval Node",
                color="blue",
                padding=(1, 2),
            )
        )
    except Exception as e:
        print(
            boxen(f"Error during ArXiv retrieval: {e}", title=">>> ArXiv Retrieval Node", color="red", padding=(1, 2))
        )
    if decision == "both":
        print(
            boxen(
                "Routing decision was 'both', proceeding to Web Search next.",
                title=">>> Routing",
                color="green",
                padding=(1, 2),
            )
        )
        next_dest = "web_search"
    else:
        print(
            boxen(
                "Routing decision was 'arxiv', proceeding to Synthesize next.",
                title=">>> Routing",
                color="green",
                padding=(1, 2),
            )
        )
    return {"arxiv_results": chunks, "next_node": next_dest}


def web_search_node(state: AgentState) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    direct = None
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        resp = client.search(query=state["question"], max_results=5, include_answer=True, search_depth="advanced")
        results = resp.get("results", [])
        direct = resp.get("answer")
        info = f"Found {len(results)} web results." + (" Direct answer found." if direct else "")
        print(boxen(info, title=">>> Web Search Node", color="blue", padding=(1, 2)))
    except Exception as e:
        print(boxen(f"Error during Web search: {e}", title=">>> Web Search Node", color="red", padding=(1, 2)))
    return {"web_results": results, "direct_answer": direct}


def synthesize_answer_node(state: AgentState) -> Dict[str, str]:
    q = state["question"]
    arxiv = state.get("arxiv_results") or []
    web = state.get("web_results") or []
    direct = state.get("direct_answer")
    history = state["conversation_history"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    final = ""
    src_type = "None"
    prompt_txt = ""
    context = ""
    if arxiv and web:
        print(
            boxen(
                "Synthesizing from Both ArXiv and Web Results",
                title=">>> Synthesize Answer Node",
                color="blue",
                padding=(1, 2),
            )
        )
        src_type = "Combined ArXiv and Web"
        arxiv_src = "\n\n".join(
            [
                f"--- ArXiv Document: {d.metadata.get('source')} (Page {d.metadata.get('page')}) ---\n{d.page_content}"
                for d in arxiv
            ]
        )
        web_src = "\n\n".join(
            [f"--- Web Source [{i+1}]: {r.get('title')} ---\n{r.get('content')}" for i, r in enumerate(web)]
        )
        direct_txt = f"Tavily suggested direct answer: {direct}" if direct else "No direct answer suggested by Tavily."
        context = f"ArXiv Extracts:\n{arxiv_src}\n\nWeb Search Results:\n{web_src}\n\n{direct_txt}"
        prompt_txt = """
        You are a knowledgeable research assistant synthesizing information from both academic papers and web search results.

        Task: Answer the user's question comprehensively using ONLY the provided information. Integrate findings, prioritizing ArXiv for core concepts/theory and web search for recent developments, examples, or general context.

        Question:
        {question}

        Conversation History:
        {conversation_history}

        Information Sources:
        {sources}

        Instructions:
        1. Carefully read and understand all provided ArXiv extracts and web search results.
        2. Synthesize a coherent and comprehensive answer addressing the question.
        3. Structure the response logically (e.g., introduction, key points from ArXiv, relevant web context/examples, conclusion). Use markdown formatting (headers, lists, bolding) for readability.
        4. **Crucially, cite your sources accurately within the text**:
            - For ArXiv info: Use (Author et al., Page X) or (Source: Document Source) if author/page unknown.
            - For Web info: Use [Web Source 1], [Web Source 2], etc., corresponding to the numbers provided.
        5. If the provided information is insufficient or contradictory, state that clearly.
        6. DO NOT include information not present in the sources. Base the entire answer strictly on the provided text.
        7. Consider the `direct_answer` suggestion from Tavily but verify against the full web results before incorporating its content.

        Synthesized Answer:
"""
    elif arxiv:
        print(
            boxen("Synthesizing from ArXiv Results", title=">>> Synthesize Answer Node", color="blue", padding=(1, 2))
        )
        src_type = "ArXiv Papers"
        context = "\n\n".join(
            [
                f"--- Document: {d.metadata.get('source')} (Page {d.metadata.get('page')}) ---\n{d.page_content}"
                for d in arxiv
            ]
        )
        prompt_txt = """
        You are a knowledgeable research assistant specializing in mathematical theory and scientific literature analysis.
        Your goal is to generate clean, formatted responses to user questions based solely on the provided ArXiv sources.

        Question:
        {question}

        Relevant Extracts from ArXiv Papers:
        {sources}

        Conversation History:
        {conversation_history}

        Instructions for Synthesizing the Answer:
        1. Read the extracts thoroughly and understand the concepts.
        2. Answer the question comprehensively using ONLY the provided context.
        3. Organize the response into the following markdown sections (if applicable):
              - Summary
              - Key Concepts
              - Theoretical Results
              - Implications / Applications
        4. Cite from the paper in the format: (Author et al., Page X). If page number is unknown, write: (Author et al.).
        5. Avoid repetition, excessive formal tone, or generic commentary. Be clear and concise.
        6. If the provided text lacks enough detail to answer, state it clearly and suggest what additional info is needed.

        Now, write a well-structured, markdown-formatted answer to the question and it should be in a readable format as well.
        
        Your answer:
"""
    elif web:
        print(boxen("Synthesizing from Web Results", title=">>> Synthesize Answer Node", color="blue", padding=(1, 2)))
        src_type = "Web Search Results"
        context = "\n\n".join(
            [f"--- Web Source [{i+1}]: {r.get('title')} ---\n{r.get('content')}" for i, r in enumerate(web)]
        )
        prompt_txt = """
        You are a knowledgeable research assistant providing accurate information based on web search results.

        Question: {question}
        
        Here are relevant web search results:
            {sources}

        Conversation History: {conversation_history}

        Instructions:
        1. Synthesize a comprehensive answer using ONLY the information provided above.
        2. Cite sources using [1], [2], etc. corresponding to the source numbers above.
        3. Consider the `direct_answer` suggestion from Tavily but verify against the full web results before incorporating its content.
        4. If the search results don't contain sufficient information, acknowledge the limitations.
        5. DO NOT make up information not present in the sources. 
        6. Include only facts supported by the sources.
        7. Use markdown formatting for readability.

        Your answer:
"""
    else:
        print(boxen("No relevant information found to synthesize answer."))
        final = "I could not find relevant information to answer your question."
    if src_type != "None":
        prompt = ChatPromptTemplate.from_template(prompt_txt)
        chain = prompt | llm | StrOutputParser()
        final = chain.invoke({"question": q, "sources": context, "conversation_history": history})
        if src_type in ["Web Search Results", "Combined ArXiv and Web"] and web:
            citations = "\n\n**Web Sources:**\n" + "\n".join([f"[{i+1}] {r.get('url')}" for i, r in enumerate(web)])
            final += citations
    output = f"""## Context
**Question:** {q}
**Source(s) Used:** {src_type}

## Response
{final}
"""
    return {"answer": output}


def update_memory_node(state: AgentState) -> Dict[str, Any]:
    mem = state["memory"]
    mem.save_context({"question": state["question"]}, {"answer": state["answer"]})
    return {"conversation_history": mem.load_memory_variables({}).get("history", "")}


class ArXivProcessor:
    def __init__(self) -> None:
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "Section"), ("##", "Subsection"), ("###", "Subsubsection")]
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", "(?<=\\. )", " ", ""]
        )
        self.vector_store = None

    def load_and_process(self, pdf_urls: List[str], force_recreate: bool = False) -> None:
        if os.path.exists("./arxiv_db") and not force_recreate:
            print(
                boxen(
                    "Loading existing vector store from ./arxiv_db", title=">>> Initialization", color="cyan", padding=1
                )
            )
            self.vector_store = Chroma(persist_directory="./arxiv_db", embedding_function=OpenAIEmbeddings())
            return
        if force_recreate and os.path.exists("./arxiv_db"):
            shutil.rmtree("./arxiv_db")
        all_chunks: List[Document] = []
        for url in pdf_urls:
            print(boxen(f"Loading PDF from {url}", title=">>> PDF Loading", color="blue", padding=1))
            pages = PyPDFLoader(url).load()
            for page in pages:
                text = f"# {page.metadata['source']}\n## Page {page.metadata['page']}\n{page.page_content}"
                header_chunks = self.header_splitter.split_text(text)
                small_chunks = self.text_splitter.split_documents(header_chunks)
                all_chunks.extend(small_chunks)
        print(
            boxen(
                f"Created {len(all_chunks)} chunks from {len(pdf_urls)} PDFs",
                title=">>> Processing Complete",
                color="green",
                padding=1,
            )
        )
        self.vector_store = Chroma.from_documents(
            documents=all_chunks, embedding=OpenAIEmbeddings(), persist_directory="./arxiv_db"
        )

    def retrieve(self, question: str, confidence_threshold: float = 0.75, k: int = 5) -> List[Document]:
        if not self.vector_store:
            raise ValueError("No ArXiv documents loaded. Run load_and_process first.")
        results = self.vector_store.similarity_search_with_relevance_scores(question, k=k)
        filtered = [doc for doc, score in results if score >= confidence_threshold]
        print(
            boxen(
                f"Found {len(filtered)} relevant chunks above threshold {confidence_threshold}",
                title=">>> ArXivProcessor",
                color="yellow",
                padding=1,
            )
        )
        return filtered


class RAGAgent:
    def __init__(self, arxiv_links: List[str], force_recreate: bool = False):
        self.memory = ConversationBufferMemory(return_messages=False, output_key="answer", input_key="question")
        self.arxiv_processor = ArXivProcessor()
        self.arxiv_processor.load_and_process(arxiv_links, force_recreate=force_recreate)
        self.web_searcher = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.workflow = StateGraph(AgentState)
        self.workflow.add_node("router", router_node)
        self.workflow.add_node("arxiv_retrieval", arxiv_retrieval_node)
        self.workflow.add_node("web_search", web_search_node)
        self.workflow.add_node("synthesize", synthesize_answer_node)
        self.workflow.add_node("update_memory", update_memory_node)
        self.workflow.set_entry_point("router")
        self.workflow.add_conditional_edges(
            "router",
            lambda state: state["routing_decision"],
            {"arxiv": "arxiv_retrieval", "web": "web_search", "both": "arxiv_retrieval"},
        )
        self.workflow.add_conditional_edges(
            "arxiv_retrieval",
            lambda state: state.get("next_node", "synthesize"),
            {"web_search": "web_search", "synthesize": "synthesize"},
        )
        self.workflow.add_edge("web_search", "synthesize")
        self.workflow.add_edge("synthesize", "update_memory")
        self.workflow.add_edge("update_memory", END)
        self.app = self.workflow.compile()

    def ask(self, question: str) -> str:
        history = self.memory.load_memory_variables({}).get("history", "")
        initial_state: AgentState = {
            "question": question,
            "routing_decision": None,
            "arxiv_results": None,
            "web_results": None,
            "direct_answer": None,
            "answer": "",
            "conversation_history": history,
            "memory": self.memory,
            "arxiv_processor": self.arxiv_processor,
            "web_searcher": self.web_searcher,
            "next_node": None,
        }
        result = self.app.invoke(initial_state)
        if "memory" in result:
            self.memory = result["memory"]
        return result.get("answer", "")


if __name__ == "__main__":
    # Example usage
    agent = RAGAgent(
        arxiv_links=[
            "https://arxiv.org/pdf/2305.10343.pdf",
            "https://arxiv.org/pdf/2303.04137.pdf",
        ],
        force_recreate=False,
    )
    question = input("Enter your question: ")
    print(agent.ask(question))
