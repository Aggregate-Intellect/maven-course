import os
from typing import Final

EVALS_PATH: Final[str] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EVALS_DATA_PATH: Final[str] = os.path.join(EVALS_PATH, "data")
EVALS_PROMPTS_PATH: Final[str] = os.path.join(EVALS_DATA_PATH, "prompts")
