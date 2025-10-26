from typing import List, Dict, Any, Optional
import json
from .llm_service import LLMService, LLMResponse


class LocalModelService(LLMService):
    def __init__(
        self,
        model_path: str,
        context_size: int = 4096,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        gpu_layers: int = 35,
    ):
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError(
                "llama-cpp-python is required for local models. "
                "Install it with: pip install llama-cpp-python"
            )
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=context_size,
            n_gpu_layers=gpu_layers,
            verbose=False,
        )
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted += f"<|system|>\n{content}\n"
            elif role == "user":
                formatted += f"<|user|>\n{content}\n"
            elif role == "assistant":
                formatted += f"<|assistant|>\n{content}\n"
        formatted += "<|assistant|>\n"
        return formatted
    
    def _parse_tool_calls(self, content: str) -> tuple[str, Optional[List[Dict[str, Any]]]]:
        if "```tool_call" not in content:
            return content, None
        
        tool_calls = []
        parts = content.split("```tool_call")
        text_content = parts[0].strip()
        
        for i, part in enumerate(parts[1:], 1):
            if "```" in part:
                tool_json, remaining = part.split("```", 1)
                try:
                    tool_data = json.loads(tool_json.strip())
                    tool_calls.append({
                        "id": f"call_{i}",
                        "type": "function",
                        "function": {
                            "name": tool_data.get("name", ""),
                            "arguments": json.dumps(tool_data.get("arguments", {})),
                        }
                    })
                except json.JSONDecodeError:
                    pass
        
        return text_content, tool_calls if tool_calls else None
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        temp = temperature if temperature is not None else self.default_temperature
        max_tok = max_tokens if max_tokens is not None else self.default_max_tokens
        
        if tools:
            tools_desc = "\n\nAvailable tools:\n"
            for tool in tools:
                tools_desc += f"- {tool['function']['name']}: {tool['function']['description']}\n"
            tools_desc += "\nTo use a tool, format your response as:\n```tool_call\n{\"name\": \"tool_name\", \"arguments\": {\"arg1\": \"value1\"}}\n```"
            
            system_msg = None
            for msg in messages:
                if msg["role"] == "system":
                    system_msg = msg
                    break
            
            if system_msg:
                system_msg["content"] += tools_desc
            else:
                messages.insert(0, {"role": "system", "content": tools_desc})
        
        prompt = self._format_messages(messages)
        
        response = self.model(
            prompt,
            max_tokens=max_tok,
            temperature=temp,
            stop=["<|user|>", "<|system|>"],
        )
        
        content = response["choices"][0]["text"].strip()
        finish_reason = response["choices"][0].get("finish_reason", "stop")
        
        text_content, tool_calls = self._parse_tool_calls(content)
        
        return LLMResponse(
            content=text_content,
            tool_calls=tool_calls,
            raw_response=response,
            finish_reason=finish_reason,
        )
    
    def get_provider_name(self) -> str:
        return "local"
