import unittest
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jarvis.agents import AgentManager
from jarvis.skills import TimeSkill, WebBrowserSkill, WikipediaSkill

sys.path.insert(0, str(Path(__file__).parent))
from mock_llm import MockLLMService


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MockLLMService()
        self.skills = [
            TimeSkill(),
            WebBrowserSkill(),
            WikipediaSkill(),
        ]
        self.agent = AgentManager(
            llm_service=self.mock_llm,
            skills=self.skills,
        )
    
    def test_chained_tool_calls(self):
        time_call = {
            "id": "call_1",
            "type": "function",
            "function": {
                "name": "get_current_time",
                "arguments": json.dumps({}),
            }
        }
        
        browser_call = {
            "id": "call_2",
            "type": "function",
            "function": {
                "name": "open_website",
                "arguments": json.dumps({"site": "youtube"}),
            }
        }
        
        self.mock_llm.add_response("", tool_calls=[time_call, browser_call])
        self.mock_llm.add_response("I've opened YouTube for you and the time is shown.")
        
        response = self.agent.process_message("Open YouTube and tell me the time")
        
        self.assertEqual(len(self.mock_llm.call_history), 2)
        
        history = self.agent.get_conversation_history()
        function_calls = [msg for msg in history if msg["role"] == "function"]
        self.assertEqual(len(function_calls), 2)
    
    def test_multiple_skills_triggered(self):
        time_call = {
            "id": "call_1",
            "type": "function",
            "function": {
                "name": "get_current_time",
                "arguments": json.dumps({}),
            }
        }
        
        self.mock_llm.add_response("", tool_calls=[time_call])
        
        wiki_call = {
            "id": "call_2",
            "type": "function",
            "function": {
                "name": "search_wikipedia",
                "arguments": json.dumps({"query": "Python programming", "sentences": 2}),
            }
        }
        
        self.mock_llm.add_response("", tool_calls=[wiki_call])
        self.mock_llm.add_response(
            "The current time is available and here's information about Python programming."
        )
        
        response = self.agent.process_message("What time is it and what is Python?")
        
        history = self.agent.get_conversation_history()
        function_calls = [msg for msg in history if msg["role"] == "function"]
        
        self.assertGreaterEqual(len(function_calls), 2)
    
    def test_contextual_conversation(self):
        self.mock_llm.add_response("Python is a high-level programming language.")
        response1 = self.agent.process_message("What is Python?")
        
        self.mock_llm.add_response("Python was created by Guido van Rossum in 1991.")
        response2 = self.agent.process_message("Who created it?")
        
        history = self.agent.get_conversation_history()
        
        self.assertIn("Python", response1)
        self.assertIn("Guido", response2)
        
        user_messages = [msg for msg in history if msg["role"] == "user"]
        self.assertEqual(len(user_messages), 2)


if __name__ == "__main__":
    unittest.main()
