# API Examples

This document provides code examples for using the n8n integration programmatically.

## Table of Contents

1. [N8nClient Examples](#n8nclient-examples)
2. [WorkflowBuilder Examples](#workflowbuilder-examples)
3. [Complete Integration Examples](#complete-integration-examples)

## N8nClient Examples

### Initialize Client

```python
from src.jarvis.integrations.n8n_client import N8nClient

# Using API key
client = N8nClient(
    base_url="http://localhost:5678",
    api_key="your-api-key-here"
)

# Using auth token
client = N8nClient(
    base_url="http://localhost:5678",
    auth_token="your-jwt-token"
)

# Test connection
if client.test_connection():
    print("Connected successfully!")
```

### List Workflows

```python
# List all workflows
all_workflows = client.list_workflows()

# List only active workflows
active_workflows = client.list_workflows(active=True)

# Print workflow names
for workflow in all_workflows:
    print(f"- {workflow['name']} (Active: {workflow.get('active', False)})")
```

### Get Workflow Details

```python
workflow_id = "abc123"
workflow = client.get_workflow(workflow_id)

print(f"Name: {workflow['name']}")
print(f"Nodes: {len(workflow['nodes'])}")
print(f"Active: {workflow['active']}")
```

### Create Workflow

```python
workflow_data = {
    "name": "My New Workflow",
    "nodes": [
        {
            "name": "Start",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {}
        }
    ],
    "connections": {},
    "active": False
}

result = client.create_workflow(workflow_data)
print(f"Created workflow with ID: {result['id']}")
```

### Update Workflow

```python
workflow_id = "abc123"
updates = {
    "name": "Updated Workflow Name",
    "active": True
}

updated = client.update_workflow(workflow_id, updates)
print(f"Updated: {updated['name']}")
```

### Activate/Deactivate Workflow

```python
# Activate
client.activate_workflow("abc123")
print("Workflow activated")

# Deactivate
client.deactivate_workflow("abc123")
print("Workflow deactivated")
```

### Execute Workflow

```python
# Execute without data
result = client.execute_workflow("abc123")
print(f"Execution ID: {result['executionId']}")

# Execute with input data
data = {"key": "value"}
result = client.execute_workflow("abc123", data=data)
```

### Get Executions

```python
# Get all recent executions
executions = client.get_executions(limit=10)

# Get executions for specific workflow
workflow_executions = client.get_executions(
    workflow_id="abc123",
    limit=20
)

for execution in executions:
    print(f"- {execution['id']}: {execution['status']}")
```

### Validate Workflow

```python
workflow_data = {
    "name": "Test Workflow",
    "nodes": [...],
    "connections": {...}
}

is_valid, errors = client.validate_workflow(workflow_data)

if is_valid:
    print("✓ Workflow is valid")
else:
    print("✗ Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Get Workflow Preview

```python
workflow_data = {...}
preview = client.get_workflow_preview(workflow_data)
print(preview)
```

## WorkflowBuilder Examples

### Create Basic Workflow

```python
from src.jarvis.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder()

workflow = builder.create_basic_workflow(
    name="My Workflow",
    description="A custom workflow"
)
```

### Add Trigger Nodes

```python
# Manual trigger
trigger = builder.add_trigger_node(workflow, "manual")

# Schedule trigger (cron)
trigger = builder.add_trigger_node(
    workflow,
    "schedule",
    {"cronExpression": "0 9 * * *"}  # 9 AM daily
)

# Interval trigger
trigger = builder.add_trigger_node(
    workflow,
    "interval",
    {"interval": 60}  # Every 60 minutes
)

# Webhook trigger
trigger = builder.add_trigger_node(
    workflow,
    "webhook",
    {"path": "my-webhook"}
)
```

### Add Action Nodes

```python
# HTTP Request
http_node = builder.add_http_request_node(
    workflow,
    url="https://api.example.com/data",
    method="POST",
    headers={"Authorization": "Bearer token"},
    body={"key": "value"}
)

# Email
email_node = builder.add_email_node(
    workflow,
    to="user@example.com",
    subject="Daily Report",
    text="Report content here"
)

# HTML Email
email_node = builder.add_email_node(
    workflow,
    to="user@example.com",
    subject="Daily Report",
    html="<h1>Report</h1><p>Content</p>"
)

# Slack
slack_node = builder.add_slack_node(
    workflow,
    channel="#general",
    message="Hello from Jarvis!"
)

# Code (JavaScript)
code_node = builder.add_code_node(
    workflow,
    code="return items.map(item => ({...item, processed: true}));",
    language="javascript"
)

# Code (Python)
code_node = builder.add_code_node(
    workflow,
    code="for item in items:\n    item['processed'] = True\nreturn items",
    language="python"
)
```

### Add Logic Nodes

```python
# IF condition
if_node = builder.add_if_node(
    workflow,
    conditions=[{
        "leftValue": "{{$json.status}}",
        "rightValue": "success",
        "operator": "equals"
    }]
)

# Set variables
set_node = builder.add_set_node(
    workflow,
    values={
        "timestamp": "{{$now}}",
        "processed": "true",
        "user_id": "12345"
    }
)
```

### Connect Nodes

```python
# Simple connection
builder.connect_nodes(workflow, trigger, http_node)

# Chain multiple nodes
builder.connect_nodes(workflow, trigger, http_node)
builder.connect_nodes(workflow, http_node, code_node)
builder.connect_nodes(workflow, code_node, email_node)

# Branching (IF node)
builder.connect_nodes(workflow, if_node, success_node, output_index=0)
builder.connect_nodes(workflow, if_node, failure_node, output_index=1)
```

### Organize Layout

```python
# Auto-arrange nodes
builder.organize_layout(workflow)
```

### Natural Language Generation

```python
# Generate from description
spec = "Send email report every day at 9 AM"
workflow = builder.parse_natural_language_spec(spec)

# With LLM (requires OPENAI_API_KEY)
builder = WorkflowBuilder(llm_api_key="your-openai-key")
workflow = builder.generate_workflow_with_llm(
    "Create a workflow that monitors Twitter mentions and sends them to Slack"
)
```

### Sample Workflows

```python
# Daily report
daily_report = builder.create_sample_daily_report_workflow()

# Calendar sync
calendar_sync = builder.create_sample_calendar_sync_workflow()
```

## Complete Integration Examples

### Example 1: Create and Deploy Workflow

```python
from src.jarvis.integrations.n8n_client import N8nClient
from src.jarvis.workflow_builder import WorkflowBuilder

# Initialize
client = N8nClient(base_url="http://localhost:5678", api_key="key")
builder = WorkflowBuilder()

# Build workflow
workflow = builder.create_basic_workflow("API Monitor")
trigger = builder.add_trigger_node(workflow, "interval", {"interval": 5})
http = builder.add_http_request_node(workflow, "https://api.example.com/health")
slack = builder.add_slack_node(workflow, "#monitoring", "API check: {{$json.status}}")

builder.connect_nodes(workflow, trigger, http)
builder.connect_nodes(workflow, http, slack)
builder.organize_layout(workflow)

# Validate
is_valid, errors = client.validate_workflow(workflow)
if not is_valid:
    print("Errors:", errors)
    exit(1)

# Preview
print(client.get_workflow_preview(workflow))

# Deploy
result = client.create_workflow(workflow)
print(f"Deployed with ID: {result['id']}")

# Activate
client.activate_workflow(result['id'])
print("Activated!")
```

### Example 2: Natural Language to Deployment

```python
# User input
user_request = "Send me an email report every morning at 9 AM with API stats"

# Generate workflow
workflow = builder.parse_natural_language_spec(user_request)

# Validate
is_valid, errors = client.validate_workflow(workflow)
if is_valid:
    # Deploy
    result = client.create_workflow(workflow)
    print(f"Created: {result['name']} (ID: {result['id']})")
else:
    print("Invalid workflow:", errors)
```

### Example 3: Monitor and Execute

```python
# List workflows
workflows = client.list_workflows(active=True)
print(f"Found {len(workflows)} active workflows")

for workflow in workflows:
    # Execute
    result = client.execute_workflow(workflow['id'])
    exec_id = result['executionId']
    
    # Check execution
    execution = client.get_execution(exec_id)
    print(f"{workflow['name']}: {execution['status']}")
```

### Example 4: Conditional Branching

```python
workflow = builder.create_basic_workflow("Smart Alert")

# Trigger
trigger = builder.add_trigger_node(workflow, "webhook")

# Fetch data
http = builder.add_http_request_node(workflow, "https://api.example.com/status")

# Check status
if_node = builder.add_if_node(workflow, [{
    "leftValue": "{{$json.status_code}}",
    "rightValue": "200",
    "operator": "notEquals"
}])

# Success path
success_msg = builder.add_slack_node(workflow, "#general", "All good!")

# Failure path
alert_email = builder.add_email_node(
    workflow,
    to="admin@example.com",
    subject="⚠️ API Alert",
    text="API returned status: {{$json.status_code}}"
)

# Connect
builder.connect_nodes(workflow, trigger, http)
builder.connect_nodes(workflow, http, if_node)
builder.connect_nodes(workflow, if_node, success_msg, output_index=1)  # False
builder.connect_nodes(workflow, if_node, alert_email, output_index=0)  # True

builder.organize_layout(workflow)

# Deploy
client.create_workflow(workflow)
```

### Example 5: Error Handling

```python
from src.jarvis.integrations.n8n_client import N8nClientError

try:
    # Try to create workflow
    result = client.create_workflow(workflow_data)
    print("Success!")
    
except N8nClientError as e:
    print(f"Failed to create workflow: {e}")
    
    # Fallback: save locally
    import json
    with open("workflow_backup.json", "w") as f:
        json.dump(workflow_data, f, indent=2)
    print("Saved workflow locally for later deployment")
```

### Example 6: Batch Operations

```python
# Create multiple workflows
specs = [
    "Send daily report at 9 AM",
    "Monitor API every 5 minutes",
    "Sync calendar events hourly"
]

created_workflows = []

for spec in specs:
    workflow = builder.parse_natural_language_spec(spec)
    
    is_valid, errors = client.validate_workflow(workflow)
    if is_valid:
        result = client.create_workflow(workflow)
        created_workflows.append(result)
        print(f"✓ Created: {result['name']}")
    else:
        print(f"✗ Failed: {spec}")
        print(f"  Errors: {errors}")

print(f"\nCreated {len(created_workflows)} workflows")
```

## Error Handling

### Common Patterns

```python
from src.jarvis.integrations.n8n_client import N8nClientError

# Test connection first
if not client.test_connection():
    print("Cannot connect to n8n. Is it running?")
    exit(1)

# Validate before creating
is_valid, errors = client.validate_workflow(workflow)
if not is_valid:
    print("Workflow validation failed:")
    for error in errors:
        print(f"  - {error}")
    exit(1)

# Handle API errors
try:
    result = client.create_workflow(workflow)
except N8nClientError as e:
    print(f"API error: {e}")
    # Handle error (retry, save locally, etc.)
```

## Tips and Best Practices

1. **Always validate** workflows before deployment
2. **Test with manual triggers** during development
3. **Use workflow preview** to verify structure
4. **Keep workflows inactive** until fully tested
5. **Handle API errors** gracefully with try/except
6. **Use descriptive names** for workflows and nodes
7. **Organize layout** after building for better visualization
8. **Monitor executions** regularly
9. **Version control** workflow JSON files
10. **Use environment variables** for sensitive data

## See Also

- [WORKFLOWS.md](WORKFLOWS.md) - Complete workflow documentation
- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [example_workflow.py](example_workflow.py) - Working examples
