# n8n Workflow Automation with Jarvis

## Overview

Jarvis now integrates deeply with n8n to provide voice-controlled workflow automation. You can generate, preview, and trigger workflows using natural language commands.

## Setup

### 1. Install n8n

```bash
# Using npm
npm install n8n -g

# Or using Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

### 2. Configure n8n Connection

1. Start n8n: `n8n start`
2. Access n8n at http://localhost:5678
3. Go to **Settings** > **API** > **Generate API Key**
4. Copy `config/n8n_config.example.json` to `config/n8n_config.json`
5. Add your API key to the config file

```json
{
  "base_url": "http://localhost:5678",
  "api_key": "your-api-key-here",
  "auth_token": null
}
```

### 3. Optional: Configure OpenAI for Advanced Workflow Generation

For more sophisticated workflow generation using LLM:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

Without OpenAI, Jarvis uses template-based workflow generation which covers common scenarios.

## Voice Commands

### Build Automation

Create new workflows using natural language:

```
"Jarvis, build automation to send daily report at 9 AM"
"Jarvis, create workflow to sync calendar every hour"
"Jarvis, set up Slack notification when API fails"
```

The system will:
1. Generate a workflow based on your description
2. Display a preview with node structure
3. Ask for confirmation before deploying

### Review and Confirm

After building a workflow, review it and confirm:

```
"Jarvis, confirm workflow"  # Deploy the workflow
"Jarvis, cancel workflow"   # Discard the workflow
```

### List Workflows

View all your n8n workflows:

```
"Jarvis, list workflows"
"Jarvis, show workflows"
```

### Execute Workflows

Run active workflows manually:

```
"Jarvis, run workflow Daily Report"
"Jarvis, execute workflow Calendar Sync"
```

## Sample Scenarios

### 1. Daily Report Email

**Command:** "Jarvis, build automation to send daily report email at 9 AM"

**Generated Workflow:**
- Schedule trigger (Cron: 0 9 * * *)
- HTTP Request to fetch data
- Code node to format report
- Email node to send report

### 2. Calendar Sync

**Command:** "Jarvis, create workflow to sync calendar events"

**Generated Workflow:**
- Interval trigger (every hour)
- HTTP Request to calendar API
- Code node to filter upcoming events
- Slack notification for new events

### 3. API Monitoring

**Command:** "Jarvis, set up monitoring for API health checks"

**Generated Workflow:**
- Interval trigger (every 5 minutes)
- HTTP Request to health endpoint
- IF node to check status
- Slack/Email alert on failure

## Workflow Preview

Before deploying, Jarvis shows a detailed preview:

```
============================================================
WORKFLOW PREVIEW
============================================================
Workflow: Daily Report
Active: False
Nodes: 4

Node Structure:
  - Trigger_node_1 (n8n-nodes-base.cron)
    Parameters: ['cronExpression']
  - HTTP_Request_node_2 (n8n-nodes-base.httpRequest)
    Parameters: ['url', 'method', 'options']
  - Code_node_3 (n8n-nodes-base.code)
    Parameters: ['mode', 'jsCode']
  - Email_node_4 (n8n-nodes-base.emailSend)
    Parameters: ['toEmail', 'subject', 'text']

Connections:
  Trigger_node_1 ->
    -> HTTP_Request_node_2
  HTTP_Request_node_2 ->
    -> Code_node_3
  Code_node_3 ->
    -> Email_node_4
============================================================
```

## Safety Features

### Dry-Run Preview

All workflows are created in **inactive** state by default. You must:
1. Review the workflow structure
2. Confirm deployment
3. Manually activate in n8n UI or via voice command

### Validation

Before deployment, workflows are validated for:
- Required fields (name, nodes, connections)
- Node structure integrity
- Connection references
- Duplicate node names

### Error Handling

- API connection failures are reported
- Invalid workflow structures are rejected
- Execution errors are logged with details

## Programmatic Usage

You can also use the n8n integration programmatically:

```python
from src.jarvis.integrations.n8n_client import N8nClient
from src.jarvis.workflow_builder import WorkflowBuilder

# Initialize client
client = N8nClient(
    base_url="http://localhost:5678",
    api_key="your-api-key"
)

# List workflows
workflows = client.list_workflows()

# Create workflow
builder = WorkflowBuilder()
workflow = builder.create_sample_daily_report_workflow()
result = client.create_workflow(workflow)

