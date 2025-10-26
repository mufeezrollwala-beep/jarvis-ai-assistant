import unittest
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jarvis.agents import AgentManager
from jarvis.skills import TimeSkill, WikipediaSkill

sys.path.insert(0, str(Path(__file__).parent))
from mock_llm import MockLLMService


class TestAgentManager(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MockLLMService()
        self.skills = [TimeSkill(), WikipediaSkill()]
        self.agent = AgentManager(
            llm_service=self.mock_llm,
            skills=self.skills,
        )
    
    def test_initialization(self):
        self.assertEqual(len(self.agent.skills), 2)
        self.assertIn("get_current_time", self.agent.skills)
        self.assertIn("search_wikipedia", self.agent.skills)
    
    def test_get_tool_definitions(self):
        tools = self.agent.get_tool_definitions()
        self.assertEqual(len(tools), 2)
        self.assertTrue(all(tool["type"] == "function" for tool in tools))
    
    def test_simple_conversation(self):
        self.mock_llm.add_response("Hello! How can I assist you today?")
        
        response = self.agent.process_message("Hi")
        
        self.assertEqual(response, "Hello! How can I assist you today?")
        self.assertEqual(len(self.mock_llm.call_history), 1)
    
    def test_tool_calling_flow(self):
        tool_call = {
            "id": "call_1",
            "type": "function",
            "function": {
                "name": "get_current_time",
                "arguments": json.dumps({}),
            }
        }
        
        self.mock_llm.add_response("", tool_calls=[tool_call])
        self.mock_llm.add_response("The current time is 14:30:00")
        
        response = self.agent.process_message("What time is it?")
        
        self.assertEqual(len(self.mock_llm.call_history), 2)
        self.assertIn("time", response.lower())
    
    def test_multi_turn_conversation(self):
        self.mock_llm.add_response("Hello! I'm here to help.")
        response1 = self.agent.process_message("Hi")
        
        self.mock_llm.add_response("I can help you with many things!")
        response2 = self.agent.process_message("What can you do?")
        
        history = self.agent.get_conversation_history()
        user_messages = [msg for msg in history if msg["role"] == "user"]
        self.assertEqual(len(user_messages), 2)
    
    def test_reset_conversation(self):
        self.mock_llm.add_response("Hello!")
        self.agent.process_message("Hi")
        
        self.agent.reset_conversation()
        
        history = self.agent.get_conversation_history()
        user_messages = [msg for msg in history if msg["role"] == "user"]
        self.assertEqual(len(user_messages), 0)


if __name__ == "__main__":
    unittest.main()
