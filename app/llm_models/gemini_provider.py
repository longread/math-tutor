"""Google Gemini LLM Provider implementation."""

from typing import Optional
import google.generativeai as genai
from PIL import Image
import io

from app.llm_models.base import BaseLLMProvider
from app.llm_models.config import SYSTEM_PROMPT, HINT_PROMPT


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider for math tutoring."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key. If None, will use GOOGLE_API_KEY env var.
        """
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Will use GOOGLE_API_KEY environment variable
            genai.configure()
        
        # Use Gemini 2.5 Flash and apply the system prompt at the model level
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        # Separate model for hints
        self.hint_model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=HINT_PROMPT
        )

    @property
    def name(self) -> str:
        return "Google Gemini"

    @property
    def supports_vision(self) -> bool:
        return True

    async def get_solution(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get math solution from Google Gemini."""
        if not problem_text and not image_data:
            raise ValueError("Either problem_text or image_data must be provided.")

        try:
            # Build content list for the user query
            user_content_parts = []
            
            if problem_text:
                user_content_parts.append(problem_text)
            
            if image_data:
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(image_data))
                user_content_parts.append(image)
            
            # Generate response
            response = self.model.generate_content(
                user_content_parts,
                generation_config={
                    'temperature': 0.7,
                }
            )
            
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None

    async def get_hint(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """Get hint for a math problem from Google Gemini."""
        if not problem_text and not image_data:
            raise ValueError("Either problem_text or image_data must be provided.")

        try:
            # Build content list for the user query
            user_content_parts = []
            
            if problem_text:
                user_content_parts.append(problem_text)
            
            if image_data:
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(image_data))
                user_content_parts.append(image)
            
            # Generate hint using hint model
            response = self.hint_model.generate_content(
                user_content_parts,
                generation_config={
                    'temperature': 0.7,
                }
            )
            
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API for hint: {e}")
            return None