# Execute workflow
client.execute_workflow(result['id'])
```

## Node Types Supported

The workflow builder supports common n8n node types:

- **Triggers:** Manual, Webhook, Schedule (Cron), Interval
- **Actions:** HTTP Request, Email, Slack, Code (JS/Python)
- **Logic:** IF conditions, Set variables
- **Data:** Transform, Filter, Merge

## Troubleshooting

### Connection Issues

```python
# Test connection
if client.test_connection():
    print("Connected to n8n")
else:
    print("Failed to connect - check config")
```

### Workflow Not Found

Ensure workflows are active:
- Check in n8n UI
- Use `list workflows` command
- Verify workflow names match

### Execution Failures

View execution logs:
- Check n8n UI > Executions
- Review node-specific errors
- Verify API credentials and endpoints

## Advanced Features

### Custom Node Parameters

Customize workflow generation:

```python
builder = WorkflowBuilder()
workflow = builder.create_basic_workflow("Custom Workflow")

# Add custom HTTP node
node = builder.add_http_request_node(
    workflow,
    url="https://api.example.com/data",
    method="POST",
    headers={"Authorization": "Bearer token"},
    body={"key": "value"}
)
```

### Conditional Logic

Add IF nodes for branching:

```python
conditions = [
    {
        "leftValue": "{{$json.status}}",
        "rightValue": "success",
        "operator": "equals"
    }
]
if_node = builder.add_if_node(workflow, conditions)

# Connect to different branches
builder.connect_nodes(workflow, if_node, success_node, output_index=0)
builder.connect_nodes(workflow, if_node, failure_node, output_index=1)
```

### LLM-Enhanced Generation

With OpenAI API key configured:

```python
builder = WorkflowBuilder(llm_api_key="your-openai-key")
workflow = builder.generate_workflow_with_llm(
    "Create a workflow that monitors Twitter mentions and sends them to Slack"
)
```

## Best Practices

1. **Start Simple:** Begin with basic workflows before adding complexity
2. **Test Manually:** Use manual trigger during development
3. **Review Previews:** Always review workflow structure before deployment
4. **Incremental Changes:** Update existing workflows rather than recreating
5. **Monitor Executions:** Check execution logs regularly
6. **Use Inactive Mode:** Keep workflows inactive until fully tested

## Examples Repository

Pre-built sample workflows:

```python
from src.jarvis.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder()

# Daily report
daily_report = builder.create_sample_daily_report_workflow()

# Calendar sync
calendar_sync = builder.create_sample_calendar_sync_workflow()
```

## API Reference

### N8nClient Methods

- `list_workflows(active=None)` - List all workflows
- `get_workflow(workflow_id)` - Get specific workflow
- `create_workflow(workflow_data)` - Create new workflow
- `update_workflow(workflow_id, workflow_data)` - Update workflow
- `delete_workflow(workflow_id)` - Delete workflow
- `execute_workflow(workflow_id, data=None)` - Execute workflow
- `activate_workflow(workflow_id)` - Activate workflow
- `deactivate_workflow(workflow_id)` - Deactivate workflow
- `get_executions(workflow_id=None, limit=20)` - Get execution history
- `validate_workflow(workflow_data)` - Validate workflow structure
- `get_workflow_preview(workflow_data)` - Generate text preview

### WorkflowBuilder Methods

- `create_basic_workflow(name, description)` - Create empty workflow
- `add_trigger_node(workflow, trigger_type, parameters)` - Add trigger
- `add_http_request_node(workflow, url, method, headers, body)` - Add HTTP request
- `add_email_node(workflow, to, subject, text, html)` - Add email
- `add_slack_node(workflow, channel, message)` - Add Slack notification
- `add_code_node(workflow, code, language)` - Add code execution
- `add_if_node(workflow, conditions)` - Add conditional logic
- `add_set_node(workflow, values)` - Add variable setting
- `connect_nodes(workflow, source, target, output_index, input_index)` - Connect nodes
- `organize_layout(workflow)` - Auto-arrange node positions
- `parse_natural_language_spec(spec)` - Generate from text description

## Support

For issues or questions:
1. Check n8n documentation: https://docs.n8n.io
2. Review error messages in console
3. Test connection with `test_connection()` method
4. Verify API key and base URL configuration
