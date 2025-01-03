import os
from dataclasses import dataclass
import pytz


@dataclass
class Config:
    # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    OPENAI_MODEL = "gpt-4o"
    GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"
    # CLAUDE_MODEL = "anthropic/claude-3-sonnet:free"
    CLAUDE_MODEL = "anthropic/claude-3.5-sonnet"
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

    SUPPORTED_LANGUAGES = ["en", "ja"]
    DEFAULT_LANGUAGE = "ja"  # Changed from "en" to "ja"

    # Timezone settings
    DEFAULT_TIMEZONE = "Asia/Tokyo"
    SUPPORTED_TIMEZONES = [
        "Asia/Tokyo",
        "America/New_York",
        "America/Los_Angeles",
        "Europe/London",
        "Europe/Paris",
        "Asia/Shanghai",
        "Asia/Singapore",
        "Australia/Sydney",
        "Pacific/Auckland"
    ]

    # Chat context settings
    MAX_HISTORY_CHATS = 10
    MAX_CONTEXT_LENGTH = 4096  # Maximum token length for context
    MEMORY_SUMMARY_TOKENS = 150  # Length of conversation summaries
    CONTEXT_WINDOW_MESSAGES = 10  # Number of messages to keep in immediate context

    @staticmethod
    def get_openai_key():
        return os.getenv("OPENAI_API_KEY", "")

    @staticmethod
    def get_openrouter_key():
        return os.getenv("OPENROUTER_API_KEY", "")