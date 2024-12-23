import os
from typing import List, Dict
import openai
import requests
from config import Config

class LLMClient:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=Config.get_openai_key())
    
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
        headers = {
            "Authorization": f"Bearer {Config.get_openrouter_key()}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": Config.GEMINI_MODEL,
            "messages": messages
        }
        
        try:
            response = requests.post(
                f"{Config.OPENROUTER_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
