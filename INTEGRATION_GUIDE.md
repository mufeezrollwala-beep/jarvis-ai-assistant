# LLM Agent Integration Guide

This guide explains how the LLM agent integration works in Jarvis and how to use it.

## Overview

The Jarvis AI Assistant now includes a sophisticated LLM agent system that enables:
- Autonomous reasoning and decision-making
- Automatic tool/skill invocation based on context
- Multi-turn conversations with memory
- Easy switching between LLM providers (OpenAI, Azure, Local)

## Architecture

### Core Components

1. **LLMService**: Abstract interface for different LLM providers
2. **AgentManager**: Orchestrates the LLM, manages conversation history, and handles tool calling
3. **Skills**: Modular capabilities that can be invoked by the LLM
4. **Config**: YAML-based configuration system

### Flow

```
User Input → AgentManager → LLMService → LLM API
                ↓
         Tool Definitions
                ↓
         LLM Response (with tool calls)
                ↓
         Execute Skills
                ↓
         Return Results to LLM
                ↓
         Final Response to User
```

## Switching LLM Providers

### Using OpenAI

Edit `config.yaml`:

```yaml
llm:
  provider: "openai"
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4o"  # or "gpt-4", "gpt-3.5-turbo"
    temperature: 0.7
    max_tokens: 2000
```

Set environment variable:
```bash
export OPENAI_API_KEY="sk-..."
```

### Using Azure OpenAI

Edit `config.yaml`:

```yaml
llm:
  provider: "azure"
  azure:
    api_key: "${AZURE_OPENAI_API_KEY}"
    endpoint: "${AZURE_OPENAI_ENDPOINT}"
    deployment_name: "${AZURE_OPENAI_DEPLOYMENT}"
    api_version: "2024-02-15-preview"
    temperature: 0.7
    max_tokens: 2000
```

Set environment variables:
```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
```

### Using Local Models

Edit `config.yaml`:

```yaml
llm:
  provider: "local"
  local:
    model_path: "${LOCAL_MODEL_PATH}"
    context_size: 4096
    temperature: 0.7
    max_tokens: 2000
    gpu_layers: 35  # Number of layers to offload to GPU
```

Set environment variable:
```bash
export LOCAL_MODEL_PATH="/path/to/model.gguf"
```

**Note**: Local models require `llama-cpp-python` to be installed. This is optional in requirements.txt.

## Adding New Skills

### 1. Create Skill Class

Create a new file in `src/jarvis/skills/`:

```python
from typing import Dict, Any
from .base_skill import BaseSkill, SkillResult


class CalculatorSkill(BaseSkill):
    def get_name(self) -> str:
        return "calculate"
    
    def get_description(self) -> str:
        return "Perform basic arithmetic calculations"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2')",
                }
            },
            "required": ["expression"],
        }
    
    def execute(self, expression: str, **kwargs) -> SkillResult:
        try:
            result = eval(expression)
            return SkillResult(success=True, result=result)
        except Exception as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Error evaluating expression: {str(e)}"
            )
```

### 2. Register Skill

Update `src/jarvis/skills/__init__.py`:

```python
from .calculator_skill import CalculatorSkill

__all__ = [
    "BaseSkill",
    "SkillResult",
    "WikipediaSkill",
    "WebBrowserSkill",
    "TimeSkill",
    "WeatherSkill",
    "CalculatorSkill",  # Add new skill
]
```

Update `src/jarvis/jarvis.py` in the `_setup_agent` method:

```python
def _setup_agent(self):
    # ... existing code ...
    
    skills = [
        WikipediaSkill(),
        WebBrowserSkill(),
        TimeSkill(),
        WeatherSkill(api_key=weather_api_key, default_city=default_city),
        CalculatorSkill(),  # Add new skill
    ]
    
    self.agent = AgentManager(
        llm_service=self.llm_service,
        skills=skills,
        logger=self.decision_logger,
    )
```

### 3. Write Tests

Create tests in `tests/test_skills.py`:

```python
class TestCalculatorSkill(unittest.TestCase):
    def setUp(self):
        self.skill = CalculatorSkill()
    
    def test_simple_calculation(self):
        result = self.skill.execute(expression="2 + 2")
        self.assertTrue(result.success)
        self.assertEqual(result.result, 4)
    
    def test_invalid_expression(self):
        result = self.skill.execute(expression="invalid")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
```

## Tool Calling Flow

### How It Works

1. **User sends message**: "What time is it and open YouTube"

2. **AgentManager processes message**: Adds to conversation history, sends to LLM with tool definitions

3. **LLM analyzes and responds**: Returns tool calls:
   ```json
   [
     {"function": {"name": "get_current_time", "arguments": "{}"}},
     {"function": {"name": "open_website", "arguments": "{\"site\": \"youtube\"}"}}
   ]
   ```

