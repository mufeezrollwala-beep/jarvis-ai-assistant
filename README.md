# Jarvis AI Assistant

Advanced AI assistant inspired by Iron Man's JARVIS. Now supports both voice and text interfaces!

## Features

- 🎤 **Voice Interface**: Traditional voice-controlled assistant
- 💬 **Text Interface**: FastAPI-based REST API and WebSocket support
- 🖥️ **CLI Client**: Interactive command-line interface
- 🔐 **Authentication**: API key-based security
- 📊 **Real-time Updates**: WebSocket streaming for live command processing
- 🔄 **Unified Logic**: Both voice and text commands share the same processing core

## Supported Commands

- `wikipedia [query]` - Search Wikipedia
- `open youtube` - Open YouTube in browser
- `open google` - Open Google in browser
- `time` - Get current time
- `weather` - Get weather information (requires API key)
- `exit/quit/goodbye` - Exit the assistant

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
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

4. (Optional) Set environment variables:
```bash
export JARVIS_API_KEY="your-secret-key"
export WEATHER_API_KEY="your-openweathermap-api-key"
export WEATHER_CITY="London"
```

## Usage

### Voice Interface

Run the traditional voice-controlled assistant:

```bash
python jarvis.py
```

### Text API Server

Start the FastAPI server:

```bash
python text_api.py
```

Or using uvicorn directly:

```bash
uvicorn text_api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### CLI Client

The CLI provides several commands for interacting with Jarvis:

#### Send a single command (via API):
```bash
python cli_client.py command "what time is it"
```

#### Send a command directly (without API):
```bash
python cli_client.py command "wikipedia python programming" --direct
```

#### Interactive mode:
```bash
python cli_client.py interactive
```

#### Check system status:
```bash
python cli_client.py status
```

#### WebSocket stream:
```bash
python cli_client.py stream
```

## API Documentation

### Authentication

All API endpoints require authentication via the `X-API-Key` header:

```bash
X-API-Key: your-secret-key
```

Default API key: `jarvis-secret-key-123` (change via `JARVIS_API_KEY` environment variable)

### Endpoints

#### POST /commands

Send a text command to Jarvis.

**Request:**
```bash
curl -X POST http://localhost:8000/commands \
  -H "X-API-Key: jarvis-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"command": "what time is it"}'
```

**Response:**
```json
{
  "success": true,
  "message": "The time is 14:30:45",
  "data": "14:30:45",
  "action": "get_time",
  "timestamp": "2024-01-01T14:30:45.123456"
}
```

#### GET /status

Get system status and statistics.

**Request:**
```bash
curl -X GET http://localhost:8000/status \
  -H "X-API-Key: jarvis-secret-key-123"
```

**Response:**
```json
{
  "status": "active",
  "uptime": 123.45,
  "commands_processed": 42,
  "last_command": {
    "query": "what time is it",
    "timestamp": "2024-01-01T14:30:45.123456"
  },
  "timestamp": "2024-01-01T14:31:00.000000"
}
```

#### WebSocket /stream

Real-time streaming of command processing updates.

**Connect:**
```bash
wscat -c "ws://localhost:8000/stream?api_key=jarvis-secret-key-123"
```

**Send command:**
```json
{"type": "command", "command": "what time is it"}
```

**Receive updates:**
```json
{"type": "processing", "message": "Processing command: what time is it", "timestamp": "2024-01-01T14:30:45"}
{"type": "result", "command": "what time is it", "response": {...}, "timestamp": "2024-01-01T14:30:46"}
```

### Example Usage with curl

```bash
# Get API information
curl http://localhost:8000/

# Send a time command
curl -X POST http://localhost:8000/commands \
  -H "X-API-Key: jarvis-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"command": "time"}'

# Search Wikipedia
curl -X POST http://localhost:8000/commands \
  -H "X-API-Key: jarvis-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"command": "wikipedia artificial intelligence"}'

# Open YouTube
curl -X POST http://localhost:8000/commands \
  -H "X-API-Key: jarvis-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"command": "open youtube"}'

# Check status
curl -X GET http://localhost:8000/status \
  -H "X-API-Key: jarvis-secret-key-123"
```

### Example Usage with Python

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "jarvis-secret-key-123"
HEADERS = {"X-API-Key": API_KEY}

# Send a command
response = requests.post(
    f"{API_URL}/commands",
    json={"command": "what time is it"},
    headers=HEADERS
)
print(response.json())

# Get status
response = requests.get(f"{API_URL}/status", headers=HEADERS)
print(response.json())
```

### WebSocket Example with Python

```python
import asyncio
import websockets
import json

async def test_stream():
    uri = "ws://localhost:8000/stream?api_key=jarvis-secret-key-123"
    
    async with websockets.connect(uri) as websocket:
        # Send a command
        await websocket.send(json.dumps({
            "type": "command",
            "command": "what time is it"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(test_stream())
```

## Architecture

The project is organized into three main components:

1. **jarvis.py**: Core logic and voice interface
   - `JarvisCore`: Shared command processing logic
   - `Jarvis`: Voice-specific interface with speech recognition and TTS

2. **text_api.py**: FastAPI service
   - REST endpoints for command processing and status
   - WebSocket support for real-time updates
   - API key authentication

3. **cli_client.py**: Command-line interface
   - Direct mode (in-process execution)
   - API mode (communicates with FastAPI server)
   - Interactive mode for conversations
   - WebSocket streaming support

## Configuration

Environment variables:

- `JARVIS_API_KEY`: API authentication key (default: `jarvis-secret-key-123`)
- `JARVIS_API_URL`: API base URL for CLI client (default: `http://localhost:8000`)
- `WEATHER_API_KEY`: OpenWeatherMap API key (required for weather commands)
- `WEATHER_CITY`: Default city for weather queries (default: `London`)

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### API Documentation

When the server is running, access interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## Quick Reference

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[verify_installation.py](verify_installation.py)** - Check if everything is installed
- **[test_acceptance_criteria.py](test_acceptance_criteria.py)** - Verify acceptance criteria
- **[curl_examples.sh](curl_examples.sh)** - Run all curl examples
- **[demo.py](demo.py)** - Interactive demo script

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
