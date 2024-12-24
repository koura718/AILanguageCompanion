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
            "Content-Type": "application/json",
            "HTTP-Referer": "https://replit.com",  # Required by OpenRouter
            "X-Title": "MyChatMe"  # Application name for OpenRouter
        }

        payload = {
            "model": Config.GEMINI_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        try:
            response = requests.post(
                f"{Config.OPENROUTER_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            response_data = response.json()

            # デバッグ用にレスポンスの構造をログ出力
            print(f"OpenRouter API Response: {response_data}")

            if "error" in response_data:
                raise Exception(f"OpenRouter API returned error: {response_data['error']}")

            if not response_data.get("choices"):
                raise Exception("No choices in OpenRouter API response")

            if not response_data["choices"][0].get("message"):
                raise Exception("No message in OpenRouter API response choice")

            return response_data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")