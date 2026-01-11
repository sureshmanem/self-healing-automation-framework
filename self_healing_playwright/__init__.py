"""
Self-Healing Playwright Framework
A Python framework that adds self-healing capabilities to Playwright test automation using Azure OpenAI.
"""

from .openai_healer import OpenAIHealer
from .safe_page import SafePage

__version__ = "1.0.0"
__all__ = ["OpenAIHealer", "SafePage"]
