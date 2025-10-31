#!/usr/bin/env python3
"""
Example demonstrating concurrent task execution while handling new commands.

This script shows how Jarvis can:
1. Execute multiple tasks simultaneously
2. Accept new commands while tasks are running
3. Monitor and report task status
4. Cancel tasks on demand
"""

import asyncio
from src.task_manager import TaskManager, TaskState
from src.background_actions import reminder_timer, download_file


async def simulate_user_commands(manager):
    """Simulates user issuing commands while tasks are running."""
    
    print("\n" + "="*60)
    print("Simulating User Commands")
    print("="*60)
    
    # User creates first batch of tasks
    print("\n[User Command]: Create 3 reminder tasks")
    
    async def reminder_5s(task):
        return await reminder_timer(task, 5, "5 second timer done")
    
    async def reminder_10s(task):
        return await reminder_timer(task, 10, "10 second timer done")
    
    async def reminder_15s(task):
        return await reminder_timer(task, 15, "15 second timer done")
    
    task1 = manager.create_task("Reminder 5s", reminder_5s, priority=1)
    task2 = manager.create_task("Reminder 10s", reminder_10s, priority=2)
    task3 = manager.create_task("Reminder 15s", reminder_15s, priority=3)
    print(f"✓ Created tasks: {task1[:8]}, {task2[:8]}, {task3[:8]}")
    
    # Wait a bit, then add more tasks
    await asyncio.sleep(2)
    
    print("\n[User Command]: Check task status")
    stats = manager.get_stats()
    print(f"Status: {stats['running']} running, {stats['pending']} pending, {stats['completed']} completed")
    
    # Add another task while others are running
    await asyncio.sleep(2)
    
    print("\n[User Command]: Start download task")
    
    async def download_task(task):
        return await download_file(
            task, 
            "https://httpbin.org/bytes/5120",
            "./downloads/example_file.bin"
        )
    
    try:
        task4 = manager.create_task("Download", download_task, priority=10)
        print(f"✓ Created download task: {task4[:8]}")
    except:
        print("⚠ Download task creation skipped (network unavailable)")
        task4 = None
    
    # Check status again
    await asyncio.sleep(3)
    
    print("\n[User Command]: List all tasks")
    tasks = manager.list_tasks()
    print(f"\nTotal tasks: {len(tasks)}")
    for task in tasks:
        print(f"  - {task.name}: {task.state.value} ({task.progress:.1f}%)")
    
    # Add a task and immediately check if we can cancel one
    await asyncio.sleep(2)
    
    print("\n[User Command]: Try to cancel a task")
    running_tasks = manager.list_tasks(TaskState.RUNNING)
    if running_tasks:
        to_cancel = running_tasks[0]
        if manager.cancel_task(to_cancel.id):
            print(f"✓ Cancelled task: {to_cancel.name}")
        else:
            print(f"✗ Could not cancel task: {to_cancel.name}")
    else:
        print("No running tasks to cancel")
    
    # Final status check
    await asyncio.sleep(5)
    
    print("\n[User Command]: Final status")
    final_stats = manager.get_stats()
    print(f"Final Status:")
    print(f"  Completed: {final_stats['completed']}")
    print(f"  Failed: {final_stats['failed']}")
    print(f"  Cancelled: {final_stats['cancelled']}")
    
    # Show completed task results
    completed_tasks = manager.list_tasks(TaskState.COMPLETED)
    if completed_tasks:
        print(f"\nCompleted Tasks:")
        for task in completed_tasks:
            print(f"  ✓ {task.name}")
            if task.result:
                print(f"    Result: {task.result}")


async def main():
    """Main execution demonstrating concurrent operations."""
    
    print("="*60)
    print("Jarvis Concurrent Task Example")
    print("="*60)
    print("\nThis example demonstrates:")
    print("1. Running multiple tasks simultaneously")
    print("2. Accepting commands while tasks are running")
    print("3. Monitoring task progress in real-time")
    print("4. Cancelling tasks on demand")
    print()
    
    # Create task manager with limit of 3 concurrent tasks
    manager = TaskManager(max_concurrent_tasks=3)
    
    # Add event callback to show real-time updates
    def on_event(task, event_type):
        if event_type == "started":
            print(f"  🚀 Task '{task.name}' started")
        elif event_type == "completed":
            print(f"  ✓ Task '{task.name}' completed")
        elif event_type == "failed":
            print(f"  ✗ Task '{task.name}' failed: {task.error}")
        elif event_type == "cancelled":
            print(f"  ⊗ Task '{task.name}' cancelled")
    
    manager.add_event_callback(on_event)
    
    # Start the task manager
    print("Starting task manager...")
    runner = asyncio.create_task(manager.run_tasks())
    
    # Simulate user issuing commands
    try:
        await simulate_user_commands(manager)
    finally:
        # Clean shutdown
        print("\n" + "="*60)
        print("Shutting down...")
        manager.stop()
        await asyncio.sleep(0.5)
    
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
