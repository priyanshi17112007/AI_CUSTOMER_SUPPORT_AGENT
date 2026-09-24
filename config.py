"""
config.py
=========
Central configuration manager for ResolveAI.
Safely loads environment variables, API keys, and model parameters.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

# System Metadata
PROJECT_NAME = "ResolveAI - Agentic Customer Support Resolution System"
VERSION = "1.0.0"
SYSTEM_AUTHOR = "Agentic AI Engineering Team"

# API Keys (Loaded strictly from environment; never hardcoded)
GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")

# Default Model Selection
DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.2"))

# Feature Flags
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_REASONING_STEPS: bool = True


def get_active_provider_info() -> dict:
    """Returns the detected LLM provider status based on available API keys."""
    providers = {
        "Gemini": bool(GEMINI_API_KEY),
        "OpenAI": bool(OPENAI_API_KEY),
        "Groq": bool(GROQ_API_KEY),
        "Deterministic Agent Mode (Autonomous Fallback)": True
    }
    return providers
