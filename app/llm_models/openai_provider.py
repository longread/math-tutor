"""OpenAI LLM Provider implementation."""

import base64
from typing import Optional
from openai import OpenAI

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

