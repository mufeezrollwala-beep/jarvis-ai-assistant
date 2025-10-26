from typing import Dict, Any
import wikipedia
from .base_skill import BaseSkill, SkillResult


class WikipediaSkill(BaseSkill):
    def get_name(self) -> str:
        return "search_wikipedia"
    
    def get_description(self) -> str:
        return "Search Wikipedia for information on a given topic. Returns a brief summary."
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query or topic to look up on Wikipedia",
                },
                "sentences": {
                    "type": "integer",
                    "description": "Number of sentences to return in the summary (default: 2)",
                    "default": 2,
                }
            },
            "required": ["query"],
        }
    
    def execute(self, query: str, sentences: int = 2, **kwargs) -> SkillResult:
        try:
            result = wikipedia.summary(query, sentences=sentences)
            return SkillResult(success=True, result=result)
        except wikipedia.exceptions.DisambiguationError as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Multiple results found. Please be more specific. Options: {', '.join(e.options[:5])}"
            )
        except wikipedia.exceptions.PageError:
            return SkillResult(
                success=False,
                result=None,
                error=f"No Wikipedia page found for '{query}'"
            )
        except Exception as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Error searching Wikipedia: {str(e)}"
            )
