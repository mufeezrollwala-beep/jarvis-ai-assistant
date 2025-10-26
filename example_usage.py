#!/usr/bin/env python3
"""
Example usage of the Jarvis memory system without voice interface.
This demonstrates the memory capabilities programmatically.
"""

from memory_store import MemoryStore
from onboarding import OnboardingManager


def example_basic_usage():
    print("\n=== Basic Memory Usage Example ===\n")
    
    memory = MemoryStore(persist_directory="./example_memory_data")
    
    print("1. Setting up user profile...")
    memory.add_user_preference("user_name", "Tony Stark")
    memory.add_user_preference("user_location", "Malibu")
    memory.add_user_preference("temperature_unit", "fahrenheit")
    print("   ✓ User preferences saved")
    
    print("\n2. Simulating a conversation...")
    memory.add_conversation(
        "What's the weather like?",
        "It's 75°F and sunny in Malibu"
    )
    memory.add_conversation(
        "Should I go to the beach?",
        "Perfect weather for the beach!"
    )
    print("   ✓ Conversation stored")
    
    print("\n3. Adding explicit memories...")
    memory.long_term.add(
        "User prefers mornings for exercising",
        {'category': 'preference', 'activity': 'exercise'}
    )
    memory.long_term.add(
        "User's favorite coffee is espresso",
        {'category': 'preference', 'item': 'coffee'}
    )
    print("   ✓ Memories saved")
    
    print("\n4. Searching memories...")
    results = memory.long_term.search("exercise routine", limit=3)
    print(f"   Found {len(results)} relevant memories:")
    for result in results:
        print(f"   - {result['text']}")
    
    print("\n5. Retrieving full context for 'morning routine'...")
    context = memory.retrieve_context("morning routine")
    print(f"   Recent conversations: {len(context['recent_conversation'].split('\\n'))} turns")
    print(f"   Relevant memories: {len(context['relevant_memories'])} items")
    print(f"   User preferences: {len(context['preferences'])} items")
    
    return memory


def example_onboarding():
    print("\n\n=== Onboarding Example ===\n")
    
    memory = MemoryStore(persist_directory="./example_memory_data")
    onboarding = OnboardingManager(memory)
    
    print("1. Quick setup for new user...")
    onboarding.quick_setup("Pepper Potts", location="New York")
    print("   ✓ User profile created")
    
    print("\n2. Adding smart home devices...")
    onboarding.add_device_knowledge(
        device_name="Bedroom Thermostat",
        device_type="thermostat",
        location="bedroom",
        capabilities=["set temperature", "get temperature", "set schedule"]
    )
    onboarding.add_device_knowledge(
        device_name="Kitchen Lights",
        device_type="smart_light",
        location="kitchen",
        capabilities=["turn on", "turn off", "dim", "brighten"]
    )
    print("   ✓ Device knowledge added")
    
    print("\n3. Adding user corrections...")
    onboarding.add_correction("play music", "play classical music playlist")
    onboarding.add_correction("news", "read tech news briefing")
    print("   ✓ Corrections learned")
    
    return memory


def example_task_tracking():
    print("\n\n=== Task Tracking Example ===\n")
    
    memory = MemoryStore(persist_directory="./example_memory_data")
    
    print("1. Logging completed tasks...")
    memory.add_task("Checked morning weather", result="Sunny, 72°F")
    memory.add_task("Opened calendar", result="3 meetings scheduled")
    memory.add_task("Set reminder for 3 PM", result="Reminder set successfully")
    print("   ✓ Tasks logged")
    
    print("\n2. Retrieving recent tasks...")
    tasks = memory.get_recent_tasks(limit=5)
    for task in tasks:
        print(f"   [{task['task_id']}] {task['description']}")
        if task['result']:
            print(f"       Result: {task['result']}")
    
    return memory


def example_memory_search():
    print("\n\n=== Memory Search Example ===\n")
    
    memory = MemoryStore(persist_directory="./example_memory_data")
    
    queries = [
        "What does the user prefer for breakfast?",
        "Tell me about the user's exercise habits",
        "What smart home devices are available?",
        "User's location and weather preferences"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = memory.long_term.search(query, limit=2)
        if results:
            print("   Relevant memories:")
            for result in results:
                print(f"   - {result['text']}")
                print(f"     (relevance: {1 - result.get('distance', 0):.2f})")
        else:
            print("   No relevant memories found")
    
    return memory


def example_conversation_context():
    print("\n\n=== Conversation Context Example ===\n")
    
    memory = MemoryStore(persist_directory="./example_memory_data")
    
    print("Simulating a multi-turn conversation with context:\n")
    
    conversation_turns = [
        ("What's my schedule today?", "You have 3 meetings scheduled"),
        ("When is the first one?", "Your first meeting is at 10 AM"),
        ("Set a reminder 10 minutes before", "Reminder set for 9:50 AM"),
        ("What's the weather?", "It's sunny and 72°F in New York"),
        ("Should I take a jacket?", "It's warm, you probably won't need one"),
    ]
    
    for user_query, assistant_response in conversation_turns:
        memory.add_conversation(user_query, assistant_response)
        print(f"User: {user_query}")
        print(f"Jarvis: {assistant_response}\n")
    
    print("\nShort-term conversation context:")
    context_str = memory.short_term.get_context_string(limit=5)
    print(context_str)
    
    return memory


def show_statistics(memory):
    print("\n\n=== Memory Statistics ===\n")
    
    stats = memory.get_stats()
    print(f"Short-term memories: {stats['short_term_count']}")
    print(f"Long-term memories: {stats['long_term_count']}")
    print(f"User preferences: {stats['preferences_count']}")
    print(f"Completed tasks: {stats['tasks_count']}")
    print(f"\nData stored in: {stats['persist_directory']}")


def main():
    print("="*70)
    print(" JARVIS MEMORY SYSTEM - EXAMPLE USAGE")
    print("="*70)
    
    memory = example_basic_usage()
    memory = example_onboarding()
    memory = example_task_tracking()
    memory = example_memory_search()
    memory = example_conversation_context()
    show_statistics(memory)
    
    print("\n" + "="*70)
    print(" Examples Complete!")
    print("="*70)
    print("\nYou can now inspect the memory data using the CLI:")
    print("  python cli.py --memory-dir ./example_memory_data stats")
    print("  python cli.py --memory-dir ./example_memory_data list long")
    print("  python cli.py --memory-dir ./example_memory_data search 'coffee'")
    print("  python cli.py --memory-dir ./example_memory_data preferences list")
    print("\nOr export the memories:")
    print("  python cli.py --memory-dir ./example_memory_data export --output example_backup.json")
    print()


if __name__ == '__main__':
    main()
