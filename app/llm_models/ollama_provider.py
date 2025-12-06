"""Ollama LLM Provider implementation."""

from typing import Optional
import httpx
import json
import base64

from app.llm_models.base import BaseLLMProvider
from app.llm_models.config import SYSTEM_PROMPT, HINT_PROMPT


class OllamaProvider(BaseLLMProvider):
    """Ollama provider for math tutoring (local models)."""

    def __init__(
        self, 
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama API base URL. Defaults to http://127.0.0.1:11434
            model: Model name to use. Defaults to 'llama3.2-vision' for vision support,
                   or set via OLLAMA_MODEL env var.
        """
        import os
        
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
        self.model_name = model or os.getenv('OLLAMA_MODEL', 'llama3.2-vision')
        self.client = httpx.AsyncClient(timeout=1200.0)  # Ollama can be slow on CPU

    @property
    def name(self) -> str:
        return f"Ollama ({self.model_name})"

    @property
    def supports_vision(self) -> bool:
        # Vision models in Ollama include llama3.2-vision, llava, bakllava, etc.
        vision_keywords = ['vision', 'llava', 'bakllava', 'minicpm']
        return any(keyword in self.model_name.lower() for keyword in vision_keywords)

    async def get_solution(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get math solution from Ollama."""
        if not problem_text and not image_data:
            raise ValueError("Either problem_text or image_data must be provided.")

        try:
            # Build the messages for the chat API
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
            
            # Build user message content
            user_content = ""
            if problem_text:
                user_content = problem_text
            
            user_message = {
                "role": "user",
                "content": user_content or "Solve this math problem from the image."
            }
            
            # Add image if provided
            if image_data:
                # Ollama expects base64-encoded images
                base64_image = base64.b64encode(image_data).decode('utf-8')
                user_message["images"] = [base64_image]
            
            messages.append(user_message)
            
            # Call Ollama API
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                }
            }
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the assistant's message
            if "message" in result and "content" in result["message"]:
                return result["message"]["content"]
            else:
                print(f"Unexpected Ollama response format: {result}")
                return None
                
        except httpx.HTTPError as e:
            print(f"HTTP error calling Ollama API: {e}")
            return None
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return None

    async def get_hint(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get hint for a math problem from Ollama."""
        if not problem_text and not image_data:
            raise ValueError("Either problem_text or image_data must be provided.")

        try:
            # Build the messages for the chat API
            messages = [
                {
                    "role": "system",
                    "content": HINT_PROMPT
                }
            ]
            
            # Build user message content
            user_content = ""
            if problem_text:
                user_content = problem_text
            
            user_message = {
                "role": "user",
                "content": user_content or "Provide a hint for this math problem from the image."
            }
            
            # Add image if provided
            if image_data:
                # Ollama expects base64-encoded images
                base64_image = base64.b64encode(image_data).decode('utf-8')
                user_message["images"] = [base64_image]
            
            messages.append(user_message)
            
            # Call Ollama API
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                }
            }
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the assistant's message
            if "message" in result and "content" in result["message"]:
                return result["message"]["content"]
            else:
                print(f"Unexpected Ollama response format: {result}")
                return None
                
        except httpx.HTTPError as e:
            print(f"HTTP error calling Ollama API for hint: {e}")
            return None
        except Exception as e:
            print(f"Error calling Ollama API for hint: {e}")
            return None

