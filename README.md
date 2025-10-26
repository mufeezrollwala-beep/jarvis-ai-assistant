# Jarvis AI Assistant

Advanced AI voice assistant inspired by Iron Man's JARVIS, featuring deep n8n integration for workflow automation.

## Features

- 🎤 **Voice Recognition** - Speak naturally to Jarvis
- 🔊 **Text-to-Speech** - Jarvis responds with voice
- 🔍 **Wikipedia Integration** - Quick information lookup
- 🌐 **Web Control** - Open YouTube, Google, and more
- 🌤️ **Weather Reports** - Current weather information
- ⚙️ **Workflow Automation** - Create and manage n8n workflows via voice
- 🤖 **LLM-Enhanced** - Optional OpenAI integration for advanced workflow generation

## New: n8n Workflow Integration

Jarvis now provides deep integration with n8n for workflow automation:

- 🎯 **Voice-Controlled Workflows** - Generate workflows using natural language
- 👀 **Preview & Confirm** - Review workflows before deployment
- 🔄 **Execute Workflows** - Run automations on demand
- 📋 **Manage Workflows** - List, activate, and monitor workflows
- 🛡️ **Safety Checks** - Dry-run previews and user confirmation

See [WORKFLOWS.md](WORKFLOWS.md) for complete documentation.

## Installation

### Prerequisites

- Python 3.8+
- Microphone for voice input
- n8n instance (optional, for workflow features)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure n8n (optional):
```bash
# Copy example config
cp config/n8n_config.example.json config/n8n_config.json

# Edit with your n8n details
# Add your n8n API key
```

4. Set up API keys:
```bash
# For weather (optional)
# Edit src/jarvis/jarvis.py and add your OpenWeatherMap API key

# For advanced workflow generation (optional)
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage

### Basic Usage

Run Jarvis:
```bash
python -m src.jarvis.jarvis
```

Or directly:
```bash
cd src/jarvis
python jarvis.py
```

### Voice Commands

**Information:**
- "Wikipedia artificial intelligence"
- "What's the time?"
- "What's the weather?"

**Web Browsing:**
- "Open YouTube"
- "Open Google"

**Workflow Automation:**
- "Jarvis, build automation to send daily report at 9 AM"
- "Jarvis, create workflow to sync calendar every hour"
- "Jarvis, list workflows"
- "Jarvis, run workflow Daily Report"
- "Jarvis, confirm workflow" (after building)

**Exit:**
- "Exit"

## Architecture

```
jarvis-ai-assistant/
├── src/jarvis/
│   ├── jarvis.py              # Main Jarvis class
│   ├── workflow_builder.py    # Workflow generation
│   └── integrations/
│       └── n8n_client.py      # n8n API client
├── tests/
│   ├── test_n8n_client.py     # Client tests
│   └── test_workflow_builder.py # Builder tests
├── config/
│   └── n8n_config.example.json # Config template
├── WORKFLOWS.md                # Workflow documentation
└── requirements.txt            # Dependencies
```

## Workflow Examples

### Daily Report

```
"Jarvis, set up daily report email at 9 AM"
```

Generates:
- Schedule trigger (9 AM daily)
- HTTP request to fetch data
- Code node to format report
- Email node to send

### Calendar Sync

```
"Jarvis, create workflow to sync calendar every hour"
```

Generates:
- Interval trigger (hourly)
- Calendar API request
- Event filtering
- Slack notifications

## Testing

Run unit tests:

```bash
# All tests
python -m pytest tests/

# Specific test file
python -m pytest tests/test_n8n_client.py

# With coverage
python -m pytest --cov=src/jarvis tests/
```

Or using unittest:

```bash
python -m unittest tests.test_n8n_client
python -m unittest tests.test_workflow_builder
```

## Configuration

### n8n Configuration

`config/n8n_config.json`:
```json
{
  "base_url": "http://localhost:5678",
  "api_key": "your-api-key-here",
  "auth_token": null
}
```

### Environment Variables

- `OPENAI_API_KEY` - For LLM-enhanced workflow generation (optional)
- `N8N_API_KEY` - Alternative to config file

## API Reference

### N8nClient

```python
from src.jarvis.integrations.n8n_client import N8nClient

client = N8nClient(base_url="http://localhost:5678", api_key="key")

# List workflows
workflows = client.list_workflows()

# Create workflow
workflow = client.create_workflow(workflow_data)

# Execute workflow
client.execute_workflow(workflow_id)
```

### WorkflowBuilder

```python
from src.jarvis.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder()

# Create from template
workflow = builder.create_sample_daily_report_workflow()

# Create from natural language
workflow = builder.parse_natural_language_spec("send daily email")

# Create custom
workflow = builder.create_basic_workflow("My Workflow")
trigger = builder.add_trigger_node(workflow, "schedule")
email = builder.add_email_node(workflow, "user@example.com", "Subject", "Body")
builder.connect_nodes(workflow, trigger, email)
```

## Development

### Project Structure

- **jarvis.py** - Main assistant with voice control and command processing
- **n8n_client.py** - REST API client for n8n with validation
- **workflow_builder.py** - Converts natural language to n8n JSON
- **tests/** - Comprehensive unit tests with mocking

### Adding New Commands

1. Add command detection in `process_command()`
2. Create handler method (e.g., `_handle_new_command()`)
3. Add tests in appropriate test file

### Adding New Node Types

1. Add method to `WorkflowBuilder` (e.g., `add_custom_node()`)
2. Update `parse_natural_language_spec()` with keywords
3. Add tests in `test_workflow_builder.py`

## Troubleshooting

### Microphone Issues

```bash
# Test microphone
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### n8n Connection

```python
# Test connection
from src.jarvis.integrations.n8n_client import N8nClient
client = N8nClient(base_url="http://localhost:5678", api_key="key")
print(client.test_connection())
```

### Voice Recognition Not Working

- Check microphone permissions
- Ensure internet connection (Google Speech API)
- Adjust `pause_threshold` in `take_command()`

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by Marvel's Iron Man JARVIS
- Built with Python, n8n, and open-source libraries
- Speech recognition powered by Google Speech API
- Text-to-speech using pyttsx3

## Roadmap

- [ ] Support for more n8n node types
- [ ] Workflow templates library
- [ ] Multi-language support
- [ ] Web dashboard
- [ ] Mobile app integration
- [ ] Advanced LLM workflow planning
- [ ] Workflow versioning and rollback
- [ ] Real-time execution monitoring

## Support

For questions or issues:
- 📖 Read [WORKFLOWS.md](WORKFLOWS.md) for workflow documentation
- 🐛 Open an issue on GitHub
- 💬 Join our community discussions
