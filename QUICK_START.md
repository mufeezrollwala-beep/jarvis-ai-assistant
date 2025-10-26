# Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test suite to verify installation:**
   ```bash
   python test_memory.py
   ```

## Running Jarvis

### With Voice Interface (requires microphone)
```bash
python jarvis.py
```

### Without Voice (programmatic usage)
```bash
python example_usage.py
```

## First-Time Setup

On first run, Jarvis will prompt for onboarding. You can also set up manually:

```bash
# Interactive onboarding
python cli.py onboarding run

# Quick setup
python cli.py onboarding quick --name "Your Name" --location "Your City"
```

## Common Commands

### Voice Commands
- "Wikipedia [topic]" - Search Wikipedia
- "Open YouTube" / "Open Google" - Open websites
- "What time is it?" - Current time
- "What's the weather?" - Weather info (requires API key)
- "Remember [something]" - Store a memory
- "What do you remember?" - Retrieve context
- "What's my name?" - Query preferences
- "Exit" / "Goodbye" - Exit Jarvis

### CLI Commands

**View Statistics**
```bash
python cli.py stats
```

**List Memories**
```bash
python cli.py list short              # Recent conversation
python cli.py list long --limit 20    # Long-term memories
python cli.py list all                # Everything
```

**Search Memories**
```bash
python cli.py search "pizza preferences"
```

**Manage Preferences**
```bash
python cli.py preferences list
python cli.py preferences set --key theme --value dark
python cli.py preferences get --key user_name
```

**View Tasks**
```bash
python cli.py tasks --limit 10
```

**Export/Import**
```bash
python cli.py export --output backup.json
python cli.py import backup.json
```

**Maintenance**
```bash
python cli.py prune --days 30    # Delete old memories
python cli.py clear short        # Clear short-term memory
```

## Running Tests

```bash
# Full test suite
python test_memory.py

# Acceptance criteria demo
python manual_test_demo.py

# Example usage
python example_usage.py
```

## Configuration

### Weather API
Set environment variable:
```bash
export WEATHER_API_KEY="your_openweathermap_api_key"
```

Or set in code (jarvis.py line 100).

### Memory Settings
Edit memory_store.py:
- Line 14-15: TTL and max size for short-term memory
- Line 54: ChromaDB directory
- Line 9: Sentence transformer model

## Troubleshooting

**"No module named 'chromadb'"**
```bash
pip install chromadb sentence-transformers
```

**Microphone not working**
```bash
# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# Windows/Mac
pip install pyaudio
```

**Memory not persisting**
- Check write permissions in project directory
- Verify memory_data/ directory can be created
- Check disk space

## Data Location

All memory data is stored in:
- `./memory_data/` - Default location
- `./memory_data/chroma/` - Vector embeddings
- `./memory_data/metadata.db` - SQLite database

**Backup your data:**
```bash
python cli.py export --output backup_$(date +%Y%m%d).json
```

## Next Steps

1. Run onboarding: `python cli.py onboarding run`
2. Test the system: `python example_usage.py`
3. Try voice commands: `python jarvis.py`
4. Explore CLI: `python cli.py --help`

For detailed documentation, see [README.md](README.md).
