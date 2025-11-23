"""Factory for creating LLM provider instances."""

import os
from typing import Optional

from app.llm_models.base import BaseLLMProvider
from app.llm_models.openai_provider import OpenAIProvider
from app.llm_models.gemini_provider import GeminiProvider


def get_llm_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None
) -> BaseLLMProvider:
    """
    Get an LLM provider instance based on configuration.
    
    Args:
        provider_name: Name of the provider ('openai' or 'gemini'). 
                      If None, reads from LLM_PROVIDER env var.
                      Defaults to 'openai' if not set.
        api_key: API key for the provider. If None, provider will use 
                environment variables (OPENAI_API_KEY or GOOGLE_API_KEY).
    
    Returns:
        An instance of BaseLLMProvider
        
    Raises:
        ValueError: If provider_name is not supported
    """
    if provider_name is None:
        provider_name = os.getenv('LLM_PROVIDER', 'openai').lower()
    else:
        provider_name = provider_name.lower()
    
    if provider_name == 'openai':
        return OpenAIProvider(api_key=api_key)
    elif provider_name == 'gemini':
        return GeminiProvider(api_key=api_key)
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider_name}. "
            f"Supported providers: 'openai', 'gemini'"
        )

