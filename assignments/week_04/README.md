# Assignment 4: Advanced Multi-Agent Proposal Generation System

Welcome to Assignment 4 of your course. In this assignment, you will extend the Enhanced Proposal Generation Agent developed in Assignment 3. This week, you'll further enhance the agent's capabilities by implementing a more sophisticated multi-agent system, introducing structured outputs, and adding human-in-the-loop functionality. The focus is on creating a robust, interactive system that can generate, critique, and visualize proposals while allowing for human intervention. Please note that this assignment builds upon the autonomous supervisor-based workflow introduced last week, adding more complexity and interactivity to the system.

*Since the assignment involves a human-in-the-loop component which requires interrupting and restarting graph execution, it is recommended to complete this assignment using a Jupyter notebook or similar interactive environment.*

## Objective

Your task is to create an advanced multi-agent system that not only generates a comprehensive proposal for pitching a new weight loss drug to Bausch Health but also incorporates a critique process, financial projections, and visualization capabilities. This will involve implementing multiple specialized agents (Researcher, Critique, and Coder), a more complex workflow, structured outputs, and the ability for human intervention.

## Prerequisites

Before starting this assignment, ensure you have completed Assignment 3 and have all the necessary tools and environment set up. If you haven't done so, please refer to the README file from Assignment 3 and follow the setup instructions.

Ensure you have the following:

- **Environment Setup**: A `.env` file in your project folder with API keys for OPENAI and TAVILY. The API keys should not be enclosed in braces, brackets, or quotes.
- **Python Environment**: Python 3.8+ installed on your system.
- **Required Libraries**: Familiarity with LangChain, LangGraph, and their integration.

## Assignment Tasks

### Recommended:

### 1. Understand the Enhanced Workflow

Familiarize yourself with the new workflow introduced in `agent.py`. This workflow now incorporates three specialized agents and a more complex decision-making process.

**Agents:**
- Researcher: Gathers information and generates the initial proposal.
- Critique: Reviews the proposal for quality and provides feedback.
- Coder: Generates Python code for ROI visualization.

**Workflow Management:** The system now uses a more sophisticated process to manage transitions between agents and incorporate human input.

### 2. Implement Structured Outputs

Review and implement the structured outputs in `agent.py`:

- **ResearcherResponse**: Contains financial projections for the proposal.
- **CritiqueResponse**: Stores feedback on the proposal and acceptance decision.

Ensure these structured outputs are correctly integrated into the workflow and used by the respective agents.

### 3. Enhance State Management

Examine and implement the `AgentState` class in `agent.py`. This class should manage the workflow state, including:
- Step count
- Research response
- Proposal content
- Proposal acceptance status
- Generated graph code

### 4. Implement Human-in-the-Loop Functionality

Add capabilities for human intervention in the workflow:

- Implement a mechanism to modify the state, such as adjusting financial projections.
- Ensure these modifications can be made during the execution of the workflow.
- Update the workflow logic to accommodate these interventions.

### 5. Develop the Coder Agent

Implement the Coder Agent functionality:

- Create a function that generates clear, executable Python code for ROI visualization based on the proposal data.
- Ensure the generated code can be executed to produce meaningful visualizations.

### 6. Refine the Workflow Logic

Enhance the conditional logic in the workflow:

- Implement the `should_continue` and `route_critique` functions to control the flow between agents.
- Ensure the workflow correctly handles different scenarios (e.g., proposal acceptance, rejection, maximum iterations).


### 4. After understanding the code, you can just run the notebook in colab.

### 5. Open the `Week4Assignment.ipynb` in colab, provide the required api keys, and run all cells.

### If you prefer to do the assignment by running the setup locally the recommendation is to do it on langgraph studio if you don't have access to langgraph studio or you want to test service in your terminal you can follow these steps:

### 6. Configure LangGraph

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

### 7. Install Required Dependencies

Navigate to the `proposal-and-roi-generation-agent` folder and install the necessary Python packages using `requirements.txt`.

```bash
pip install -r requirements.txt
```

Ensure all dependencies, including `langchain`, `langgraph`, `dotenv`, and other required libraries, are installed.

### 8. Verify Docker Setup

This project relies on Docker for running the LangGraph services. Ensure that Docker is installed and running on your machine.

Check Docker's status by running:

```bash
docker --version
```

If Docker is not running, start it before proceeding.

### 9. Run the Agent Locally

Open a terminal and navigate to the `proposal-and-roi-generation-agent` folder. Build the Docker image and start the agent service by running:

```bash
langgraph test
```

### 10. Test the Service

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

## Completing the Assignment

After implementing the enhancements above, you should have an advanced Multi-Agent Proposal Generation System. To complete the assignment:

1. Verify Functionality:
   - Ensure that the system successfully generates a comprehensive proposal, including all required sections and ROI calculations.
   - Confirm that the Critique Agent effectively reviews and provides feedback on the proposal.
   - Verify that the Coder Agent generates accurate and visually informative ROI graph code.

2. Review Workflow Management:
   - Check that the system correctly manages the transitions between the Researcher, Critique, and Coder agents.
   - Validate that each agent performs its designated tasks without errors.

3. Test Human-in-the-Loop Features:
   - Ensure that you can successfully intervene and modify the workflow state during execution.
   - Verify that these modifications have the expected impact on subsequent steps in the workflow.

4. Analyze Visualization Capabilities:
   - Review the ROI visualization code generated by the Coder Agent.
   - Execute the code and assess the clarity and informativeness of the resulting visualization.

## Additional Resources

To aid you in this assignment, refer to these resources:

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Tavily API Documentation](https://tavily.com/docs)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html) (for visualization code)
- [Pydantic Documentation](https://docs.pydantic.dev/)