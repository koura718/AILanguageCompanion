import os
import time
import requests
from typing import List, Dict, Optional
from config import Config

class OpenRouterClient:
    def __init__(self):
        self.api_key = Config.get_openrouter_key()
        self.base_url = Config.OPENROUTER_API_BASE
        self.max_retries = 3
        self.retry_delay = 2  # Initial delay in seconds

    def create(self, messages: List[Dict[str, str]], model: str = None, response_format: Optional[Dict] = None) -> str:
        retries = 0
        last_error = None

        while retries < self.max_retries:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://replit.com",
                    "X-Title": "MyChatMe",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": model or Config.GEMINI_MODEL,
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

                # Print full response for debugging
                print(f"OpenRouter Status Code: {response.status_code}")
                print(f"OpenRouter Response: {response.text}\n")

                if response.status_code == 429:
                    wait_time = self.retry_delay * (2 ** retries)  # Exponential backoff
                    print(f"Rate limit exceeded. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    retries += 1
                    continue

                response.raise_for_status()
                response_data = response.json()

                if "error" in response_data:
                    raise ValueError(f"OpenRouter API returned error: {response_data['error']}")

                if not response_data.get('choices'):
                    raise ValueError("No choices in OpenRouter API response")

                if not response_data['choices'][0].get('message'):
                    raise ValueError("No message in OpenRouter API response choice")

                return response_data['choices'][0]['message']['content']

            except requests.exceptions.RequestException as e:
                print(f"OpenRouter Request Error: {str(e)}")
                last_error = e
                if "429" not in str(e):  # Only retry on rate limit errors
                    break
                retries += 1
                time.sleep(self.retry_delay * (2 ** retries))
            except ValueError as e:
                print(f"OpenRouter Value Error: {str(e)}")
                last_error = e
                if "rate" not in str(e).lower():  # Only retry on rate limit errors
                    break
                retries += 1
                time.sleep(self.retry_delay * (2 ** retries))
            except Exception as e:
                print(f"OpenRouter Unexpected Error: {str(e)}")
                last_error = e
                break

        # If all retries failed or other error occurred
        error_msg = str(last_error) if last_error else "Maximum retries exceeded"
        raise Exception(f"OpenRouter API error: {error_msg}")