import os
from typing import List, Dict
import openai
from config import Config
from openrouter_client import OpenRouterClient

class LLMClient:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=Config.get_openai_key())
        self.openrouter_client = OpenRouterClient()

    def chat_openai(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def chat_gemini(self, messages: List[Dict[str, str]]) -> str:
        try:
            return self.openrouter_client.create(messages)
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")

    def generate_context_summary(self, messages: List[Dict[str, str]]) -> str:
        """Generate a summary of the conversation context."""
        try:
            summary_prompt = {
                "role": "system",
                "content": (
                    "Summarize the key points of this conversation in a concise way. "
                    "Focus on the main topics and important details. "
                    f"Keep the summary within {Config.MEMORY_SUMMARY_TOKENS} tokens."
                )
            }

            # Create a list of messages for summarization
            summary_messages = [summary_prompt] + messages[-Config.CONTEXT_WINDOW_MESSAGES:]

            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=summary_messages,
                max_tokens=Config.MEMORY_SUMMARY_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed to generate context summary: {str(e)}")
            return ""  # Return empty string if summarization fails