import os
from typing import Literal, Annotated, Sequence, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from pydantic import BaseModel
import functools
import operator
from dotenv import load_dotenv

from prompts import SUPERVISOR_PROMPT, INPUT_PROMPT

# Load environment variables from .env file
load_dotenv()

# Define the members of the workflow
MEMBERS = ["Researcher", "Coder"]
# Define the possible options for the next step in the workflow
OPTIONS = ["FINISH"] + MEMBERS

# Define the response model for routing using Pydantic
class RouteResponse(BaseModel):
    next: Literal[tuple(OPTIONS)]

# Define the state structure for the agent using TypedDict
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# Function to handle agent invocation and return the result
def agent_node(state, agent, name):
    # Invoke the agent with the current state
    result = agent.invoke(state)
    # Return the result as a dictionary with the latest message
    return {"messages": [HumanMessage(content=result["messages"][-1].content, name=name)]}

# Initialize the language model (LLM) with GPT-4
llm = ChatOpenAI(model="gpt-4")
# Initialize the Tavily search tool with a maximum of 2 results
tavily_tool = TavilySearchResults(max_results=2)
# Initialize the Python REPL tool
python_repl_tool = PythonREPLTool()

# Define the supervisor agent function
def supervisor_agent(state):
    # Create a chain with the supervisor prompt and the LLM
    supervisor_chain = (
        SUPERVISOR_PROMPT
        | llm.with_structured_output(RouteResponse)
    )
    # Invoke the chain with the current state
    return supervisor_chain.invoke(state)

# Create the research agent using the LLM and the Tavily tool
research_agent = create_react_agent(llm, tools=[tavily_tool])
# Create a partial function for the research node
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# Create the code agent using the LLM and the Python REPL tool
code_agent = create_react_agent(llm, tools=[python_repl_tool])
# Create a partial function for the code node
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

# Define the workflow using StateGraph
workflow = StateGraph(AgentState)
# Add nodes to the workflow
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("supervisor", supervisor_agent)

# Add edges between nodes
for member in MEMBERS:
    workflow.add_edge(member, "supervisor")

# Define conditional edges based on the next step
conditional_map = {k: k for k in MEMBERS}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

# Add the starting edge
workflow.add_edge(START, "supervisor")

# Set up memory
memory = MemorySaver()

# Compile the workflow
graph = workflow.compile(checkpointer=memory,interrupt_before=["Coder"])