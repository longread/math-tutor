"""AI Service - Provides math tutoring solutions using configurable LLM providers."""

from app.llm_models import get_llm_provider

# Initialize the LLM provider based on LLM_PROVIDER environment variable
# Defaults to OpenAI if not set. Can be 'openai', 'gemini', or 'ollama'
llm_provider = get_llm_provider()


async def get_math_solution(problem_text: str = None, image_data: bytes = None):
    """
    Get a math solution from the configured LLM provider.
    
    Args:
        problem_text: The text of the math problem
        image_data: Image data in bytes (for vision-capable models)
        
    Returns:
        The LLM response as a string, or None if an error occurred
    """
    return await llm_provider.get_solution(
        problem_text=problem_text,
        image_data=image_data
    )


async def get_math_hint(problem_text: str = None, image_data: bytes = None):
    """
    Get a hint for a math problem from the configured LLM provider.
    
    Args:
        problem_text: The text of the math problem
        image_data: Image data in bytes (for vision-capable models)
        
    Returns:
        The hint as a string, or None if an error occurred
    """
    return await llm_provider.get_hint(
        problem_text=problem_text,
        image_data=image_data
    )
