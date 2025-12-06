"""Base interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    async def get_solution(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """
        Get a math solution from the LLM.
        
        Args:
            problem_text: The text of the math problem
            image_data: Image data in bytes (for vision-capable models)
            
        Returns:
            The LLM response as a string, or None if an error occurred
        """
        pass

    @abstractmethod
    async def get_hint(
        self, 
        problem_text: Optional[str] = None, 
        image_data: Optional[bytes] = None
    ) -> Optional[str]:
        """
        Get a hint for a math problem from the LLM.
        
        Args:
            problem_text: The text of the math problem
            image_data: Image data in bytes (for vision-capable models)
            
        Returns:
            The hint as a string, or None if an error occurred
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the provider."""
        pass

    @property
    @abstractmethod
    def supports_vision(self) -> bool:
        """Return whether this provider supports vision/image inputs."""
        pass

