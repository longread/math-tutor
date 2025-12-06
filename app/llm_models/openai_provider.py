"""OpenAI LLM Provider implementation."""

import base64
from typing import Optional
from openai import OpenAI

from app.llm_models.base import BaseLLMProvider
from app.llm_models.config import SYSTEM_PROMPT, HINT_PROMPT


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider for math tutoring."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY env var.
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()

    @property
    def name(self) -> str:
        return "OpenAI GPT"

    @property
    def supports_vision(self) -> bool:
        return True

    async def get_solution(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get math solution from OpenAI GPT models."""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        user_content = []

        if problem_text:
            user_content.append({"type": "text", "text": problem_text})

        if image_data:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        
        if not user_content:
            raise ValueError("Either problem_text or image_data must be provided.")

        messages.append({"role": "user", "content": user_content})

        try:
            # Use gpt-4o for all requests (supports both text and vision)
            model = "gpt-4o"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None

    async def get_hint(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get hint for a math problem from OpenAI GPT models."""
        messages = [
            {"role": "system", "content": HINT_PROMPT}
        ]

        user_content = []

        if problem_text:
            user_content.append({"type": "text", "text": problem_text})

        if image_data:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        
        if not user_content:
            raise ValueError("Either problem_text or image_data must be provided.")

        messages.append({"role": "user", "content": user_content})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,  # Hints are shorter
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API for hint: {e}")
            return None

