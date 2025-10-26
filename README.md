# JARVIS - AI Assistant with Memory System

Advanced AI assistant inspired by Iron Man's JARVIS, featuring a comprehensive memory system for contextual conversations and persistent learning.

## Features

### Core Capabilities
- 🎤 Voice recognition and text-to-speech
- 🔍 Wikipedia search integration
- 🌐 Web browser automation (YouTube, Google)
- ⏰ Time queries
- 🌤️ Weather information (with OpenWeatherMap API)
- 💬 Natural conversation flow

### Memory System
- **Short-term Memory**: Maintains conversation context with TTL (Time-To-Live)
- **Long-term Memory**: Persistent knowledge storage using vector embeddings (Chroma)
- **User Preferences**: Remembers user settings and preferences
- **Task Tracking**: Logs completed tasks and their results
- **Smart Context Retrieval**: Uses semantic search to find relevant memories

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up API keys:
```bash
export WEATHER_API_KEY="your_openweathermap_api_key"
```

## Usage

### Running Jarvis

Start the voice assistant:
```bash
python jarvis.py
```

On first run, you'll be prompted to complete onboarding to set up your preferences.

### Voice Commands

- **Wikipedia**: "Wikipedia Albert Einstein"
- **Web Navigation**: "Open YouTube" / "Open Google"
- **Time**: "What time is it?"
- **Weather**: "What's the weather?"
- **Memory**: "Remember that I like pizza" / "What do you remember?"
- **Personal**: "What's my name?"
- **Exit**: "Goodbye" / "Exit"

### Memory Management CLI

The CLI tool provides powerful memory inspection and management:

#### View Statistics
```bash
python cli.py stats
```

#### List Memories
```bash
# List short-term memories
python cli.py list short

# List long-term memories
python cli.py list long --limit 50

# List all memories
python cli.py list all
```

#### Search Memories
```bash
python cli.py search "pizza preferences" --limit 5
```

#### Manage Preferences
```bash
# List all preferences
python cli.py preferences list

# Set a preference
python cli.py preferences set --key user_name --value "Tony Stark"

# Get a specific preference
python cli.py preferences get --key user_name
```

#### View Tasks
```bash
python cli.py tasks --limit 20
```

#### Export/Import Memories
```bash
# Export memories
python cli.py export --output my_memories.json

# Import memories
python cli.py import my_memories.json

# Import and clear existing
python cli.py import my_memories.json --clear
```

#### Prune Old Memories
```bash
# Delete memories older than 30 days
python cli.py prune --days 30
```

#### Clear Memories
```bash
# Clear short-term memory
python cli.py clear short

# Clear long-term memory
python cli.py clear long

# Clear all memories
python cli.py clear all
```

#### Onboarding Management
```bash
# Run full onboarding
python cli.py onboarding run

# Check onboarding status
python cli.py onboarding status

# Quick setup
python cli.py onboarding quick --name "Tony Stark" --location "New York"
```

## Memory System Architecture

### Short-term Memory
- **Purpose**: Maintains recent conversation context
- **TTL**: 1 hour (configurable)
- **Max Size**: 50 entries (configurable)
- **Storage**: In-memory deque with automatic expiration

### Long-term Memory
- **Purpose**: Persistent knowledge and learning
- **Storage**: ChromaDB with vector embeddings
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Features**: Semantic search, category filtering, persistence

### Metadata Database
- **Storage**: SQLite
- **Tables**:
  - `user_preferences`: User settings and preferences
  - `conversation_sessions`: Session tracking
  - `completed_tasks`: Task history

### Memory Categories
- `conversation`: User-assistant dialogue
- `preference`: User preferences and settings
- `task`: Completed tasks
- `user_note`: Explicit user memories
- `correction`: User corrections and clarifications
- `interest`: User interests
- `device`: Smart home devices
- `system`: System capabilities

## API Reference

### MemoryStore Class

