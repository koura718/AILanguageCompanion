import os
from dataclasses import dataclass

@dataclass
class Config:
    # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    OPENAI_MODEL = "gpt-4o"
    GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
    
    SUPPORTED_LANGUAGES = ["en", "ja"]
    DEFAULT_LANGUAGE = "en"
    
    MAX_HISTORY_CHATS = 10
    
    @staticmethod
    def get_openai_key():
        return os.getenv("OPENAI_API_KEY", "")
    
    @staticmethod
    def get_openrouter_key():
        return os.getenv("OPENROUTER_API_KEY", "")
