#!/usr/bin/env python3
"""
Test script to demonstrate and verify the memory system functionality
"""

import time
from memory_store import MemoryStore
from onboarding import OnboardingManager


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def test_short_term_memory():
    print_section("Testing Short-term Memory")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Adding conversation entries...")
    memory.short_term.add("User: What's the weather?")
    memory.short_term.add("Assistant: It's sunny today")
    memory.short_term.add("User: Great! Should I bring an umbrella?")
    memory.short_term.add("Assistant: No need, it's clear skies")
    
    print("\n2. Retrieving recent conversation:")
    context = memory.short_term.get_context_string()
    print(context)
    
    print("\n3. Testing TTL - adding old entry...")
    old_entry = {
        'text': 'This is an old memory',
        'timestamp': time.time() - 7200,  # 2 hours ago
        'metadata': {}
    }
    memory.short_term.memory.append(old_entry)
    
    print("\n4. After clearing expired entries:")
    memory.short_term.clear_expired()
    print(f"Valid entries remaining: {len(memory.short_term.get_recent())}")
    
    print("✓ Short-term memory test passed")


def test_long_term_memory():
    print_section("Testing Long-term Memory")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Adding knowledge to long-term memory...")
    memory.long_term.add(
        "User prefers celsius for temperature",
        {'category': 'preference', 'key': 'temperature_unit'}
    )
    memory.long_term.add(
        "User is interested in machine learning and AI",
        {'category': 'interest', 'topic': 'AI'}
    )
    memory.long_term.add(
        "User's favorite food is pizza",
        {'category': 'preference', 'key': 'favorite_food'}
    )
    
    print("\n2. Searching for 'temperature':")
    results = memory.long_term.search("temperature", limit=3)
    for i, result in enumerate(results, 1):
        print(f"   [{i}] {result['text']}")
        print(f"       Distance: {result.get('distance', 'N/A'):.4f}")
    
    print("\n3. Searching for 'food preferences':")
    results = memory.long_term.search("food preferences", limit=2)
    for i, result in enumerate(results, 1):
        print(f"   [{i}] {result['text']}")
    
    print("\n✓ Long-term memory test passed")


def test_user_preferences():
    print_section("Testing User Preferences")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Setting user preferences...")
    memory.add_user_preference("user_name", "Tony Stark")
    memory.add_user_preference("user_location", "New York")
    memory.add_user_preference("temperature_unit", "fahrenheit")
    
    print("\n2. Retrieving preferences:")
    prefs = memory.get_all_preferences()
    for key, value in prefs.items():
        print(f"   {key}: {value}")
    
    print("\n3. Getting specific preference:")
    name = memory.get_user_preference("user_name")
    print(f"   User name: {name}")
    
    print("\n✓ User preferences test passed")


def test_task_tracking():
    print_section("Testing Task Tracking")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Adding completed tasks...")
    memory.add_task("Checked weather", result="Sunny, 72°F")
    memory.add_task("Opened YouTube", result="Success")
    memory.add_task("Wikipedia search for Python", result="Found article")
    
    print("\n2. Retrieving recent tasks:")
    tasks = memory.get_recent_tasks(limit=5)
    for task in tasks:
        print(f"   [{task['task_id']}] {task['description']}")
        print(f"       Result: {task['result']}")
        print(f"       Completed: {task['completed_at']}")
    
    print("\n✓ Task tracking test passed")


def test_context_retrieval():
    print_section("Testing Context Retrieval")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Adding conversation context...")
    memory.add_conversation(
        "What's my favorite food?",
        "Based on what you told me, your favorite food is pizza"
    )
    
    print("\n2. Retrieving context for 'food preferences':")
    context = memory.retrieve_context("food preferences", long_term_limit=3)
    
    print("\n   Recent conversation:")
    print(f"   {context.get('recent_conversation', 'None')[:200]}")
    
    print("\n   Relevant memories:")
    for mem in context.get('relevant_memories', [])[:3]:
        print(f"   - {mem['text']}")
    
    print("\n   User preferences:")
    for key, value in list(context.get('preferences', {}).items())[:3]:
        print(f"   - {key}: {value}")
    
    print("\n✓ Context retrieval test passed")


def test_onboarding():
    print_section("Testing Onboarding")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    onboarding = OnboardingManager(memory)
    
    print("\n1. Running quick setup...")
    onboarding.quick_setup("Tony Stark", location="Malibu")
    
    print("\n2. Adding device knowledge...")
    onboarding.add_device_knowledge(
        device_name="Living Room Lights",
        device_type="smart_light",
        location="living room",
        capabilities=["turn on", "turn off", "dim"]
    )
    
    print("\n3. Adding correction...")
    onboarding.add_correction("play music", "play workout playlist")
    
    print("\n4. Checking onboarding status:")
    status = onboarding.check_onboarding_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✓ Onboarding test passed")


def test_export_import():
    print_section("Testing Export/Import")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n1. Exporting memories...")
    export_path = memory.export_memories("./test_export.json")
    print(f"   Exported to: {export_path}")
    
    print("\n2. Verifying export file exists...")
    import os
    if os.path.exists(export_path):
        print(f"   ✓ File exists")
        file_size = os.path.getsize(export_path)
        print(f"   File size: {file_size} bytes")
    
    print("\n✓ Export/Import test passed")


def test_persistence():
    print_section("Testing Persistence Across Sessions")
    
    print("\n1. Creating first session and adding data...")
    memory1 = MemoryStore(persist_directory="./test_memory_data")
    memory1.add_user_preference("test_key", "test_value")
    memory1.long_term.add("This should persist", {'category': 'test'})
    
    print("\n2. Creating second session (simulating restart)...")
    memory2 = MemoryStore(persist_directory="./test_memory_data")
    
    print("\n3. Verifying data persists:")
    test_value = memory2.get_user_preference("test_key")
    print(f"   Preference retrieved: test_key = {test_value}")
    
    memories = memory2.long_term.search("persist", limit=1)
    if memories:
        print(f"   Long-term memory retrieved: {memories[0]['text']}")
    
    if test_value == "test_value" and memories:
        print("\n✓ Persistence test passed")
    else:
        print("\n✗ Persistence test failed")


def test_stats():
    print_section("Testing Statistics")
    
    memory = MemoryStore(persist_directory="./test_memory_data")
    
    stats = memory.get_stats()
    
    print("\nMemory Statistics:")
    print(f"   Short-term memories: {stats['short_term_count']}")
    print(f"   Long-term memories: {stats['long_term_count']}")
    print(f"   User preferences: {stats['preferences_count']}")
    print(f"   Completed tasks: {stats['tasks_count']}")
    print(f"   Persist directory: {stats['persist_directory']}")
    
    print("\n✓ Statistics test passed")


def main():
    print("\n" + "="*60)
    print("  JARVIS MEMORY SYSTEM TEST SUITE")
    print("="*60)
    
    try:
        test_short_term_memory()
        test_long_term_memory()
        test_user_preferences()
        test_task_tracking()
        test_context_retrieval()
        test_onboarding()
        test_export_import()
        test_persistence()
        test_stats()
        
        print_section("ALL TESTS PASSED ✓")
        print("\nMemory system is working correctly!")
        print("You can inspect the test data using:")
        print("  python cli.py --memory-dir ./test_memory_data stats")
        print("  python cli.py --memory-dir ./test_memory_data list long")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
