# Jarvis AI Assistant

Advanced AI assistant inspired by Iron Man's JARVIS, now powered by configurable Large Language Model agents for autonomous reasoning and skill orchestration.

## Features

- 🤖 **LLM-Powered Agent**: Autonomous reasoning and decision-making using GPT-4, Azure OpenAI, or local models
- 🎯 **Multi-Turn Conversations**: Maintains context across conversation history
- 🛠️ **Extensible Skills System**: Modular architecture for adding new capabilities
- 🔊 **Voice Interface**: Speech recognition and text-to-speech
- 🔧 **Tool Calling**: LLM can automatically invoke registered skills
- 📝 **Comprehensive Logging**: Track conversations and decisions with sensitive data masking
- ⚙️ **Flexible Configuration**: Switch between LLM providers with config changes only

## Built-in Skills

- **Wikipedia Search**: Query Wikipedia for factual information
- **Web Browser**: Open websites (YouTube, Google, etc.)
- **Time**: Get current time
- **Weather**: Retrieve weather information for cities

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

4. Configure your settings:
```bash
cp config.yaml config.local.yaml
# Edit config.local.yaml with your API keys
```

## Configuration

The system uses a YAML configuration file. Key settings:

### LLM Provider Selection

```yaml
llm:
  provider: "openai"  # Options: openai, azure, local
```

### OpenAI Configuration

```yaml
llm:
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4o"
    temperature: 0.7
    max_tokens: 2000
```

### Azure OpenAI Configuration

```yaml
llm:
  azure:
    api_key: "${AZURE_OPENAI_API_KEY}"
    endpoint: "${AZURE_OPENAI_ENDPOINT}"
    deployment_name: "${AZURE_OPENAI_DEPLOYMENT}"
    api_version: "2024-02-15-preview"
```

### Local Model Configuration

```yaml
llm:
  local:
    model_path: "${LOCAL_MODEL_PATH}"
    context_size: 4096
    temperature: 0.7
    max_tokens: 2000
    gpu_layers: 35
```

### Environment Variables

Set these environment variables or use them in config.yaml:

```bash
export OPENAI_API_KEY="your-openai-key"
export OPENWEATHERMAP_API_KEY="your-weather-key"
```

## Usage

Run the assistant:

```bash
python main.py
```

The assistant will greet you and start listening for commands. Example interactions:

- "What time is it?"
- "Search Wikipedia for quantum computing"
- "Open YouTube"
- "What's the weather in New York?"
- "Tell me about Python and open Google"

## Architecture

### Components

- **LLMService**: Abstract interface for LLM providers
  - `OpenAIService`: OpenAI GPT models
  - `AzureOpenAIService`: Azure OpenAI deployment
  - `LocalModelService`: Local models via llama.cpp

- **AgentManager**: Orchestrates LLM, skills, and conversation flow
  - Maintains conversation history
  - Manages tool calling pipeline
  - Handles multi-turn reasoning

- **Skills**: Modular capabilities
  - Each skill defines parameters and execution logic
  - Automatically converted to tool definitions for LLM

- **Config**: YAML-based configuration with environment variable expansion

- **Logging**: Structured logging with sensitive data masking

### Adding New Skills

1. Create a new skill class in `src/jarvis/skills/`:

```python
from .base_skill import BaseSkill, SkillResult

class MySkill(BaseSkill):
    def get_name(self) -> str:
        return "my_skill"
    
    def get_description(self) -> str:
        return "Description of what my skill does"
    
    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        }
    
    def execute(self, param1: str, **kwargs) -> SkillResult:
        # Implementation
        return SkillResult(success=True, result="Result")
```

2. Register the skill in `src/jarvis/jarvis.py`:

```python
from .skills import MySkill

# In _setup_agent method:
skills = [
    WikipediaSkill(),
    MySkill(),
    # ... other skills
]
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run specific tests:

```bash
python -m pytest tests/test_agent_manager.py
python -m pytest tests/test_skills.py
python -m pytest tests/test_integration.py
```

The tests use a mock LLM service to validate:
- Skill execution
- Tool calling flow
- Multi-turn conversations
- Configuration loading

## Project Structure

```
jarvis-ai-assistant/
├── src/
│   └── jarvis/
│       ├── agents/          # Agent manager and prompts
│       ├── config/          # Configuration loader
│       ├── services/        # LLM service implementations
│       ├── skills/          # Skill implementations
│       └── utils/           # Logging and utilities
├── tests/                   # Unit and integration tests
├── config.yaml             # Configuration template
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Development

### Code Style

- Follow PEP 8 conventions
- Use type hints where applicable
- Document public methods and classes

### Contributing

1. Create a feature branch
2. Implement your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License

## Acknowledgments

Inspired by Iron Man's JARVIS assistant with modern LLM capabilities for autonomous reasoning and tool use.
