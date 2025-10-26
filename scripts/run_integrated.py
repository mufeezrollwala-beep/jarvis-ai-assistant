#!/usr/bin/env python3
import sys
import os
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ui.dashboard import JarvisDashboard
from ui.event_bus import EventBus


def assistant_thread_example():
    event_bus = EventBus()
    
    event_bus.add_conversation("System", "Jarvis assistant initialized")
    event_bus.add_task("init_001", "Initialize voice recognition", "completed")
    event_bus.add_memory("System Status", "All systems operational")
    
    print("Assistant thread: Ready to receive commands")
    print("Note: This is a placeholder. Integrate with jarvis.txt for real functionality.")


def main():
    print("=" * 70)
    print("  J.A.R.V.I.S - Integrated Mode")
    print("  Voice Assistant + Dashboard UI")
    print("=" * 70)
    print()
    
    print("Starting assistant thread...")
    thread = threading.Thread(target=assistant_thread_example, daemon=True)
    thread.start()
    
    print("Launching dashboard UI in mock mode...")
    print()
    
    dashboard = JarvisDashboard(mock_mode=True, headless_safe=False)
    exit_code = dashboard.run()
    
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nShutdown requested.")
        sys.exit(0)
