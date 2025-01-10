
# Assignment 1: LangGraph Demo Agent

Welcome to Assignment 1 of this mentorship program. The primary objective of this assignment is to ensure that you successfully set up all the essential tools required for the various assignments and team projects you will encounter throughout the course. These tools include LangGraph, and OpenAI among others. In this assignment, you will be creating a LangGraph demo agent. Follow the instructions below to set up your environment and get started with the assignment.

## Directory Structure

```
assignments/
└── week_01/
    └── langgraph-demo-agent/
        ├── agent.py
        ├── langgraph.json
        ├── requirements.txt
        ├── .env_example
    ├── README.md
```

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local system.

```bash
git clone https://github.com/Aggregate-Intellect/maven-course.git
cd maven-course
cd assignments/week_01/langgraph-demo-agent
```

### 2. Set Up a Virtual Environment

It's recommended to create a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

All required packages for LangGraph to setup are listed in the `requirements.txt` file. Install them using the following command:

```bash
pip install -Ur requirements.txt
```

### 4. Set Up Environment Variables

You need to create a `.env` file to store API keys. This file is critical for running the agent.

1. Create a `.env` file by copying the example provided:

```bash
cp .env_example .env
```

2. Fill in the required API keys (e.g., [OpenAI](https://openai.com/index/openai-api/), [Tavily](https://app.tavily.com/)):

```bash
# Example:
echo "OPENAI_API_KEY='your-openai-api-key-here'" > .env
echo "TAVILY_API_KEY='tavily-api-key-here'" >> .env
```

Make sure you have the keys ready from the respective services.

### 5. Run Agent Locally
Open a terminal and go to the `langgraph-demo-agent` folder. Run the following command to run LangGraph API server in development mode. This will open open a new browser window with the LangGraph Studio UI.

```bash
langgraph dev
```
### 6. Test the service
In the LangGraph Studio UI, enter a message to test the agent. For example, enter `latest AI News in the quantum computing space`.

## Completing the Assignment

 After following the steps above, you should have a fully operational LangGraph Agent Service running locally on your machine. To complete the assignment `Verify that the Agent service is setup correctly. If you got a response to the prompt entered in the LangGraph Studio UI, you have successfully completed the assignment`.

## Additional Resources

[Langchain Ecosystem](https://python.langchain.com/docs/introduction/)

`Langchain key components`:
[Chat models](https://python.langchain.com/docs/how_to/#chat-models)
[LLMs](https://python.langchain.com/docs/how_to/#llms)
[Message](https://python.langchain.com/docs/how_to/#messages)
[Prompt Templates](https://python.langchain.com/docs/how_to/#prompt-templates)
[Tools](https://python.langchain.com/docs/how_to/#tools)
[Agents](https://python.langchain.com/docs/how_to/#agents)

[LangGraph Key Concepts](https://langchain-ai.github.io/langgraph/concepts/)
[LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

[LangSmith Documentation](https://smith.langchain.com/docs/)

Good luck with the assignment!
