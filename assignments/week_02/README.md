# Assignment 2: Proposal Generation Agent

Welcome to Assignment 2 of your course. In this assignment, you will build an agent that generates a proposal for pitching a new weight loss drug to Bausch Health, a Canadian pharmaceutical company. You'll use the LangGraph, OpenAI, and Tavily search API tools that you set up in the [previous assignment](https://github.com/Aggregate-Intellect/maven-course/blob/main/assignments/week_01/README.md).

## Objective

Your task is to create an agent that researches details about Bausch Health and generates a comprehensive proposal for pitching a new weight loss drug to the company.

## Prerequisites

Before starting this assignment, ensure you have completed Assignment 1 and have all the necessary tools and environment set up. If you haven't done so, please refer to the README file from Assignment 1 [here](https://github.com/Aggregate-Intellect/maven-course/blob/main/assignments/week_01/README.md) and follow the setup instructions. 
Make sure to create a .env file proposal-generation-agent similar to week1 assignment with API keys for OPENAI and TAVILY. The api keys shouldn't be enclosed in braces, braackets or quotes etc..

## Assignment Tasks

### 1. Implement the Search Tool

Your first task is to implement the Tavily search tool. This tool will be crucial for gathering information about Bausch Health.

Make sure you understand what the code does and why we're using the Tavily search tool.

### 2. Create the Proposal Agent

Next, you need to define a ReAct Agent using LangGraph. This agent should have access to the Tavily search tool you just created. 

Think about why we're using a ReAct Agent and how it will help in generating the proposal.

### 3. Create the Proposal Agent Prompt

Now, create a prompt for your agent. This prompt should give clear instructions on how to generate the proposal. Consider including the following elements in your prompt:

- Clear instructions for the agent
- Details to be included in the output (e.g., expected cost to produce the drug)
- Structure of the output

Here's an example to get you started:

```python
prompt = """
You are an AI assistant tasked with creating a proposal for a new weight loss drug to pitch to Bausch Health. 
Use the Tavily search tool to gather information about Bausch Health and the pharmaceutical industry.

Your proposal should include:
1. Executive Summary
2. Company Overview (Bausch Health)
3. Product Description
4. Market Analysis
5. Marketing Strategy
6. Financial Projections
   - Include estimated production costs
   - Projected sales and revenue
7. Conclusion

Ensure your proposal is well-structured, informative, and persuasive.
"""

# Your task: Refine and expand this prompt as needed
```

Consider why each section of the proposal is important and how it contributes to a compelling pitch.

### 4. Implement the Workflow

Your final task is to implement the entire workflow using LangGraph. Your implementation should:

1. Initialize the Tavily search tool
2. Create the ReAct Agent with your custom prompt
3. Set up the LangGraph workflow
4. Execute the workflow to generate the proposal

Think about how each component fits together to create a cohesive workflow.

### 5. Verify Docker Setup

This project relies on Docker for some operations. Ensure that Docker is running before you proceed. You can check Docker’s status by running:

```bash
docker --version
```
### 6. Run Agent Locally
Open a terminal and go to the `proposal-generation-agent` folder. Run the following command to build the docker image and create an agent service

```bash
langgraph test
```

### 7. Test the service

Open another terminal and call the endpoint, to generate the proposal. Please ensure that the port 8123 is available to run this service. You can check that by running the following:
 
 Mac and Linux:

```bash
lsof -i :8123
```

Windows:

```bash
netstat -an | find "8123"
```

If the port is in use, it will appear in the output make sure to note down the process id (PID) of the process running on the port. If nothing appears, the port is available. If the port is in use, and running a non critical process you can kill that process to make the port available again by doing the following:

Mac or Linux:

```bash
kill -9 PID
```

Windows 

```bash
taskkill /PID PID /F
```

Once port is available to test the servie run:

```bash
curl --request POST \
    --url http://localhost:8123/runs/stream \
    --header 'Content-Type: application/json' \
    --data '{
    "assistant_id": "agent",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "Generate a proposal for pitching our new weight loss drug to Bausch Health"
            }
        ]
    },
    "metadata": {},
    "config": {
        "configurable": {}
    },
    "multitask_strategy": "reject",
    "stream_mode": [
        "values"
    ]
}'
```

### 8. OPTIONAL: Integrate UI using LangGraph Studio

Currently, LangGraph Studio only supports macOS. To use LangGraph Studio with other OS, you'll have to use VirtualBox with macOS. To install LangGraph Studio on macOS, follow these steps:

- Download the latest `.dmg` file of LangGraph Studio by clicking [here](https://langgraph-studio.vercel.app/api/mac/latest).
- LangGraph Studio requires docker-compose version 2.22.0+ or higher. Please ensure you have [Docker Desktop](https://docs.docker.com/engine/install/) installed and running before continuing.

If you want to visualize and debug the agent flow, you can use LangGraph Studio:

- Open the application and authenticate via LangSmith.
- Choose the `proposal-generation-agent` folder as the project folder in LangGraph Studio.
- Use the UI to run, debug, and interact with the agent visually.

## Completing the Assignment

After following the steps above, you should have a fully operational LangGraph Agent Service running locally on your machine. To complete the assignment, verify that the Agent service is set up correctly by validating the response from the service to input prompts sent via API requests.

Remember, the goal is not just to complete the assignment, but to understand how these tools can be used to create an intelligent agent capable of complex tasks. Good luck with your assignment! 
Also in case you prefer working with notebooks or have any issues with setting up required tools as part of week 1 assignment, you can open the notebook in the week02 folder of the repo on [google colab](https://colab.research.google.com/) in place of running the agent locally.

## Additional Resources

To aid you in this assignment, refer to these resources:
- [Open AI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Tavily Search Langchain](https://python.langchain.com/v0.2/docs/integrations/tools/tavily_search/)
- [Build ReAct Agent With LangGraph](https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/)

