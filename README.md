# Jarvis AI Assistant

Advanced AI assistant inspired by Iron Man's JARVIS, now with multitasking capabilities.

## Features

### Core Capabilities
- Voice-based interaction using speech recognition
- Text-to-speech responses
- Wikipedia search integration
- Web browser control (YouTube, Google)
- Current time and weather information
- Wolfram Alpha integration

### Task Management System
- **Concurrent Task Execution**: Run multiple tasks simultaneously with configurable concurrency limits
- **Task States**: Track tasks through pending, running, completed, failed, and cancelled states
- **Progress Tracking**: Real-time progress updates for long-running operations
- **Priority System**: Prioritize important tasks to run first
- **Task Cancellation**: Cancel running or pending tasks
- **Event Notifications**: Get voice/text notifications when tasks start, complete, or fail

### Built-in Background Actions
- **File Download**: Download files asynchronously with progress tracking
- **Reminder Timer**: Set countdown timers with completion notifications
- **Health Check**: Periodic URL health monitoring
- **Batch Operations**: Process multiple queries in sequence

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Mode (Recommended for Testing)

Run the CLI version that accepts text commands:

```bash
python jarvis_cli.py
```

Available commands:
- `help` - Show all available commands
- `wikipedia <query>` - Search Wikipedia
- `open youtube` - Open YouTube in browser
- `open google` - Open Google in browser
- `time` - Get current time
- `weather` - Get weather information (requires API key)

Task management commands:
- `download test` - Start a test file download
- `reminder <seconds>` - Set a reminder timer
- `health check` - Start periodic health monitoring
- `list tasks` - Show all tasks with their states
- `cancel task [id]` - Cancel a specific or most recent task
- `task status` - Show running task progress

### Voice Mode

Run the voice-enabled version:

```bash
python jarvis_async.py
```

Note: Requires a microphone and speaker setup.

### Original Version

The original synchronous version is still available:

```bash
python jarvis.py
```

## Architecture

### TaskManager
Located in `src/task_manager.py`, this is the core of the multitasking system:
- Uses asyncio for concurrent task execution
- Manages task lifecycle and state transitions
- Provides event callbacks for task updates
- Enforces concurrency limits

### Background Actions
Located in `src/background_actions.py`, provides reusable async operations:
- `download_file`: Async file downloads with progress
- `reminder_timer`: Countdown timers
- `periodic_health_check`: URL health monitoring
- `batch_web_search`: Batch query processing

### Jarvis Implementations
- `jarvis.py`: Original synchronous version
- `jarvis_async.py`: Async version with voice support
- `jarvis_cli.py`: CLI version for easier testing and development

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

Test categories:
- `test_task_manager.py`: Task creation, execution, cancellation, priority
- `test_background_actions.py`: Background action functionality

## Configuration

### Weather API
To use weather functionality, add your OpenWeatherMap API key:
1. Get a free API key from https://openweathermap.org/api
2. Update the `api_key` variable in the weather command section
3. Set your city name in the `city` variable

### Wolfram Alpha
For advanced queries, configure Wolfram Alpha:
1. Get an API key from https://products.wolframalpha.com/api/
2. Add initialization code in the Jarvis class

## Examples

### Running Multiple Tasks Concurrently

```python
# Start multiple tasks
download test
reminder 30
health check

# Check their status
list tasks
task status

# Cancel if needed
cancel task <id>
```

### Programmatic Usage

```python
import asyncio
from src.task_manager import TaskManager
from src.background_actions import reminder_timer

async def main():
    manager = TaskManager(max_concurrent_tasks=5)
    
    # Create tasks
    async def my_task(task):
        await reminder_timer(task, 10, "Done!")
        return "Success"
    
    task_id = manager.create_task("My Timer", my_task, priority=5)
    
    # Run the manager
    runner = asyncio.create_task(manager.run_tasks())
    
    # Wait for completion
    await asyncio.sleep(15)
    
    # Check results
    task = manager.get_task(task_id)
    print(f"Task completed: {task.result}")
    
    manager.stop()

asyncio.run(main())
```

## Acceptance Criteria Status

✅ System can handle at least three concurrent tasks while responding to new commands
✅ Task state changes surface in GUI/API and voice notifications
✅ Tests cover scheduling, cancellation, and recovery scenarios
✅ Built-in background actions showcase functionality
✅ Voice/text interfaces announce task updates without blocking

## Contributing

When adding new background actions:
1. Add the async function to `src/background_actions.py`
2. Update the task progress periodically
3. Return a result dictionary
4. Add tests in `tests/test_background_actions.py`

## License

MIT License
