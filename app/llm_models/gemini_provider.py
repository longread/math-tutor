"""Google Gemini LLM Provider implementation."""

from typing import Optional
import google.generativeai as genai
from PIL import Image
import io

from app.llm_models.base import BaseLLMProvider


# System prompt as defined in the PRD
SYSTEM_PROMPT = """You are an expert Math Tutoring AI designed to help students learn problem-solving logic. Your goal is to provide clear, step-by-step solutions that explain the "why" and "how," not just the result.

### OUTPUT FORMAT RULES
You must strictly follow this XML-style format for your response. Do not include markdown code blocks (like ```xml) around the output.

<step>
[Explain the first logical step here. Define variables or state the formula being used.]
</step>
<step>
[Perform the next calculation or logical deduction. Show intermediate work.]
</step>
... (add as many steps as necessary) ...
<answer>
[The final result]
</answer>

### CONTENT GUIDELINES
1. **Math Formatting:** Use LaTeX formatting for all mathematical expressions. Enclose inline math in single dollar signs (e.g., $x^2$) and block math in double dollar signs (e.g., $$ \\frac{a}{b} $$).
2. **Pedagogy:** Do not skip logical jumps. Write as if you are teaching a student who needs to see the intermediate work.
3. **Tone:** Be encouraging, professional, and concise.
4. **Non-Math Inputs:** If the user sends text that is not a math problem, politely decline inside a single <step> tag.
"""


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

