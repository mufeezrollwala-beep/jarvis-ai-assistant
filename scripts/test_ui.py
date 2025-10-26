#!/usr/bin/env python3
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ui.event_bus import EventBus


def test_event_bus():
    print("Testing Event Bus...")
    
    event_bus = EventBus()
    
    event_bus.add_conversation("User", "Hello Jarvis")
    event_bus.add_conversation("Jarvis", "Hello, sir. How can I assist you?")
    
    event_bus.add_task("test_001", "Test task", "running")
    
    event_bus.update_metrics({
        'cpu': 45.5,
        'memory': 62.3,
        'disk': 55.0,
        'network_in': 1024.5,
        'network_out': 512.3
    })
    
    event_bus.add_memory("Test Key", "Test Value")
    
    event_bus.update_audio_waveform([0.1, 0.2, 0.3, 0.2, 0.1])
    
    print("  - Conversation history:", len(event_bus.get_conversation_history()))
    print("  - Tasks:", len(event_bus.get_tasks()))
    print("  - Memory items:", len(event_bus.get_memory_items()))
    
    print("✓ Event Bus test passed!\n")


def test_ui_imports():
    print("Testing UI module imports...")
    
    try:
        from ui.dashboard import JarvisDashboard, DashboardBridge
        from ui.mock_data import MockDataGenerator
        print("✓ All imports successful!\n")
    except Exception as e:
        print(f"✗ Import failed: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    print("=" * 70)
    print("  J.A.R.V.I.S Dashboard - Unit Tests")
    print("=" * 70)
    print()
    
    test_ui_imports()
    test_event_bus()
    
    print("=" * 70)
    print("  All tests passed!")
    print("=" * 70)
