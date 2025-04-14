from typing import Dict

import dotenv
from langchain_openai import ChatOpenAI
from langsmith import Client, wrappers
from openai import OpenAI
from pydantic import BaseModel, Field
from utils import EvaluationDataset, Prompt

from src import RAGAgent

dotenv.load_dotenv()
client = Client()
openai_client = wrappers.wrap_openai(OpenAI())

prompt = Prompt.default_eval_prompt()

agent = RAGAgent(
    arxiv_links=[
        "https://arxiv.org/pdf/2305.10343.pdf",  # Quantum computing paper
        "https://arxiv.org/pdf/2303.04137.pdf",  # LLM research paper
    ],
    force_recreate=False,
)


def create_dataset(eval_dataset: EvaluationDataset, dataset_name: str) -> str:
    """
    Create a LangSmith dataset from evaluation questions if it doesn't exist already.
    Return a name of the dataset.
    """
    datasets = client.list_datasets()
    dataset_names = [ds.name for ds in datasets]

    if dataset_name in dataset_names:
        print(f"Dataset `{dataset_name}` already exists")
        return dataset_name

    dataset = client.create_dataset(dataset_name=dataset_name)
    client.create_examples(dataset_id=dataset.id, examples=eval_dataset.to_examples())
    print(f"Created dataset `{dataset_name}` with {len(eval_dataset.questions)} examples")
    return dataset_name


# Define the application logic you want to evaluate inside a target function
# The langsmith SDK will automatically send the inputs from the dataset to your target function
def target(inputs: Dict[str, str]) -> Dict[str, str]:
    response = agent.ask(inputs["question"])
    return {"response": response}


# Define output schema for the LLM judge
class Grade(BaseModel):
    score: bool = Field(
        description="Boolean that indicates whether the response is accurate relative to the reference answer"
    )


def accuracy(outputs: Dict[str, str], reference_outputs: Dict[str, str]) -> bool:
    messages = prompt.to_messages(answer=reference_outputs["answer"], response=outputs["response"])

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model_with_structured_output = model.bind_tools([Grade])
    ai_msg = model_with_structured_output.invoke(messages)

    grade = Grade.model_validate(ai_msg.tool_calls[0]["args"])
    return grade.score


def run_evals():
    # Load evaluation questions
    eval_dataset = EvaluationDataset.load_default()

    # Create dataset
    dataset_name = create_dataset(eval_dataset, dataset_name="rag_agent_evaluation")

    # Run evaluations
    experiment_results = client.evaluate(
        target,
        data=dataset_name,
        evaluators=[accuracy],  # can add more evaluators here
    )

    print(f"Explore your results in LangSmith Experiments UI. Experiment name: {experiment_results.experiment_name}")


if __name__ == "__main__":
    run_evals()
