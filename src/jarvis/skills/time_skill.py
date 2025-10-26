from typing import Dict, Any
import datetime
from .base_skill import BaseSkill, SkillResult


class TimeSkill(BaseSkill):
    def get_name(self) -> str:
        return "get_current_time"
    
    def get_description(self) -> str:
        return "Get the current time in HH:MM:SS format"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }
    
    def execute(self, **kwargs) -> SkillResult:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            return SkillResult(success=True, result=current_time)
        except Exception as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Error getting time: {str(e)}"
            )
