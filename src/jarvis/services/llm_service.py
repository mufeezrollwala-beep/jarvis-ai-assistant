from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    raw_response: Optional[Any] = None
    finish_reason: Optional[str] = None


class LLMService(ABC):
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        pass
