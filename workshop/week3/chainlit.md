# Build Multi-Agent Applications - Hugging Face Spaces Deployment with Chainlit

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