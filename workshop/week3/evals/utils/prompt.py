from __future__ import annotations

import os
from typing import Any, Dict, List

from pydantic import BaseModel

from .path import EVALS_PROMPTS_PATH


class Prompt(BaseModel):
    system_prompt: str
    user_prompt_template: str

    @staticmethod
    def load_prompt(filename: str) -> str:
        path = os.path.join(EVALS_PROMPTS_PATH, filename)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def default_eval_prompt(cls) -> Prompt:
        return cls(
            system_prompt=cls.load_prompt("llm_judge_system_prompt.md"),
            user_prompt_template=cls.load_prompt("llm_judge_user_prompt_template.md"),
        )

    def to_messages(self, **kwargs: Any) -> List[Dict[str, Any]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt_template.format(**kwargs)},
        ]
