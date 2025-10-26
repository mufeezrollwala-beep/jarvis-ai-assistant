from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from .llm_service import LLMService, LLMResponse


class AzureOpenAIService(LLMService):
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment_name: str,
        api_version: str = "2024-02-15-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
        )
        self.deployment_name = deployment_name
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        temp = temperature if temperature is not None else self.default_temperature
        max_tok = max_tokens if max_tokens is not None else self.default_max_tokens
        
        kwargs = {
            "model": self.deployment_name,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tok,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        response = self.client.chat.completions.create(**kwargs)
        
        message = response.choices[0].message
        content = message.content or ""
        
        tool_calls = None
        if hasattr(message, 'tool_calls') and message.tool_calls:
            tool_calls = []
            for tool_call in message.tool_calls:
                tool_calls.append({
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    }
                })
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason,
        )
    
    def get_provider_name(self) -> str:
        return "azure"
