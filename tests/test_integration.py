import pytest
import asyncio
from src.task_manager import TaskManager, TaskState
from src.background_actions import reminder_timer


@pytest.mark.asyncio
async def test_concurrent_task_execution():
    manager = TaskManager(max_concurrent_tasks=3)
    
    async def task_1(task):
        await asyncio.sleep(0.5)
        return "task1_done"
    
    async def task_2(task):
        await asyncio.sleep(0.5)
        return "task2_done"
    
    async def task_3(task):
        await asyncio.sleep(0.5)
        return "task3_done"
    
    task_ids = [
        manager.create_task("Task 1", task_1),
        manager.create_task("Task 2", task_2),
        manager.create_task("Task 3", task_3),
    ]
    
    runner = asyncio.create_task(manager.run_tasks())
    
    await asyncio.sleep(1.5)
    
    for task_id in task_ids:
        task = manager.get_task(task_id)
        assert task.state == TaskState.COMPLETED
        assert "done" in task.result
    
    manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_task_manager_with_new_commands():
    manager = TaskManager(max_concurrent_tasks=2)
    
    events = []
    
    def track_events(task, event_type):
        events.append((task.name, event_type))
    
    manager.add_event_callback(track_events)
    
    async def quick_task(task):
        await asyncio.sleep(0.2)
        return "quick"
    
    task_id = manager.create_task("Quick Task", quick_task, priority=10)
    
    runner = asyncio.create_task(manager.run_tasks())
    
    await asyncio.sleep(0.1)
    
    tasks = manager.list_tasks()
    assert len(tasks) == 1
    
    await asyncio.sleep(0.5)
    
    assert ("Quick Task", "started") in events
    assert ("Quick Task", "completed") in events
    
    manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_multitasking_with_cancellation():
    manager = TaskManager(max_concurrent_tasks=3)
    
    async def long_task(task):
        await asyncio.sleep(5.0)
        return "should_not_complete"
    
    task_id = manager.create_task("Long Task", long_task)
    
    runner = asyncio.create_task(manager.run_tasks())
    
    await asyncio.sleep(0.3)
    
    task = manager.get_task(task_id)
    assert task.state == TaskState.RUNNING
    
    cancelled = manager.cancel_task(task_id)
    assert cancelled
    
    await asyncio.sleep(0.3)
    
    task = manager.get_task(task_id)
    assert task.state == TaskState.CANCELLED
    
    manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_priority_scheduling():
    manager = TaskManager(max_concurrent_tasks=1)
    
    execution_order = []
    
    async def tracking_task(task):
        execution_order.append(task.name)
        await asyncio.sleep(0.2)
        return "done"
    
    manager.create_task("Low", tracking_task, priority=1)
    manager.create_task("High", tracking_task, priority=100)
    manager.create_task("Medium", tracking_task, priority=50)
    
    runner = asyncio.create_task(manager.run_tasks())
    
    await asyncio.sleep(1.5)
    
    assert execution_order[0] == "High"
    assert execution_order[1] == "Medium"
    assert execution_order[2] == "Low"
    
    manager.stop()
    await asyncio.sleep(0.1)
