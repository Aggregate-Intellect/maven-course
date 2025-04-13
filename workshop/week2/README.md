# 📚 Agentic RAG System with ArXiv + Web Fallback

This project implements an **intelligent research assistant** that retrieves and synthesizes information using:
1. **ArXiv papers** as the primary knowledge source (**RAG approach**)
2. **Web search (Tavily API)** as a fallback mechanism
3. **LangGraph** for orchestrating the decision-making workflow

---

## 🚀 Features

- **Retrieves academic papers** from **ArXiv** using semantic search.
- **Falls back to web search** if no relevant ArXiv results are found.
- **Synthesizes responses** from multiple sources while ensuring proper attribution.
- **Maintains conversation memory** for multi-turn interactions.

---

## 📌 System Architecture

The workflow consists of several nodes:

1. **Router Node**  
   - Decides whether to retrieve information from **ArXiv** or **Web search**.
   - Prioritizes **ArXiv papers** first.
   - Falls back to **web search** if needed.

2. **ArXiv RAG Node**  
   - Loads **PDF files** from ArXiv.
   - **Chunks** them effectively using a specialized strategy.
   - **Stores** information in a vector database for **semantic search**.

3. **Web Search Node**  
   - Uses the **Tavily API** to fetch web search results.
   - **Optimizes queries** to retrieve relevant information.
   - **Filters and processes** results while ensuring proper attribution.

4. **Answer Synthesis Node**  
   - Merges information from ArXiv and Web sources.
   - Uses **context-aware prompts** based on the source.
   - **Generates well-structured responses** with citations.

5. **Conversation Memory Node**  
   - Tracks **previous Q&A** for contextual understanding.
   - Updates conversation state dynamically.
   - Maintains a **sliding window** of relevant history.

6. **Workflow Construction**  
   - Uses **LangGraph** to define the **state graph**.
   - Integrates all nodes and configures decision paths.




