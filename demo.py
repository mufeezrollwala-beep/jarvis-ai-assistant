#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jarvis.agents import AgentManager
from jarvis.skills import WikipediaSkill, WebBrowserSkill, TimeSkill, WeatherSkill
from tests.mock_llm import MockLLMService
import json


def demo_agent():
    print("=" * 60)
    print("Jarvis LLM Agent Integration Demo")
    print("=" * 60)
    print()
    
    mock_llm = MockLLMService()
    
    skills = [
        WikipediaSkill(),
        WebBrowserSkill(),
        TimeSkill(),
        WeatherSkill(api_key="demo_key", default_city="London"),
    ]
    
    agent = AgentManager(
        llm_service=mock_llm,
        skills=skills,
    )
    
    print("Available Skills:")
    for skill in skills:
        print(f"  - {skill.get_name()}: {skill.get_description()}")
    print()
    
    print("Demo 1: Simple conversation")
    print("-" * 60)
    mock_llm.add_response("Hello! I'm Jarvis. How may I assist you today?")
    response = agent.process_message("Hello")
    print(f"User: Hello")
    print(f"Jarvis: {response}")
    print()
    
    print("Demo 2: Single tool call (get time)")
    print("-" * 60)
    time_call = {
        "id": "call_1",
        "type": "function",
        "function": {
            "name": "get_current_time",
            "arguments": json.dumps({}),
        }
    }
    mock_llm.add_response("", tool_calls=[time_call])
    mock_llm.add_response("The current time is {time}.")
    response = agent.process_message("What time is it?")
    print(f"User: What time is it?")
    print(f"[Agent called tool: get_current_time]")
    print(f"Jarvis: {response}")
    print()
    
    print("Demo 3: Multiple tool calls in sequence")
    print("-" * 60)
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
    mock_llm.add_response("", tool_calls=[time_call, browser_call])
    mock_llm.add_response("I've opened YouTube for you. The current time is displayed above.")
    response = agent.process_message("Open YouTube and tell me the time")
    print(f"User: Open YouTube and tell me the time")
    print(f"[Agent called tools: get_current_time, open_website]")
    print(f"Jarvis: {response}")
    print()
    
    print("Demo 4: Multi-turn conversation with context")
    print("-" * 60)
    mock_llm.add_response("Python is a high-level, interpreted programming language known for its simplicity and readability.")
    response1 = agent.process_message("What is Python?")
    print(f"User: What is Python?")
    print(f"Jarvis: {response1}")
    print()
    
    mock_llm.add_response("Based on our previous discussion, Python was created by Guido van Rossum and first released in 1991.")
    response2 = agent.process_message("When was it created?")
    print(f"User: When was it created?")
    print(f"Jarvis: {response2}")
    print()
    
    print("Conversation History Summary:")
    history = agent.get_conversation_history()
    user_messages = [msg for msg in history if msg["role"] == "user"]
    assistant_messages = [msg for msg in history if msg["role"] == "assistant"]
    function_calls = [msg for msg in history if msg["role"] == "function"]
    print(f"  - User messages: {len(user_messages)}")
    print(f"  - Assistant messages: {len(assistant_messages)}")
    print(f"  - Function calls: {len(function_calls)}")
    print()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("Key Features Demonstrated:")
    print("  ✓ LLM-powered conversational agent")
    print("  ✓ Automatic tool/skill invocation")
    print("  ✓ Multi-turn context awareness")
    print("  ✓ Multiple skills triggered in sequence")
    print("  ✓ Configurable and extensible architecture")


if __name__ == "__main__":
    demo_agent()
