# Task Manager API Documentation

## Overview

The Task Manager provides asynchronous task execution capabilities with state tracking, priority scheduling, and event notifications.

## Core Components

### TaskState Enum

Represents the lifecycle states of a task:

- `PENDING`: Task created but not yet started
- `RUNNING`: Task currently executing
- `COMPLETED`: Task finished successfully
- `FAILED`: Task encountered an error
- `CANCELLED`: Task was cancelled before or during execution

### Task Dataclass

Properties:
- `id`: Unique task identifier (UUID)
- `name`: Human-readable task name
- `coroutine`: Async function to execute
- `state`: Current TaskState
- `priority`: Integer priority (higher = runs first)
- `progress`: Float from 0.0 to 100.0
- `result`: Return value from coroutine (when completed)
- `error`: Error message (when failed)
- `created_at`: Timestamp of creation
- `started_at`: Timestamp when execution began
- `completed_at`: Timestamp when execution finished

### TaskManager Class

#### Initialization

```python
manager = TaskManager(max_concurrent_tasks=5)
```

Parameters:
- `max_concurrent_tasks`: Maximum number of tasks to run simultaneously

#### Methods

##### create_task(name, coroutine, priority=0) -> str

Creates and enqueues a new task.

```python
async def my_task(task):
    # Your async code here
    task.progress = 50.0
    await asyncio.sleep(1)
    return "result"

task_id = manager.create_task("My Task", my_task, priority=10)
```

Returns: Task ID (string)

##### get_task(task_id) -> Optional[Task]

Retrieves a task by ID.

```python
task = manager.get_task(task_id)
if task:
    print(f"State: {task.state}, Progress: {task.progress}%")
```

##### list_tasks(state=None) -> List[Task]

Lists all tasks, optionally filtered by state.

```python
# Get all tasks
all_tasks = manager.list_tasks()

# Get only running tasks
running = manager.list_tasks(TaskState.RUNNING)
```

##### cancel_task(task_id) -> bool

Cancels a pending or running task.

```python
if manager.cancel_task(task_id):
    print("Task cancelled")
```

Returns: True if cancelled, False otherwise

##### set_priority(task_id, priority) -> bool

Updates the priority of a pending task.

```python
manager.set_priority(task_id, 100)
```

##### update_progress(task_id, progress)

Updates the progress percentage (0.0-100.0).

```python
manager.update_progress(task_id, 75.0)
```

##### add_event_callback(callback)

Registers a callback for task events.

```python
async def on_task_event(task, event_type):
    print(f"Task {task.name} {event_type}")

manager.add_event_callback(on_task_event)
```

Event types: "started", "completed", "failed", "cancelled"

##### get_stats() -> Dict[str, int]

Returns task statistics.

```python
stats = manager.get_stats()
# {'total': 10, 'pending': 2, 'running': 3, 'completed': 5, 'failed': 0, 'cancelled': 0}
```

##### async run_tasks()

Main task execution loop. Should be run as a background task.

```python
runner = asyncio.create_task(manager.run_tasks())
```

##### stop()

Stops the task manager and cancels all running tasks.

```python
manager.stop()
```

## Background Actions

Pre-built async actions in `src/background_actions.py`:

### download_file(task, url, destination, chunk_size=8192)

Downloads a file with progress tracking.

```python
async def download_wrapper(task):
    return await download_file(task, "https://example.com/file.zip", "./downloads/file.zip")

task_id = manager.create_task("Download", download_wrapper)
```

### reminder_timer(task, duration_seconds, message)

Creates a countdown timer.

```python
async def reminder_wrapper(task):
    return await reminder_timer(task, 60, "One minute is up!")

task_id = manager.create_task("Reminder", reminder_wrapper)
```

### periodic_health_check(task, url, interval_seconds=60, max_checks=10)

Performs periodic HTTP health checks.

```python
async def health_wrapper(task):
    return await periodic_health_check(task, "https://myapi.com/health", 30, 20)

task_id = manager.create_task("Health Check", health_wrapper)
```

### batch_web_search(task, queries, delay_seconds=1.0)

Processes multiple queries with delays.

```python
async def search_wrapper(task):
    queries = ["python asyncio", "task management", "concurrent programming"]
    return await batch_web_search(task, queries, delay_seconds=2.0)

task_id = manager.create_task("Batch Search", search_wrapper)
```

## Usage Patterns

### Basic Task Execution

```python
import asyncio
from src.task_manager import TaskManager

async def main():
    manager = TaskManager(max_concurrent_tasks=3)
    
    async def my_work(task):
        await asyncio.sleep(2)
        return "Done!"
    
    task_id = manager.create_task("Work", my_work)
    
    # Start the manager
    runner = asyncio.create_task(manager.run_tasks())
    
    # Wait for completion
    await asyncio.sleep(3)
    
    task = manager.get_task(task_id)
    print(f"Result: {task.result}")
    
    manager.stop()

asyncio.run(main())
```

### Task with Progress Updates

```python
async def progressive_task(task):
    total_steps = 10
    for i in range(total_steps):
        # Do some work
        await asyncio.sleep(0.5)
        
        # Update progress
        progress = ((i + 1) / total_steps) * 100
        task.progress = progress
    
    return "All steps completed"

task_id = manager.create_task("Progressive", progressive_task)
```

### Event Monitoring

```python
def log_event(task, event_type):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {task.name} - {event_type}")

manager.add_event_callback(log_event)
```

### Priority Queue

```python
# High priority tasks run first
urgent = manager.create_task("Urgent", urgent_work, priority=100)
normal = manager.create_task("Normal", normal_work, priority=10)
low = manager.create_task("Low", low_work, priority=1)
```

### Error Handling

```python
async def risky_task(task):
    try:
        # Risky operation
        result = await some_async_operation()
        return result
    except Exception as e:
        # Error is automatically captured in task.error
        raise

task_id = manager.create_task("Risky", risky_task)

# Check later
task = manager.get_task(task_id)
if task.state == TaskState.FAILED:
    print(f"Error: {task.error}")
```

## Best Practices

1. **Progress Updates**: Update `task.progress` regularly for long-running tasks
2. **Resource Cleanup**: Always call `manager.stop()` when done
3. **Concurrency Limits**: Set `max_concurrent_tasks` based on your resources
4. **Priority Range**: Use 0-100 for priorities (higher = more urgent)
5. **Error Handling**: Let exceptions propagate; they're automatically captured
6. **Task Names**: Use descriptive names for better monitoring
7. **Event Callbacks**: Keep callbacks fast to avoid blocking the event loop

## Thread Safety

TaskManager uses threading.Lock for thread-safe operations:
- Creating tasks
- Updating task state
- Querying task information

However, the async operations themselves should not be called from multiple threads.

## Performance Considerations

- Tasks are selected for execution based on priority every 0.1 seconds
- Event callbacks should be lightweight
- Network operations automatically benefit from asyncio's efficiency
- Consider using `max_concurrent_tasks` to limit resource usage

## Troubleshooting

### Tasks Not Starting

Check if `run_tasks()` is running:
```python
runner = asyncio.create_task(manager.run_tasks())
```

### Tasks Stuck in PENDING

Reduce `max_concurrent_tasks` or wait for running tasks to complete.

### Progress Not Updating

Ensure you're calling `task.progress = value` or `manager.update_progress()`.

### Memory Leaks

Call `manager.stop()` to clean up resources when done.
