import os
import abc
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BaseLLM(abc.ABC):
    """Abstract base class for LLM providers."""
    
    @abc.abstractmethod
    def get_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get a completion from the LLM provider."""
        pass

    @abc.abstractmethod
    def get_streaming_completion(self, messages: List[Dict[str, str]], **kwargs):
        """Get a streaming completion from the LLM provider."""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI implementation of the LLM interface."""
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or passed directly.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def get_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        temperature = kwargs.get("temperature", 0.2)
        max_tokens = kwargs.get("max_tokens", 4000)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def get_streaming_completion(self, messages: List[Dict[str, str]], **kwargs):
        temperature = kwargs.get("temperature", 0.2)
        max_tokens = kwargs.get("max_tokens", 4000)
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"

class LLMFactory:
    """Factory for creating LLM instances."""
    
    @staticmethod
    def create_llm(provider: Optional[str] = None, **kwargs) -> BaseLLM:
        llm_provider = provider or os.environ.get("LLM_PROVIDER", "openai").lower()
        
        if llm_provider == "openai":
            return OpenAILLM(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
