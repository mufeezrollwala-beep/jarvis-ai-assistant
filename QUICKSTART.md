# Jarvis AI Assistant - Quick Start Guide

Get up and running with the LLM-powered Jarvis assistant in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key (or Azure OpenAI, or local model)

## Installation

### 1. Clone and Setup

```bash
# Navigate to project directory
cd jarvis-ai-assistant

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy example config
cp config.yaml config.local.yaml

# Set your API key
export OPENAI_API_KEY="sk-your-key-here"

# Or edit config.local.yaml directly (not recommended for production)
```

### 3. Test Installation

```bash
# Run tests to verify everything works
python -m unittest discover -s tests -p "test_*.py" -v

# Run demo (no API key needed for demo)
python demo.py
```

## Usage

### Option 1: Voice Interface (Full Experience)

```bash
python main.py
```

Speak commands like:
- "What time is it?"
- "Search Wikipedia for artificial intelligence"
- "Open YouTube"
- "What's the weather?"

### Option 2: Text Interface (For Testing)

```python
from jarvis import Jarvis
from jarvis.config import load_config

config = load_config("config.yaml")
jarvis = Jarvis(config)

# Process text directly
response = jarvis.agent.process_message("Tell me a joke")
print(response)
```

## Using Different LLM Providers

### OpenAI (Default)

```yaml
# config.yaml
llm:
  provider: "openai"
```

```bash
export OPENAI_API_KEY="sk-..."
```

### Azure OpenAI

```yaml
# config.yaml
llm:
  provider: "azure"
```

```bash
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://..."
export AZURE_OPENAI_DEPLOYMENT="..."
```

### Local Model (No API Key Needed!)

```yaml
# config.yaml
llm:
  provider: "local"
```

```bash
# Install llama.cpp
pip install llama-cpp-python

# Download a model (e.g., from Hugging Face)
# Set path
export LOCAL_MODEL_PATH="/path/to/model.gguf"
```

## What Can Jarvis Do?

Out of the box, Jarvis can:

1. **Search Wikipedia** - Get factual information
   - "Tell me about quantum computing"
   
2. **Open Websites** - Launch sites in your browser
   - "Open YouTube"
   - "Open GitHub"
   
3. **Tell Time** - Get current time
   - "What time is it?"
   
4. **Weather Info** - Check weather (requires OpenWeatherMap API key)
   - "What's the weather in London?"

5. **Conversational AI** - Natural language understanding
   - Multi-turn conversations
   - Context awareness
   - Automatic skill selection

## Troubleshooting

### "No module named 'speech_recognition'"

```bash
pip install SpeechRecognition
```

### "OpenAI API key not configured"

```bash
export OPENAI_API_KEY="your-key"
```

### Voice recognition not working

Make sure you have a microphone connected and:
```bash
# On Linux, you may need:
sudo apt-get install python3-pyaudio portaudio19-dev

# Then reinstall:
pip install --upgrade pyaudio
```

### Tests failing

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run tests with verbose output
python -m unittest discover -s tests -p "test_*.py" -v
```

## Next Steps

1. **Add Skills**: See `INTEGRATION_GUIDE.md` for how to add new capabilities

2. **Customize Persona**: Edit `src/jarvis/agents/prompts.py`

3. **Configure Weather**: Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
   ```bash
   export OPENWEATHERMAP_API_KEY="your-key"
   ```

4. **Explore Advanced Features**: Check out `INTEGRATION_GUIDE.md`

## Development

### Run Tests

```bash
./run_tests.sh
# or
python -m unittest discover -s tests -p "test_*.py" -v
```

### Add a New Skill

1. Create skill in `src/jarvis/skills/my_skill.py`
2. Register in `src/jarvis/skills/__init__.py`
3. Add to Jarvis in `src/jarvis/jarvis.py`
4. Write tests in `tests/test_skills.py`

See `INTEGRATION_GUIDE.md` for detailed instructions.

## Support & Documentation

- **README.md** - Project overview
- **INTEGRATION_GUIDE.md** - Detailed integration guide
- **ACCEPTANCE_CRITERIA.md** - Verification of features
- **config.yaml** - Configuration reference

## Tips

1. **Use GPT-4 for best results** - Better reasoning and tool usage
2. **Start with demo.py** - No API key needed, shows all features
3. **Check logs** - `logs/` directory has conversation and decision logs
4. **Mock in tests** - Use `MockLLMService` for fast, predictable tests
5. **Environment variables** - Keep secrets out of config files

## Example Conversation

```
You: Hello Jarvis
Jarvis: Good afternoon! I am Jarvis. How can I help you?

You: What time is it and open YouTube
Jarvis: [Calls get_current_time and open_website]
        The current time is 14:32:15. I've opened YouTube for you.

You: Search for Python programming language
Jarvis: [Calls search_wikipedia]
        According to Wikipedia, Python is a high-level, interpreted 
        programming language known for its simplicity...

You: Who created it?
Jarvis: [Uses context from previous message]
        Python was created by Guido van Rossum and first released in 1991.
```

## Need Help?

Check the logs:
```bash
cat logs/conversations.log
cat logs/decisions.log
```

Run the demo to verify setup:
```bash
python demo.py
```

---

**Ready to go!** Start with `python demo.py` to see Jarvis in action, then move to `python main.py` for the full voice experience.
