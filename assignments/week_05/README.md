# Assignment 5: Deploying the Agentic Application

Welcome to Assignment 5! In this assignment, you will learn how to deploy the agentic application we've been building so far, either using LangGraph Cloud or a Gradio dashboard.

## Objective
Your objective is to deploy your agentic system on LangGraph Cloud or integrate it with a Gradio dashboard to allow global access.

## Prerequisites
Before starting, ensure the following:
- You have successfully completed Assignment 4.
- Your development environment is fully set up. If not, refer to the README file from Assignment 4 and follow the setup instructions.

Ensure you have:
- Environment Setup: A .env file in your project folder with valid API keys for OpenAI and Tavily. Make sure the API keys are not enclosed in braces, brackets, or quotes.
- Python: Python version 3.8+ installed on your system.
- Required Libraries: Familiarity with LangChain, LangGraph, and their integration.

## Assignment Tasks

### Option 1: Deploying to LangGraph Cloud
LangGraph Cloud is a managed service for deploying and hosting LangGraph applications. It allows you to expose the functionality of your LangGraph system through Assistants—an abstraction that provides API endpoints for your cognitive graph architecture.

If your agentic system is functioning locally on LangGraph Studio or your terminal, your next step is to deploy it to the cloud, making it accessible from anywhere, similar to a production application.

To deploy your LangGraph application to LangGraph Cloud, refer to the following guide:

LangGraph Cloud Quick Start Guide: https://langchain-ai.github.io/langgraph/cloud/quick_start/

*Note: LangGraph Cloud is a paid service. If you prefer not to use it, you can proceed with the alternative option below.*

### Option 2: Integrating Gradio Dashboard
If you're not using LangGraph Cloud, we’ve provided an alternative method: running your agentic system locally and making it globally accessible through a Gradio dashboard.

This option allows users around the world to interact with your application via the Gradio UI. However, be aware that with Gradio it not straighforward to integerate advanced features of LangGraph, such as human-in-the-loop interactions or pausing and resuming graph execution. If your system relies on these concepts, Gradio will not be a viable solution.

In this week’s assignment folder, you will find a `gradio_ui.py` file that adds a Gradio-based frontend to your agentic application.

Steps for Local Deployment and Testing
Follow these steps to integrate Gradio and run your agent locally.

#### 1. Familiarize Yourself with the Code:
Review the provided gradio_ui.py file in this week’s folder to understand how Gradio integrates with your LangGraph agent.

#### 2. Running the Agent Locally
Navigate to the proposal-generation-agent folder from week_02 assignment, open a terminal, and run the following command to build the Docker image and create an agent service:

```bash
langgraph test
```

#### 3. Testing the Service
To test the agent locally, open another terminal and call the service endpoint. Make sure port 8123 is available for this service by running:

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

Once the port is available, run this curl command to test your service:

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
                "content": "Enter your input prompt here"
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

#### 4. Running the Gradio UI
Once your agent is successfully running and you've verified it locally, navigate to the week_05 folder and install Gradio:

```bash
pip install gradio
```

Then run the gradio_ui.py file, to make the dashboard accesible to everyone via a public link use `share = True`, when lanuching the dashboard, please refer to `gradio_ui.py` for more details:

```bash
python3 gradio_ui.py
```

Now you have a langgraph agentic application running as a service locally on your system, accessible to the world via gradio dashboard.

## Completing the Assignment

By the end of this assignment, your agentic system should be deployed either on LangGraph Cloud or accessible via a Gradio dashboard. Users should be able to interact with your application seamlessly.

To complete the assignment, try invoking your agent via the public Gradio link or through Langsmith if using LangGraph Cloud, and validate the responses.

Good luck!