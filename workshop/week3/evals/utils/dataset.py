from __future__ import annotations

import os
from typing import Any, Dict, List, Literal

import yaml
from pydantic import BaseModel

from .path import EVALS_DATA_PATH


class EvaluationQuestion(BaseModel):
    question: str
    answer: str
    category: Literal["internal", "external", "reasoning"]


class EvaluationDataset(BaseModel):
    questions: List[EvaluationQuestion]

    @classmethod
    def from_yaml(cls, path: str) -> EvaluationDataset:
        with open(path, "r", encoding="utf-8") as f:
            yaml_content = yaml.safe_load(f)

        questions = [EvaluationQuestion(**q) for q in yaml_content["questions"]]
        return cls(questions=questions)

    @classmethod
    def load_default(cls) -> EvaluationDataset:
        """Load EvaluationDataset from a default location."""
        path = os.path.join(EVALS_DATA_PATH, "questions.yaml")
        return EvaluationDataset.from_yaml(path)

    def to_examples(self) -> List[Dict[str, Any]]:
        examples = [
            {"inputs": {"question": example.question}, "outputs": {"answer": example.answer}}
            for example in self.questions
        ]
        return examples
