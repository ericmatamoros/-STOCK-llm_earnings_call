"""
Interfaces
"""

from llm_earnings_call.interfaces.CFOSearcher import CFOSearcher
from llm_earnings_call.interfaces.ChatGPTPrompter import ChatGPTPrompter

__all__: list[str] = [
    "ChatGPTPrompter",
    "CFOSearcher"
]