```python
from memory_store import MemoryStore

# Initialize
memory = MemoryStore(persist_directory="./memory_data")

# Add conversation
memory.add_conversation("What's the weather?", "It's sunny today")

# Add user preference
memory.add_user_preference("favorite_color", "blue")

# Retrieve context
context = memory.retrieve_context("weather preferences", long_term_limit=5)

# Add task
memory.add_task("Check weather", result="Completed successfully")

# Export memories
memory.export_memories("backup.json")

# Get statistics
stats = memory.get_stats()
```

### OnboardingManager Class

```python
from onboarding import OnboardingManager

# Initialize
onboarding = OnboardingManager(memory_store)

# Run interactive onboarding
onboarding.run_onboarding()

# Quick setup
onboarding.quick_setup("Tony Stark", location="New York")

# Add device knowledge
onboarding.add_device_knowledge(
    device_name="Living Room Lights",
    device_type="smart_light",
    location="living room",
    capabilities=["turn on", "turn off", "dim", "change color"]
)

# Add correction
onboarding.add_correction("play music", "play my workout playlist")
```

## Configuration

### Memory Settings

Edit the initialization parameters in your code:

```python
# Short-term memory configuration
short_term = ShortTermMemory(
    max_size=50,        # Maximum entries
    ttl_seconds=3600    # 1 hour TTL
)

# Long-term memory configuration
long_term = LongTermMemory(
    persist_directory="./memory_data/chroma"
)
```

### User Preferences

Supported preferences:
- `user_name`: User's name
- `user_location`: City/location for weather
- `temperature_unit`: "celsius" or "fahrenheit"
- `time_format`: "12" or "24"
- `user_interests`: Comma-separated interests

## Testing

### Manual Test Scenarios

1. **Context Persistence**:
   ```
   User: "Remember I like pepperoni pizza"
   User: "What's my favorite pizza?"
   Expected: Jarvis recalls the preference
   ```

2. **Conversation Context**:
   ```
   User: "Open YouTube"
   User: "Now search for cooking videos"
   Expected: Jarvis understands "Now" refers to YouTube
   ```

3. **Session Survival**:
   ```
   1. Set a preference: "Remember my name is Tony"
   2. Exit and restart Jarvis
   3. Ask: "What's my name?"
   Expected: Jarvis remembers "Tony"
   ```

### Verify Memory Persistence

```bash
# Add some memories
python jarvis.py

# Check they're stored
python cli.py stats
python cli.py list long

# Restart and verify
python jarvis.py  # Memories should still be available
```

## Data Persistence

All memory data is stored in the `memory_data/` directory:

```
memory_data/
├── chroma/              # Vector embeddings (Chroma)
│   ├── chroma.sqlite3
│   └── ...
└── metadata.db          # SQLite database for preferences and tasks
```

This directory is gitignored and should be backed up separately.

## Troubleshooting

### Memory System Not Working
- Check that `memory_data/` directory is writable
- Verify ChromaDB installation: `pip install chromadb`
- Check disk space

### Voice Recognition Issues
- Ensure microphone permissions are granted
- Install PyAudio: `pip install pyaudio`
- On Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`

### Import Errors
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Jarvis                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Voice Input → Speech Recognition → Command Parser  │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Memory System                       │   │
│  │  ┌──────────────┐    ┌─────────────────────────┐   │   │
│  │  │ Short-term   │    │    Long-term            │   │   │
│  │  │ (TTL Queue)  │    │  (Chroma Vectors)       │   │   │
│  │  └──────────────┘    └─────────────────────────┘   │   │
│  │           ↓                     ↓                    │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │    SQLite Metadata Store                    │   │   │
│  │  │  (Preferences, Tasks, Sessions)             │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Context-Enhanced Response Generation              │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Text-to-Speech Output                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Contributing

Contributions are welcome! Please follow these guidelines:
- Write clear commit messages
- Add tests for new features
- Update documentation
- Follow existing code style

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by Marvel's JARVIS from Iron Man
- Built with ChromaDB, sentence-transformers, and other amazing open-source tools
