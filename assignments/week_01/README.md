
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

### LangGraph Studio

- Currently, LangGraph only supports macOS. 
- Download the latest `.dmg` file of LangGraph Studio by clicking [here](https://langgraph-studio.vercel.app/api/mac/latest).

### Docker

- Install Docker Desktop for your system. You can follow the official [Docker Desktop installation guide](https://docs.docker.com/engine/install/).

## Setup Instructions

LangGraph Studio requires docker-compose version 2.22.0+ or higher. Please make sure you have [Docker Desktop](https://docs.docker.com/engine/install/) installed and running before continuing.

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

2. Fill in the required API keys (e.g., OpenAI, Anthropic, Tavily):

```bash
# Example:
echo "OPENAI_API_KEY='your-openai-api-key-here'" > .env
echo "ANTHROPIC_API_KEY='your-anthropic-api-key-here'" >> .env
```

Make sure you have the keys ready from the respective services.

### 5. Verify Docker Setup

This project relies on Docker for some operations. Ensure that Docker is running before you proceed. You can check Docker’s status by running:

```bash
docker --version
```

### 6. Open LangGraph Studio

If you want to visualize and debug the agent flow, now you can use LangGraph Studio:

- Open the application and authenticate via LangSmith.
- Choose the `langgraph-demo-agent` folder as the project folder in LangGraph Studio.
- Use the UI to run, debug, and interact with the agent visually.

## Completing the Assignment

Once the agent is running, you will be able to interact with it based on the assignment requirements. Follow the course instructions to complete the tasks and submit your results.

## Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://smith.langchain.com/docs/)

Good luck with the assignment!
