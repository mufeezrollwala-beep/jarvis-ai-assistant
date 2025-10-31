import pytest
import asyncio
from src.task_manager import TaskManager, TaskState, Task


@pytest.fixture
def task_manager():
    return TaskManager(max_concurrent_tasks=3)


@pytest.mark.asyncio
async def test_create_task(task_manager):
    async def sample_task(task):
        await asyncio.sleep(0.1)
        return "completed"
    
    task_id = task_manager.create_task("Test Task", sample_task)
    
    assert task_id is not None
    assert len(task_id) > 0
    
    task = task_manager.get_task(task_id)
    assert task is not None
    assert task.name == "Test Task"
    assert task.state == TaskState.PENDING


@pytest.mark.asyncio
async def test_task_execution(task_manager):
    result_value = "test_result"
    
    async def sample_task(task):
        await asyncio.sleep(0.1)
        return result_value
    
    task_id = task_manager.create_task("Test Task", sample_task)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(0.5)
    
    task = task_manager.get_task(task_id)
    assert task.state == TaskState.COMPLETED
    assert task.result == result_value
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_task_failure(task_manager):
    async def failing_task(task):
        await asyncio.sleep(0.1)
        raise ValueError("Test error")
    
    task_id = task_manager.create_task("Failing Task", failing_task)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(0.5)
    
    task = task_manager.get_task(task_id)
    assert task.state == TaskState.FAILED
    assert "Test error" in task.error
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_concurrent_tasks(task_manager):
    executed_tasks = []
    
    async def sample_task(task):
        executed_tasks.append(task.id)
        await asyncio.sleep(0.2)
        return "done"
    
    task_ids = []
    for i in range(5):
        task_id = task_manager.create_task(f"Task {i}", sample_task)
        task_ids.append(task_id)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(1.0)
    
    completed = task_manager.list_tasks(TaskState.COMPLETED)
    assert len(completed) == 5
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_cancel_task(task_manager):
    async def long_task(task):
        await asyncio.sleep(2.0)
        return "done"
    
    task_id = task_manager.create_task("Long Task", long_task)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(0.2)
    
    cancelled = task_manager.cancel_task(task_id)
    assert cancelled
    
    await asyncio.sleep(0.3)
    
    task = task_manager.get_task(task_id)
    assert task.state == TaskState.CANCELLED
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_task_priority(task_manager):
    execution_order = []
    
    async def tracking_task(task):
        execution_order.append(task.name)
        await asyncio.sleep(0.1)
        return "done"
    
    task_manager.max_concurrent_tasks = 1
    
    task_manager.create_task("Low Priority", tracking_task, priority=1)
    task_manager.create_task("High Priority", tracking_task, priority=10)
    task_manager.create_task("Medium Priority", tracking_task, priority=5)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(1.0)
    
    assert execution_order[0] == "High Priority"
    assert execution_order[1] == "Medium Priority"
    assert execution_order[2] == "Low Priority"
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_list_tasks(task_manager):
    async def sample_task(task):
        await asyncio.sleep(0.1)
        return "done"
    
    task_manager.create_task("Task 1", sample_task)
    task_manager.create_task("Task 2", sample_task)
    task_manager.create_task("Task 3", sample_task)
    
    all_tasks = task_manager.list_tasks()
    assert len(all_tasks) == 3
    
    pending_tasks = task_manager.list_tasks(TaskState.PENDING)
    assert len(pending_tasks) == 3


@pytest.mark.asyncio
async def test_task_stats(task_manager):
    async def sample_task(task):
        await asyncio.sleep(0.1)
        return "done"
    
    task_manager.create_task("Task 1", sample_task)
    task_manager.create_task("Task 2", sample_task)
    
    stats = task_manager.get_stats()
    
    assert stats['total'] == 2
    assert stats['pending'] == 2
    assert stats['running'] == 0
    assert stats['completed'] == 0


@pytest.mark.asyncio
async def test_progress_update(task_manager):
    async def progress_task(task):
        for i in range(5):
            task_manager.update_progress(task.id, (i + 1) * 20)
            await asyncio.sleep(0.1)
        return "done"
    
    task_id = task_manager.create_task("Progress Task", progress_task)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(0.7)
    
    task = task_manager.get_task(task_id)
    assert task.progress == 100.0
    
    task_manager.stop()
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_event_callbacks(task_manager):
    events = []
    
    async def event_callback(task, event_type):
        events.append((task.name, event_type))
    
    task_manager.add_event_callback(event_callback)
    
    async def sample_task(task):
        await asyncio.sleep(0.1)
        return "done"
    
    task_manager.create_task("Test Task", sample_task)
    
    runner = asyncio.create_task(task_manager.run_tasks())
    
    await asyncio.sleep(0.5)
    
    assert ("Test Task", "started") in events
    assert ("Test Task", "completed") in events
    
    task_manager.stop()
    await asyncio.sleep(0.1)
