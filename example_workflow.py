#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'jarvis'))

from integrations.n8n_client import N8nClient, N8nClientError
from workflow_builder import WorkflowBuilder


def example_create_daily_report():
    print("="*60)
    print("Example: Create Daily Report Workflow")
    print("="*60)
    
    builder = WorkflowBuilder()
    workflow = builder.create_sample_daily_report_workflow()
    
    preview = N8nClient("http://localhost:5678", api_key="dummy").get_workflow_preview(workflow)
    print(preview)
    
    print("\n✓ Sample workflow created!")
    print("  To deploy, configure n8n and use the Jarvis voice commands")


def example_natural_language():
    print("\n" + "="*60)
    print("Example: Natural Language Workflow Generation")
    print("="*60)
    
    builder = WorkflowBuilder()
    
    specs = [
        "Send daily email report at 9 AM",
        "Sync calendar events every hour",
        "Send Slack message when API fails"
    ]
    
    for spec in specs:
        print(f"\n📝 Spec: '{spec}'")
        workflow = builder.parse_natural_language_spec(spec)
        print(f"   ✓ Generated workflow with {len(workflow['nodes'])} nodes")
        print(f"   Nodes: {[node['type'].split('.')[-1] for node in workflow['nodes']]}")


def example_custom_workflow():
    print("\n" + "="*60)
    print("Example: Custom Workflow Building")
    print("="*60)
    
    builder = WorkflowBuilder()
    
    workflow = builder.create_basic_workflow(
        name="Custom API Monitor",
        description="Monitor API and alert on failures"
    )
    
    trigger = builder.add_trigger_node(workflow, "interval", {"interval": 5})
    http = builder.add_http_request_node(
        workflow,
        url="https://api.example.com/health",
        method="GET"
    )
    condition = builder.add_if_node(workflow, [
        {"leftValue": "{{$json.status}}", "rightValue": "200", "operator": "equals"}
    ])
    slack_success = builder.add_slack_node(workflow, "#monitoring", "API is healthy")
    slack_failure = builder.add_slack_node(workflow, "#alerts", "API is down!")
    
    builder.connect_nodes(workflow, trigger, http)
    builder.connect_nodes(workflow, http, condition)
    builder.connect_nodes(workflow, condition, slack_success, output_index=0)
    builder.connect_nodes(workflow, condition, slack_failure, output_index=1)
    
    builder.organize_layout(workflow)
    
    print(f"\n✓ Custom workflow created: {workflow['name']}")
    print(f"  Nodes: {len(workflow['nodes'])}")
    print(f"  Flow: Interval → HTTP → IF → Slack (success/failure)")


def example_validation():
    print("\n" + "="*60)
    print("Example: Workflow Validation")
    print("="*60)
    
    client = N8nClient("http://localhost:5678", api_key="dummy")
    
    valid_workflow = {
        "name": "Valid Workflow",
        "nodes": [{"name": "Start", "type": "test", "position": [0, 0]}],
        "connections": {}
    }
    
    invalid_workflow = {
        "nodes": [],
        "connections": {}
    }
    
    is_valid, errors = client.validate_workflow(valid_workflow)
    print(f"\n✓ Valid workflow: {is_valid}")
    
    is_valid, errors = client.validate_workflow(invalid_workflow)
    print(f"\n✗ Invalid workflow: {is_valid}")
    print(f"  Errors: {errors}")


def main():
    print("\n🤖 Jarvis n8n Workflow Integration Examples")
    print("=" * 60)
    
    try:
        example_create_daily_report()
        example_natural_language()
        example_custom_workflow()
        example_validation()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        print("\nTo use with Jarvis:")
        print("1. Configure n8n: cp config/n8n_config.example.json config/n8n_config.json")
        print("2. Add your n8n API key to the config file")
        print("3. Run Jarvis: python -m src.jarvis.jarvis")
        print("4. Say: 'Jarvis, build automation to send daily report'")
        print("\nFor more info, see WORKFLOWS.md")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
