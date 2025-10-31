# Quick Start Guide

Get up and running with Jarvis text interface in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Test Direct Mode (No Server Required)

The simplest way to test - runs commands directly without starting an API server:

```bash
# Single command
python cli_client.py command "what time is it" --direct

# Interactive mode
python cli_client.py interactive --direct
```

## 3. Start the API Server

In a separate terminal:

```bash
python text_api.py
```

The server will start at http://localhost:8000

## 4. Use the CLI Client (API Mode)

In another terminal:

```bash
# Send a command
python cli_client.py command "what time is it"

# Check status
python cli_client.py status

# Interactive mode
python cli_client.py interactive
```

## 5. Test with curl

```bash
# Get API info
curl http://localhost:8000/

# Send a command (requires authentication)
curl -X POST http://localhost:8000/commands \
  -H "X-API-Key: jarvis-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"command": "what time is it"}'

# Get status
curl -X GET http://localhost:8000/status \
  -H "X-API-Key: jarvis-secret-key-123"
```

Or run all curl examples:

```bash
./curl_examples.sh
```

## 6. Run the Demo

```bash
python demo.py
```

This will demonstrate both direct mode and API mode with various commands.

## Try These Commands

- `what time is it` - Get current time
- `wikipedia [topic]` - Search Wikipedia (e.g., "wikipedia artificial intelligence")
- `open youtube` - Open YouTube in browser
- `open google` - Open Google in browser
- `weather` - Get weather (requires WEATHER_API_KEY env variable)

## WebSocket Stream

Connect to the WebSocket for real-time updates:

```bash
python cli_client.py stream
```

Or with a WebSocket client:

```bash
wscat -c "ws://localhost:8000/stream?api_key=jarvis-secret-key-123"
```

Then send commands:
```json
{"type": "command", "command": "what time is it"}
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Customize API Key

Set your own API key:

```bash
export JARVIS_API_KEY="your-secret-key"
python text_api.py
```

For the CLI client:

```bash
export JARVIS_API_KEY="your-secret-key"
python cli_client.py command "what time is it"
```

## Need Help?

Check the full documentation in [README.md](README.md)
