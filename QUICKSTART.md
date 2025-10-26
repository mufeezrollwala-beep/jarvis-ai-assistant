# Quick Start Guide - n8n Workflow Integration

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up n8n (Optional)

If you want to deploy workflows:

```bash
# Option A: Using npm
npm install n8n -g
n8n start

# Option B: Using Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

### 3. Configure n8n Connection

```bash
cp config/n8n_config.example.json config/n8n_config.json
# Edit config/n8n_config.json with your n8n API key
```

To get your API key:
1. Open n8n at http://localhost:5678
2. Go to Settings → API
3. Generate API Key
4. Paste it into `config/n8n_config.json`

### 4. Try the Examples

```bash
python example_workflow.py
```

This demonstrates:
- Creating workflows from templates
- Generating workflows from natural language
- Building custom workflows
- Validating workflows

### 5. Run Jarvis

```bash
python -m src.jarvis.jarvis
```

Or:

```bash
cd src/jarvis
python jarvis.py
```

## 🎤 Voice Commands

### Build Workflows

```
"Jarvis, build automation to send daily report at 9 AM"
"Jarvis, create workflow to sync calendar every hour"
"Jarvis, set up Slack notification when API fails"
```

### Manage Workflows

```
"Jarvis, list workflows"
"Jarvis, run workflow Daily Report"
"Jarvis, confirm workflow"  # After building
"Jarvis, cancel workflow"   # Discard pending workflow
```

### Other Commands

```
"Wikipedia artificial intelligence"
"What's the time?"
"Open YouTube"
"Exit"
```

## 🧪 Run Tests

```bash
# All tests
python -m unittest discover tests

# Specific test suite
python -m unittest tests.test_n8n_client
python -m unittest tests.test_workflow_builder
python -m unittest tests.test_integration

# With pytest (if installed)
pytest tests/
```

## 📝 Example Workflows

### Daily Email Report

**Voice:** "Jarvis, set up daily email report at 9 AM"

**Creates:**
- Schedule trigger (cron: 0 9 * * *)
- HTTP request to fetch data
- Code node to format report
- Email node to send

### Calendar Sync

**Voice:** "Jarvis, sync calendar events every hour"

**Creates:**
- Interval trigger (60 minutes)
- HTTP request to calendar API
- Code node to filter events
- Slack notification

### API Monitor

**Voice:** "Jarvis, monitor API and alert on failure"

**Creates:**
- Interval trigger
- HTTP health check
- IF condition
- Alert on failure

## 🔧 Troubleshooting

### No microphone detected

```bash
# List available microphones
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### n8n connection failed

Check if n8n is running:
```bash
curl http://localhost:5678/api/v1/workflows
```

### Import errors

Make sure you're in the project directory and dependencies are installed:
```bash
cd /home/engine/project
pip install -r requirements.txt
```

## 📚 Documentation

- **[README.md](README.md)** - Full project documentation
- **[WORKFLOWS.md](WORKFLOWS.md)** - Complete workflow guide
- **[example_workflow.py](example_workflow.py)** - Code examples

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Run example script
3. ✅ Configure n8n (optional)
4. ✅ Try voice commands
5. 📖 Read WORKFLOWS.md for advanced features
6. 🔨 Build custom workflows
7. 🚀 Deploy to production

## 💡 Tips

- Start with `example_workflow.py` to understand the API
- Use manual triggers during development
- Review workflow previews before deploying
- Keep workflows inactive until tested
- Monitor execution logs in n8n UI

## 🆘 Need Help?

- Check [WORKFLOWS.md](WORKFLOWS.md) for detailed documentation
- Review test files for code examples
- Run `python example_workflow.py` for demonstrations
- Open an issue on GitHub

Happy automating! 🤖
