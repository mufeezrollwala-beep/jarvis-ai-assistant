import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from memory_store import MemoryStore
from onboarding import OnboardingManager


def format_memory(memory: dict, index: int = None) -> str:
    prefix = f"[{index}] " if index is not None else ""
    text = memory.get('text', 'N/A')
    metadata = memory.get('metadata', {})
    
    output = f"{prefix}{text[:100]}"
    if len(text) > 100:
        output += "..."
    
    if metadata:
        category = metadata.get('category', 'N/A')
        timestamp = metadata.get('created_at', 'N/A')
        output += f"\n    Category: {category} | Created: {timestamp}"
    
    return output


def cmd_stats(memory_store: MemoryStore, args):
    stats = memory_store.get_stats()
    
    print("\n=== Memory Statistics ===")
    print(f"Short-term memories: {stats['short_term_count']}")
    print(f"Long-term memories: {stats['long_term_count']}")
    print(f"User preferences: {stats['preferences_count']}")
    print(f"Completed tasks: {stats['tasks_count']}")
    print(f"Persist directory: {stats['persist_directory']}")
    print()


def cmd_list_memories(memory_store: MemoryStore, args):
    if args.type == 'short':
        memories = memory_store.short_term.get_recent()
        print(f"\n=== Short-term Memories ({len(memories)}) ===")
        for i, memory in enumerate(memories, 1):
            timestamp = datetime.fromtimestamp(memory['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{i}] [{timestamp}] {memory['text']}")
        print()
    
    elif args.type == 'long':
        limit = args.limit if hasattr(args, 'limit') else 20
        memories = memory_store.long_term.get_all(limit=limit)
        print(f"\n=== Long-term Memories (showing {len(memories)}) ===")
        for i, memory in enumerate(memories, 1):
            print(format_memory(memory, i))
        print()
    
    elif args.type == 'all':
        print("\n=== All Memories ===")
        
        short_memories = memory_store.short_term.get_recent()
        print(f"\nShort-term ({len(short_memories)}):")
        for i, memory in enumerate(short_memories, 1):
            timestamp = datetime.fromtimestamp(memory['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  [{i}] [{timestamp}] {memory['text'][:80]}")
        
        long_memories = memory_store.long_term.get_all(limit=10)
        print(f"\nLong-term (showing {len(long_memories)}):")
        for i, memory in enumerate(long_memories, 1):
            print(f"  {format_memory(memory, i)}")
        print()


def cmd_search(memory_store: MemoryStore, args):
    results = memory_store.long_term.search(args.query, limit=args.limit)
    
    print(f"\n=== Search Results for '{args.query}' ===")
    if not results:
        print("No results found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result['text']}")
            if result.get('distance') is not None:
                print(f"    Relevance score: {1 - result['distance']:.3f}")
            if result.get('metadata'):
                print(f"    Metadata: {result['metadata']}")
    print()


def cmd_preferences(memory_store: MemoryStore, args):
    if args.action == 'list':
        prefs = memory_store.get_all_preferences()
        print("\n=== User Preferences ===")
        if not prefs:
            print("No preferences set.")
        else:
            for key, value in prefs.items():
                print(f"{key}: {value}")
        print()
    
    elif args.action == 'set':
        if not args.key or not args.value:
            print("Error: Both --key and --value are required for 'set' action")
            return
        memory_store.add_user_preference(args.key, args.value)
        print(f"✓ Preference set: {args.key} = {args.value}")
    
    elif args.action == 'get':
        if not args.key:
            print("Error: --key is required for 'get' action")
            return
        value = memory_store.get_user_preference(args.key)
        if value:
            print(f"{args.key}: {value}")
        else:
            print(f"No preference found for key: {args.key}")


def cmd_tasks(memory_store: MemoryStore, args):
    tasks = memory_store.get_recent_tasks(limit=args.limit)
    
    print(f"\n=== Recent Tasks ({len(tasks)}) ===")
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"\n[{task['task_id']}] {task['description']}")
            print(f"    Completed: {task['completed_at']}")
            if task['result']:
                print(f"    Result: {task['result']}")
    print()


def cmd_export(memory_store: MemoryStore, args):
    output_path = args.output or f"jarvis_memory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    result_path = memory_store.export_memories(output_path)
    print(f"✓ Memories exported to: {result_path}")


def cmd_import(memory_store: MemoryStore, args):
    if not Path(args.input).exists():
        print(f"Error: File not found: {args.input}")
        return
    
    if args.clear:
        confirm = input("This will clear all existing memories. Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Import cancelled.")
            return
    
    memory_store.import_memories(args.input, clear_existing=args.clear)
    print(f"✓ Memories imported from: {args.input}")


def cmd_prune(memory_store: MemoryStore, args):
    confirm = input(f"This will delete memories older than {args.days} days. Continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Prune cancelled.")
        return
    
    deleted_count = memory_store.prune_memories(days=args.days)
    print(f"✓ Pruned {deleted_count} old memories.")


def cmd_clear(memory_store: MemoryStore, args):
    confirm = input(f"This will clear {args.type} memory. Are you sure? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Clear cancelled.")
        return
    
    if args.type == 'short':
        memory_store.short_term.clear()
        print("✓ Short-term memory cleared.")
    elif args.type == 'long':
        memory_store.long_term.clear()
        print("✓ Long-term memory cleared.")
    elif args.type == 'all':
        memory_store.short_term.clear()
        memory_store.long_term.clear()
        print("✓ All memories cleared.")


def cmd_onboarding(memory_store: MemoryStore, args):
    onboarding = OnboardingManager(memory_store)
    
    if args.action == 'run':
        onboarding.run_onboarding()
    elif args.action == 'status':
        status = onboarding.check_onboarding_status()
        print("\n=== Onboarding Status ===")
        print(f"Has user name: {status['has_user_name']}")
        print(f"Has location: {status['has_location']}")
        print(f"Has seed knowledge: {status['has_seed_knowledge']}")
        print(f"Ready to use: {status['is_ready']}")
        print()
    elif args.action == 'quick':
        if not args.name:
            print("Error: --name is required for quick setup")
            return
        onboarding.quick_setup(args.name, args.location)


def main():
    parser = argparse.ArgumentParser(
        description='Jarvis Memory Management CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--memory-dir',
        default='./memory_data',
        help='Path to memory data directory (default: ./memory_data)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    subparsers.add_parser('stats', help='Show memory statistics')
    
    list_parser = subparsers.add_parser('list', help='List memories')
    list_parser.add_argument('type', choices=['short', 'long', 'all'], help='Type of memories to list')
    list_parser.add_argument('--limit', type=int, default=20, help='Limit number of results (default: 20)')
    
    search_parser = subparsers.add_parser('search', help='Search long-term memories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=5, help='Number of results (default: 5)')
    
    pref_parser = subparsers.add_parser('preferences', help='Manage user preferences')
    pref_parser.add_argument('action', choices=['list', 'set', 'get'], help='Action to perform')
    pref_parser.add_argument('--key', help='Preference key')
    pref_parser.add_argument('--value', help='Preference value')
    
    task_parser = subparsers.add_parser('tasks', help='View completed tasks')
    task_parser.add_argument('--limit', type=int, default=10, help='Number of tasks to show (default: 10)')
    
    export_parser = subparsers.add_parser('export', help='Export memories to JSON file')
    export_parser.add_argument('--output', help='Output file path')
    
    import_parser = subparsers.add_parser('import', help='Import memories from JSON file')
    import_parser.add_argument('input', help='Input file path')
    import_parser.add_argument('--clear', action='store_true', help='Clear existing memories before import')
    
    prune_parser = subparsers.add_parser('prune', help='Prune old memories')
    prune_parser.add_argument('--days', type=int, default=30, help='Delete memories older than N days (default: 30)')
    
    clear_parser = subparsers.add_parser('clear', help='Clear memories')
    clear_parser.add_argument('type', choices=['short', 'long', 'all'], help='Type of memory to clear')
    
    onboard_parser = subparsers.add_parser('onboarding', help='Manage onboarding')
    onboard_parser.add_argument('action', choices=['run', 'status', 'quick'], help='Onboarding action')
    onboard_parser.add_argument('--name', help='User name (for quick setup)')
    onboard_parser.add_argument('--location', help='User location (for quick setup)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    memory_store = MemoryStore(persist_directory=args.memory_dir)
    
    commands = {
        'stats': cmd_stats,
        'list': cmd_list_memories,
        'search': cmd_search,
        'preferences': cmd_preferences,
        'tasks': cmd_tasks,
        'export': cmd_export,
        'import': cmd_import,
        'prune': cmd_prune,
        'clear': cmd_clear,
        'onboarding': cmd_onboarding,
    }
    
    if args.command in commands:
        commands[args.command](memory_store, args)
    else:
        print(f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()
