import os
import requests
from typing import List, Dict, Optional
from config import Config

class OpenRouterClient:
    def __init__(self):
        self.api_key = Config.get_openrouter_key()
        self.base_url = Config.OPENROUTER_API_BASE

    def create(self, messages: List[Dict[str, str]], response_format: Optional[Dict] = None) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://replit.com",
                "X-Title": "MyChatMe",
                "Content-Type": "application/json"
            }

            data = {
                "model": Config.GEMINI_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }

            if response_format:
                data["response_format"] = response_format

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()

            response_data = response.json()
            if not response_data.get('choices') or not response_data['choices'][0].get('message'):
                raise ValueError(f"Invalid response format from OpenRouter: {response_data}")

            return response_data['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"OpenRouter API response error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error in OpenRouter API call: {str(e)}")
