import asyncio
from src.task_manager import TaskManager, TaskState
from src.background_actions import download_file, reminder_timer, periodic_health_check


async def demo_multitasking():
    print("=" * 60)
    print("Jarvis Multitasking Demo")
    print("=" * 60)
    print()
    
    manager = TaskManager(max_concurrent_tasks=3)
    
    def on_event(task, event_type):
        print(f"[EVENT] Task '{task.name}' {event_type} (Progress: {task.progress:.1f}%)")
    
    manager.add_event_callback(on_event)
    
    print("Creating tasks...")
    print()
    
    async def reminder_5s(task):
        return await reminder_timer(task, 5, "5 second reminder completed!")
    
    async def reminder_10s(task):
        return await reminder_timer(task, 10, "10 second reminder completed!")
    
    async def reminder_15s(task):
        return await reminder_timer(task, 15, "15 second reminder completed!")
    
    task1_id = manager.create_task("Reminder 5s", reminder_5s, priority=1)
    task2_id = manager.create_task("Reminder 10s", reminder_10s, priority=2)
    task3_id = manager.create_task("Reminder 15s", reminder_15s, priority=3)
    
    print(f"✓ Created task 1: Reminder 5s (ID: {task1_id[:8]})")
    print(f"✓ Created task 2: Reminder 10s (ID: {task2_id[:8]})")
    print(f"✓ Created task 3: Reminder 15s (ID: {task3_id[:8]})")
    print()
    
    print("Starting task manager...")
    runner = asyncio.create_task(manager.run_tasks())
    
    await asyncio.sleep(2)
    
    print("\nAdding more tasks while others are running...")
    
    async def health_check_task(task):
        return await periodic_health_check(
            task, 
            "https://httpbin.org/status/200", 
            interval_seconds=2, 
            max_checks=3
        )
    
    task4_id = manager.create_task("Health Check", health_check_task, priority=5)
    print(f"✓ Created task 4: Health Check (ID: {task4_id[:8]})")
    print()
    
    for i in range(20):
        await asyncio.sleep(1)
        
        stats = manager.get_stats()
        running_tasks = manager.list_tasks(TaskState.RUNNING)
        
        print(f"\n[{i+1}s] Stats: Running={stats['running']}, "
              f"Pending={stats['pending']}, Completed={stats['completed']}")
        
        if running_tasks:
            print("   Running tasks:")
            for task in running_tasks:
                print(f"   - {task.name}: {task.progress:.1f}%")
        
        if stats['running'] == 0 and stats['pending'] == 0:
            print("\nAll tasks completed!")
            break
    
    print("\n" + "=" * 60)
    print("Final Results")
    print("=" * 60)
    
    all_tasks = manager.list_tasks()
    for task in all_tasks:
        status_symbol = "✓" if task.state == TaskState.COMPLETED else "✗"
        print(f"{status_symbol} {task.name}: {task.state.value}")
        if task.result:
            print(f"   Result: {task.result}")
        if task.error:
            print(f"   Error: {task.error}")
    
    print()
    final_stats = manager.get_stats()
    print(f"Total tasks: {final_stats['total']}")
    print(f"Completed: {final_stats['completed']}")
    print(f"Failed: {final_stats['failed']}")
    print(f"Cancelled: {final_stats['cancelled']}")
    
    manager.stop()
    await asyncio.sleep(0.5)
    
    print("\nDemo completed!")


if __name__ == "__main__":
    asyncio.run(demo_multitasking())
