# Quick Reference Card

## 🎤 Voice Commands

### Workflow Automation
```
"Jarvis, build automation to [description]"
"Jarvis, create workflow to [description]"
"Jarvis, set up [description]"
"Jarvis, list workflows"
"Jarvis, run workflow [name]"
"Jarvis, confirm workflow"
"Jarvis, cancel workflow"
```

### Examples
```
"Jarvis, build automation to send daily report at 9 AM"
"Jarvis, create workflow to sync calendar every hour"
"Jarvis, set up Slack notification when API fails"
```

## 💻 Python API

### Initialize
```python
from src.jarvis.integrations.n8n_client import N8nClient
from src.jarvis.workflow_builder import WorkflowBuilder

client = N8nClient("http://localhost:5678", api_key="key")
builder = WorkflowBuilder()
```

### Create Workflow
```python
workflow = builder.create_basic_workflow("My Workflow")
trigger = builder.add_trigger_node(workflow, "manual")
http = builder.add_http_request_node(workflow, "https://api.example.com")
builder.connect_nodes(workflow, trigger, http)
```

### Deploy
```python
is_valid, errors = client.validate_workflow(workflow)
if is_valid:
    result = client.create_workflow(workflow)
    print(f"Created: {result['id']}")
```

## 📝 Node Types

### Triggers
- `manual` - Manual execution
- `webhook` - HTTP webhook
- `schedule` - Cron schedule
- `interval` - Time interval

### Actions
- `add_http_request_node()` - HTTP requests
- `add_email_node()` - Send email
- `add_slack_node()` - Slack messages
- `add_code_node()` - JavaScript/Python code

### Logic
- `add_if_node()` - Conditional branching
- `add_set_node()` - Set variables

## 🔧 Configuration

### File: `config/n8n_config.json`
```json
{
  "base_url": "http://localhost:5678",
  "api_key": "your-api-key",
  "auth_token": null
}
```

### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."  # Optional, for LLM
```

## 🧪 Testing

```bash
# All tests
python -m unittest discover tests

# Specific suite
python -m unittest tests.test_n8n_client
python -m unittest tests.test_workflow_builder
python -m unittest tests.test_integration

# Run example
python example_workflow.py
```

## 📚 Documentation

- **README.md** - Project overview
- **WORKFLOWS.md** - Complete workflow guide
- **QUICKSTART.md** - Get started in 5 minutes
- **API_EXAMPLES.md** - Code examples
- **IMPLEMENTATION_SUMMARY.md** - Technical details

## 🚀 Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure (optional)
cp config/n8n_config.example.json config/n8n_config.json
# Edit with your n8n API key

# 3. Test
python example_workflow.py

# 4. Run
python -m src.jarvis.jarvis
```

## ⚠️ Troubleshooting

### Connection Failed
```bash
# Check if n8n is running
curl http://localhost:5678/api/v1/workflows

# Test connection
python -c "from src.jarvis.integrations.n8n_client import N8nClient; \
           print(N8nClient('http://localhost:5678', api_key='key').test_connection())"
```

### Import Errors
```bash
# Check dependencies
pip install -r requirements.txt

# Verify structure
ls -la src/jarvis/
```

## 🎯 Common Patterns

### Daily Report
```python
workflow = builder.create_sample_daily_report_workflow()
# Schedule → HTTP → Code → Email
```

### API Monitor
```python
workflow = builder.create_basic_workflow("Monitor")
trigger = builder.add_trigger_node(workflow, "interval", {"interval": 5})
http = builder.add_http_request_node(workflow, "https://api.example.com/health")
alert = builder.add_slack_node(workflow, "#alerts", "Status: {{$json.status}}")
```

### Conditional Logic
```python
if_node = builder.add_if_node(workflow, [{
    "leftValue": "{{$json.status}}",
    "rightValue": "ok",
    "operator": "equals"
}])
builder.connect_nodes(workflow, source, if_node)
builder.connect_nodes(workflow, if_node, success_node, output_index=0)
builder.connect_nodes(workflow, if_node, failure_node, output_index=1)
```

## 📊 Validation

```python
is_valid, errors = client.validate_workflow(workflow)
if not is_valid:
    print("Errors:", errors)
```

## 🔍 Preview

```python
preview = client.get_workflow_preview(workflow)
print(preview)
```

## ✨ Tips

1. Always validate before deploying
2. Use manual triggers for testing
3. Review previews before confirming
4. Keep workflows inactive until tested
5. Monitor execution logs
6. Use descriptive workflow names

## 📞 Support

- Check documentation files
- Run example script
- Review test files for patterns
- Open GitHub issue

---

**Version:** 2.0.0  
**Last Updated:** October 2025  
**Status:** Production Ready
