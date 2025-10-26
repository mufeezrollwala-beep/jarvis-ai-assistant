from typing import List, Dict, Any, Optional
import json
import logging
from ..services import LLMService
from ..skills import BaseSkill
from .prompts import JARVIS_SYSTEM_PROMPT, FALLBACK_RESPONSES, ERROR_RESPONSE


class AgentManager:
    def __init__(
        self,
        llm_service: LLMService,
        skills: List[BaseSkill],
        logger: Optional[logging.Logger] = None,
        max_iterations: int = 5,
    ):
        self.llm_service = llm_service
        self.skills = {skill.get_name(): skill for skill in skills}
        self.logger = logger or logging.getLogger(__name__)
        self.max_iterations = max_iterations
        self.conversation_history: List[Dict[str, str]] = []
        self._init_conversation()
    
    def _init_conversation(self):
        self.conversation_history = [
            {"role": "system", "content": JARVIS_SYSTEM_PROMPT}
        ]
    
    def reset_conversation(self):
        self._init_conversation()
        self.logger.info("Conversation history reset")
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [skill.to_tool_definition() for skill in self.skills.values()]
    
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        self.logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
        
        if tool_name not in self.skills:
            error_msg = f"Unknown tool: {tool_name}"
            self.logger.error(error_msg)
            return error_msg
        
        skill = self.skills[tool_name]
        result = skill.execute(**arguments)
        
        if result.success:
            self.logger.info(f"Tool {tool_name} executed successfully: {result.result}")
            return str(result.result)
        else:
            error_msg = f"Tool {tool_name} failed: {result.error}"
            self.logger.error(error_msg)
            return error_msg
    
    def process_message(self, user_message: str) -> str:
        self.logger.info(f"Processing user message: {user_message}")
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            self.logger.debug(f"Iteration {iteration}/{self.max_iterations}")
            
            try:
                tools = self.get_tool_definitions()
                response = self.llm_service.chat(
                    messages=self.conversation_history,
                    tools=tools if tools else None,
                )
                
                if response.tool_calls:
                    self.logger.info(f"LLM requested {len(response.tool_calls)} tool call(s)")
                    
                    if response.content:
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": response.content
                        })
                    
                    for tool_call in response.tool_calls:
                        tool_name = tool_call["function"]["name"]
                        try:
                            arguments = json.loads(tool_call["function"]["arguments"])
                        except json.JSONDecodeError:
                            arguments = {}
                        
                        tool_result = self._execute_tool(tool_name, arguments)
                        
                        self.conversation_history.append({
                            "role": "function",
                            "name": tool_name,
                            "content": tool_result
                        })
                    
                    continue
                
                if response.content:
                    self.logger.info(f"LLM response: {response.content}")
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    return response.content
                else:
                    self.logger.warning("Empty response from LLM")
                    return FALLBACK_RESPONSES[0]
                
            except Exception as e:
                self.logger.error(f"Error during iteration {iteration}: {str(e)}", exc_info=True)
                return ERROR_RESPONSE
        
        self.logger.warning(f"Reached maximum iterations ({self.max_iterations})")
        return "I apologize, but I need more time to process this request. Could you try rephrasing it?"
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history.copy()
