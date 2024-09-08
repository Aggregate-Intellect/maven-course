
# Assignment 1: LangGraph Demo Agent

Welcome to Assignment 1 of your course. In this assignment, you will be working with a LangGraph demo agent. Follow the instructions below to set up your environment and get started with the assignment.

## Directory Structure

```
assignments/
└── week_01/
    └── langgraph-demo-agent/
        ├── agent.py
        ├── langgraph.json
        ├── requirements.txt
    ├── README.md
    ├── .env_example
```

## Download

Before proceeding, ensure that you have the following tools installed on your system:

### Docker

- Install Docker Desktop for your system. You can follow the official [Docker Desktop installation guide](https://docs.docker.com/engine/install/).

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local system.

```bash
git clone https://github.com/Aggregate-Intellect/maven-course.git
cd assignments/week_01/langgraph-demo-agent
```

### 2. Set Up a Virtual Environment

It's recommended to create a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

All required packages for LangGraph to setup are listed in the `requirements.txt` file. Install them using the following command:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

You need to create a `.env` file to store API keys. This file is critical for running the agent.

1. Create a `.env` file by copying the example provided:

```bash
cp .env.example .env
```

2. Fill in the required API keys (e.g., [OpenAI](https://openai.com/index/openai-api/), [Tavily](https://docs.tavily.com/docs/gpt-researcher/getting-started)):

```bash
# Example:
echo "OPENAI_API_KEY='your-openai-api-key-here'" > .env
echo "TAVILY_API_KEY='tavily-api-key-here'" >> .env
```

Make sure you have the keys ready from the respective services.

### 5. Verify Docker Setup

This project relies on Docker for some operations. Ensure that Docker is running before you proceed. You can check Docker’s status by running:

```bash
docker --version
```
### 6. Run Agent Locally
Open a terminal and go to the `langgraph-demo-agent` folder. Run the following command to build the docker image and create an agent service

```bash
langgraph test
```
### 7. Test the service
Open another terminal and call the endpoint, to check the `latest AI News in the biotech space`. To test with different prompts replace the `content` field in the request.

```bash
# Example:
curl --request POST \
    --url http://localhost:8123/runs/stream \
    --header 'Content-Type: application/json' \
    --data '{
    "assistant_id": "agent",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "Give me the latest AI News in the biotech space"
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

- Currently, LangGraph Studio only supports macOS. To use LangGraph Studio with other OS you'll have to use VirtualBOx with MacOS. To install LangGraph Studio on MacOS follow these steps:
- Download the latest `.dmg` file of LangGraph Studio by clicking [here](https://langgraph-studio.vercel.app/api/mac/latest).
- LangGraph Studio requires docker-compose version 2.22.0+ or higher. Please ensure you have [Docker Desktop](https://docs.docker.com/engine/install/) installed and running before continuing.

If you want to visualize and debug the agent flow, now you can use LangGraph Studio:

- Open the application and authenticate via LangSmith.
- Choose the `langgraph-demo-agent` folder as the project folder in LangGraph Studio.
- Use the UI to run, debug, and interact with the agent visually.

## Assignment Objective

The primary objective of this assignment is to ensure that you successfully set up all the essential tools required for the various assignments and team projects you will encounter throughout the course. These tools include LangGraph, Docker, and OpenAI, among others. After following the steps above, you should have a fully operational LangGraph Agent Service running locally on your machine. `To verify the setup make sure the service is responding correctly to input prompts send via API requests`.

## Additional Resources

[Langchain Ecosystem](https://python.langchain.com/v0.2/docs/introduction/)

`Langchain key components`:
[Chat models](https://python.langchain.com/v0.2/docs/concepts/#chat-models)
[LLMs](https://python.langchain.com/v0.2/docs/concepts/#llms)
[Message](https://python.langchain.com/v0.2/docs/concepts/#messages)
[Prompt Templates](https://python.langchain.com/v0.2/docs/concepts/#prompt-templates)
[Tools](https://python.langchain.com/v0.2/docs/concepts/#tools)
[Agents](https://python.langchain.com/v0.2/docs/concepts/#agents)

[LangGraph Key Concepts](https://langchain-ai.github.io/langgraph/concepts/)
[LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

[LangSmith Documentation](https://smith.langchain.com/docs/)

Good luck with the assignment!
