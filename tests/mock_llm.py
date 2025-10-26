from typing import List, Dict, Any, Optional
import json
from src.jarvis.services import LLMService, LLMResponse


class MockLLMService(LLMService):
    def __init__(self):
        self.responses = []
        self.call_history = []
    
    def add_response(self, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None):
        self.responses.append({
            "content": content,
            "tool_calls": tool_calls,
        })
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        self.call_history.append({
            "messages": messages.copy(),
            "tools": tools,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })
        
        if not self.responses:
            return LLMResponse(
                content="Mock response",
                tool_calls=None,
                finish_reason="stop",
            )
        
        response = self.responses.pop(0)
        return LLMResponse(
            content=response["content"],
            tool_calls=response["tool_calls"],
            finish_reason="stop",
        )
    
    def get_provider_name(self) -> str:
        return "mock"