4. **AgentManager executes tools**: Calls each skill's `execute()` method

5. **Results added to history**: Tool results are appended to conversation

6. **LLM generates final response**: With tool results as context

7. **User receives response**: "The current time is 14:30:00. I've opened YouTube for you."

## Testing

### Unit Tests

Test individual components:

```bash
python -m unittest tests.test_skills
python -m unittest tests.test_config
```

### Integration Tests

Test the full agent pipeline with mock LLM:

```bash
python -m unittest tests.test_agent_manager
python -m unittest tests.test_integration
```

### All Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Demo Without API Keys

Run the demo script to see agent behavior without real API calls:

```bash
python demo.py
```

## Logging

### Configuration

Logging is configured in `config.yaml`:

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  conversation_log: "logs/conversations.log"
  decision_log: "logs/decisions.log"
  mask_sensitive: true
  sensitive_patterns:
    - "api[_-]?key"
    - "password"
    - "token"
    - "secret"
```

### Log Files

- **conversations.log**: User interactions and responses
- **decisions.log**: Agent reasoning, tool calls, and execution results

### Sensitive Data Masking

API keys and other sensitive data matching the patterns are automatically masked in logs as `***MASKED***`.

## Best Practices

### 1. Skill Design

- Keep skills focused and single-purpose
- Provide clear, descriptive names and descriptions
- Use proper error handling and return meaningful error messages
- Validate inputs in the `execute()` method

### 2. Prompt Engineering

The system prompt in `src/jarvis/agents/prompts.py` defines Jarvis's personality and behavior. Customize it for your use case:

```python
JARVIS_SYSTEM_PROMPT = """You are Jarvis, an advanced AI assistant...

Your capabilities:
- List your skills here
- Be specific about what you can and cannot do

Guidelines:
1. When to use tools
2. How to respond to users
3. Safety considerations
"""
```

### 3. Configuration Management

- Use environment variables for secrets
- Keep `config.yaml` in version control (without secrets)
- Use `config.local.yaml` for local development (add to .gitignore)
- Provide `.env.example` for required environment variables

### 4. Testing Strategy

- Mock LLM service for predictable tests
- Test each skill independently
- Test agent flow with various scenarios
- Test multi-turn conversations
- Test error handling

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'speech_recognition'"

**Solution**: Install with correct package name:
```bash
pip install SpeechRecognition
```

### Issue: LLM not calling tools

**Possible causes**:
1. Tool descriptions are not clear enough
2. LLM model doesn't support function calling (use GPT-4 or GPT-3.5-turbo-0613+)
3. System prompt conflicts with tool usage

**Solution**: Improve tool descriptions and ensure compatible model.

### Issue: "OpenAI API key not configured"

**Solution**: Set environment variable:
```bash
export OPENAI_API_KEY="your-key-here"
```

Or update config.yaml directly (not recommended for production).

### Issue: Local model not loading

**Possible causes**:
1. `llama-cpp-python` not installed
2. Model path incorrect
3. Insufficient memory/GPU

**Solution**: 
```bash
pip install llama-cpp-python
export LOCAL_MODEL_PATH="/correct/path/to/model.gguf"
```

## Example Usage

### With Voice Interface

```bash
python main.py
```

Speak commands like:
- "What time is it?"
- "Search Wikipedia for quantum computing"
- "Open YouTube and tell me the weather"

### Programmatic Usage

```python
from jarvis import Jarvis
from jarvis.config import load_config

config = load_config()
jarvis = Jarvis(config)

# Process text commands directly
response = jarvis.agent.process_message("What can you do?")
print(response)
```

## Performance Considerations

### Response Time

- **OpenAI API**: ~1-3 seconds per request
- **Azure OpenAI**: ~1-3 seconds per request  
- **Local Model**: ~0.5-5 seconds depending on hardware

### Token Usage

Monitor token usage for API-based providers:
- System prompt: ~150 tokens
- Tool definitions: ~50-100 tokens per skill
- Conversation history grows over time (consider truncation for long sessions)

### Cost Optimization

1. Use GPT-3.5-turbo for simpler tasks
2. Truncate conversation history after N turns
3. Use local models for development/testing
4. Cache frequent queries (not implemented yet)

## Next Steps

1. **Add more skills**: File operations, email, calendar, etc.
2. **Implement conversation truncation**: For long sessions
3. **Add caching**: For expensive API calls
4. **Enhance error recovery**: Retry logic, fallbacks
5. **Add streaming responses**: For real-time feedback
6. **Implement tool chaining**: Complex multi-step operations

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Run tests to verify setup
3. Review configuration in `config.yaml`
4. Check API key environment variables
