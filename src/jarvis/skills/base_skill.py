from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class SkillResult:
    success: bool
    result: Any
    error: str = None


class BaseSkill(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        pass
    
    def to_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": self.get_description(),
                "parameters": self.get_parameters(),
            }
        }
