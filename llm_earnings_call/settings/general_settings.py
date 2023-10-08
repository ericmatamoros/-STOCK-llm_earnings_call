import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    fmp_api: str = os.getenv("FINANCIALMODELINGPREP_secret_key", "")
    openai_api: str = os.getenv("OPENAI_secret_key", "")