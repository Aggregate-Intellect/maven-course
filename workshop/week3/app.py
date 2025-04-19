import chainlit as cl
from chainlit.message import Message

from src import RAGAgent

agent = RAGAgent(
    arxiv_links=[
        "https://arxiv.org/pdf/2305.10343.pdf",  # Quantum computing paper
        "https://arxiv.org/pdf/2303.04137.pdf",  # LLM research paper
    ],
    force_recreate=False,
)


@cl.on_chat_start
async def on_chat_start():
    """Send a welcome message when the chat starts."""
    welcome_text = "Welcome to the AISC Demo 04! \n\n" "Agentic RAG System with ArXiv + Web Fallback "
    await cl.Message(content=welcome_text).send()


@cl.on_message
async def on_message(message: Message):
    """Handle incoming messages."""
    print(message.content)
    answer = agent.ask(message.content)
    await cl.Message(content=answer).send()
