# Assignment 3: Enhanced Proposal Generation Agent

Welcome to Assignment 3 of your course. In this assignment, you will extend the Proposal Generation Agent developed in Assignment 2. This week, you'll enhance the agent's capabilities by introducing a supervisory workflow, integrating additional tools, and refining the proposal generation process using LangGraph and advanced LangChain functionalities.

## Objective

Your task is to create an enhanced agent that not only generates a comprehensive proposal for pitching a new weight loss drug to Bausch Health but also incorporates a supervisory workflow to manage different roles within the agent. This will involve implementing multiple agents (Researcher and Coder), a supervisor to orchestrate their actions, and integrating tools for specialized tasks such as ROI calculations and graph generation.

## Prerequisites

Before starting this assignment, ensure you have completed Assignment 2 and have all the necessary tools and environment set up. If you haven't done so, please refer to the README file from Assignment 2 and follow the setup instructions.

Ensure you have the following:

- **Environment Setup**: A `.env` file named `proposal-generation-agent` with API keys for OPENAI and TAVILY. The API keys should not be enclosed in braces, brackets, or quotes.
- **Docker**: Ensure Docker is installed and running on your machine.
- **LangGraph Tools**: Familiarity with LangGraph and its integration with LangChain.

## Assignment Tasks

### 1. Understand the Enhanced Workflow

Familiarize yourself with the new workflow introduced in `agent.py`. This workflow incorporates multiple agents and a supervisor to manage their interactions.

**Agents:**
- Researcher: Gathers information using the Tavily search tool.
- Coder: Handles calculations and graph generation using Python REPL.

**Supervisor:** Orchestrates the agents' actions and manages the workflow state.

### 2. Implement the Supervisor Agent

The supervisor agent is responsible for managing the workflow between the Researcher and Coder agents. Review the `agent.py` and `prompts.py` files to understand how the supervisor is implemented using LangGraph's StateGraph.

Key Components:
- **RouteResponse Model**: Determines the next agent to act based on the supervisor's prompt.
- **Workflow Initialization**: Sets up the state graph with nodes for each agent and defines the conditional transitions.

### 3. Define and Refine Prompts

Enhance the prompts in `prompts.py` to provide clear instructions for both the supervisor and the agents.

- **SYSTEM_PROMPT**: Guides the supervisor on managing the agents.
- **INPUT_PROMPT**: Provides the initial instructions for generating the proposal, including detailed sections and ROI calculations.

Consider refining the prompts to ensure that each agent performs its designated task effectively and that the supervisor correctly manages the workflow transitions.

### 4. Configure LangGraph

Review and update the `langgraph.json` file to ensure it accurately reflects the dependencies and graph configurations required for the enhanced workflow.

```json
{
    "dependencies": ["."],
    "graphs": {
        "agent": "./agent.py:graph"
    },
    "env": ".env"
}
```

Ensure that all dependencies are correctly listed and that the graph points to the appropriate workflow definition in `agent.py`.

### 5. Install Required Dependencies

Navigate to the `proposal-generation-agent` folder and install the necessary Python packages using `requirements.txt`.

```bash
pip install -r requirements.txt
```

Ensure all dependencies, including `langchain`, `langgraph`, `dotenv`, and other required libraries, are installed.

### 6. Verify Docker Setup

This project relies on Docker for running the LangGraph services. Ensure that Docker is installed and running on your machine.

Check Docker's status by running:

```bash
docker --version
```

If Docker is not running, start it before proceeding.

### 7. Run the Agent Locally

Open a terminal and navigate to the `proposal-generation-agent` folder. Build the Docker image and start the agent service by running:

```bash
langgraph test
```

### 8. Test the Service

Open another terminal and ensure that port 8123 is available. Check the port status:

Mac and Linux:
```bash
lsof -i :8123
```

Windows:
```bash
netstat -an | find "8123"
```

If the port is in use, terminate the process using the appropriate command:

Mac or Linux:
```bash
kill -9 PID
```

Windows:
```bash
taskkill /PID PID /F
```

Once the port is available, execute the following command to generate the proposal:

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
                "content": "Generate a comprehensive proposal for pitching our new weight loss drug to Bausch Health, including ROI calculations and a 5-year ROI trend graph."
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

### 9. OPTIONAL: Integrate UI using LangGraph Studio

LangGraph Studio provides a visual interface to interact with and debug your agent workflow. Currently, it supports only macOS. To use LangGraph Studio on other operating systems, set up a macOS virtual environment using VirtualBox.

Installation Steps on macOS:

1. Download LangGraph Studio:
   - Get the latest .dmg file from [here](https://github.com/langchain-ai/langchain-studio/releases).

2. Install Docker Compose:
   - Ensure you have Docker Desktop installed and running.
   - LangGraph Studio requires docker-compose version 2.22.0 or higher.

3. Run LangGraph Studio:
   - Open the application and authenticate via LangSmith.
   - Select the `proposal-generation-agent` folder as the project directory.
   - Use the UI to run, debug, and visualize the agent workflow.

## Completing the Assignment

After following the steps above, you should have an enhanced Proposal Generation Agent running locally. To complete the assignment:

1. Verify Functionality:
   - Ensure that the agent successfully generates a comprehensive proposal, including all required sections and ROI calculations.
   - Confirm that the 5-year ROI trend graph is accurately generated and integrated into the proposal.

2. Review Workflow Management:
   - Check that the supervisor correctly manages the transitions between the Researcher and Coder agents.
   - Validate that each agent performs its designated tasks without errors.


## Additional Resources

To aid you in this assignment, refer to these resources:

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [LangChain Community Tools](https://python.langchain.com/docs/integrations/tools/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [LangGraph Studio Guide](https://github.com/langchain-ai/langchain-studio)
