# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Run Examples

### 1. Acceptance Criteria Verification
```bash
python test_acceptance_criteria.py
```
This script demonstrates all acceptance criteria are met.

### 2. Interactive CLI Mode (Recommended)
```bash
python jarvis_cli.py
```
Then try these commands:
```
help
reminder 10
list tasks
task status
download test
cancel task
exit
```

### 3. Multitasking Demo
```bash
python demo_multitasking.py
```
Shows tasks running concurrently with real-time progress.

### 4. Concurrent Operations Example
```bash
python example_concurrent.py
```
Advanced demo showing commands during task execution.

## Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_task_manager.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## Quick API Usage

```python
import asyncio
from src.task_manager import TaskManager
from src.background_actions import reminder_timer

async def main():
    # Create manager
    manager = TaskManager(max_concurrent_tasks=3)
    
    # Add event callback
    def on_event(task, event_type):
        print(f"{task.name}: {event_type}")
    
    manager.add_event_callback(on_event)
    
    # Create tasks
    async def my_task(task):
        return await reminder_timer(task, 5, "Done!")
    
    task_id = manager.create_task("My Timer", my_task, priority=10)
    
    # Start manager
    runner = asyncio.create_task(manager.run_tasks())
    
    # Wait for tasks
    await asyncio.sleep(6)
    
    # Get result
    task = manager.get_task(task_id)
    print(f"Result: {task.result}")
    
    # Cleanup
    manager.stop()

asyncio.run(main())
```

## Key Features

✅ Concurrent task execution (configurable limit)  
✅ Priority-based scheduling  
✅ Real-time progress tracking  
✅ Task cancellation  
✅ Event notifications  
✅ Built-in actions (download, timer, health check)  
✅ Voice and CLI interfaces  
✅ Comprehensive tests  

## Documentation

- **README.md** - Full documentation
- **TASK_MANAGER_API.md** - Complete API reference
- **IMPLEMENTATION_SUMMARY.md** - Technical details

## Troubleshooting

**Tasks not starting?**
- Ensure `manager.run_tasks()` is running as async task

**Network tests failing?**
- Tests gracefully skip if external services unavailable
- Run `pytest tests/test_task_manager.py` for non-network tests

**Voice mode not working?**
- Use CLI mode: `python jarvis_cli.py`
- Voice mode requires microphone hardware
