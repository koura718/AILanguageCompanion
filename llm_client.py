import os
from typing import List, Dict
import openai
from config import Config
from openrouter_client import OpenRouterClient

class LLMClient:
    def __init__(self):
        self.openai_client = None
        self.openrouter_client = None
        self.test_mode = False  # For testing error scenarios
        self.initialize_clients()

    def initialize_clients(self):
        """Initialize API clients with proper error handling"""
        try:
            if Config.get_openai_key():
                self.openai_client = openai.OpenAI(api_key=Config.get_openai_key())
            if Config.get_openrouter_key():
                self.openrouter_client = OpenRouterClient()
        except Exception as e:
            print(f"Error initializing API clients: {str(e)}")

    def set_test_mode(self, enabled: bool = True):
        """Enable or disable test mode for simulating errors"""
        self.test_mode = enabled

    def chat_openai(self, messages: List[Dict[str, str]]) -> str:
        """Send chat completion request to OpenAI API"""
        if not self.openai_client:
            raise Exception("OpenAI client not initialized. Please check your API key.")

        if self.test_mode:
            # Simulate different error scenarios for testing
            if messages and "test_error" in messages[-1].get("content", "").lower():
                error_type = messages[-1]["content"].lower()
                if "api_key" in error_type:
                    raise Exception("Invalid API key")
                elif "rate_limit" in error_type:
                    raise Exception("Rate limit exceeded")
                elif "network" in error_type:
                    raise Exception("Network connection error")

        try:
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def chat_gemini(self, messages: List[Dict[str, str]]) -> str:
        """Send chat completion request to Gemini via OpenRouter"""
        if not self.openrouter_client:
            raise Exception("OpenRouter client not initialized. Please check your API key.")

        try:
            return self.openrouter_client.create(
                messages,
                model=Config.GEMINI_MODEL
            )
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")

    def generate_context_summary(self, messages: List[Dict[str, str]]) -> str:
        """Generate a summary of the conversation context."""
        if not self.openai_client:
            print("OpenAI client not initialized. Skipping context summary.")
            return ""

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

    def chat_claude(self, messages: List[Dict[str, str]]) -> str:
        """Send chat completion request to Claude via OpenRouter"""
        if not self.openrouter_client:
            raise Exception("OpenRouter client not initialized. Please check your API key.")

        try:
            return self.openrouter_client.create(
                messages,
                model=Config.CLAUDE_MODEL
            )
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")