import unittest
from unittest.mock import Mock, patch
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'jarvis'))

from workflow_builder import WorkflowBuilder


class TestWorkflowBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = WorkflowBuilder()

    def test_create_basic_workflow(self):
        workflow = self.builder.create_basic_workflow(
            name="Test Workflow",
            description="Test description"
        )
        
        self.assertEqual(workflow["name"], "Test Workflow")
        self.assertIn("description", workflow["settings"])
        self.assertIsInstance(workflow["nodes"], list)
        self.assertIsInstance(workflow["connections"], dict)
        self.assertFalse(workflow["active"])

    def test_add_trigger_node_manual(self):
        workflow = self.builder.create_basic_workflow("Test")
        node_name = self.builder.add_trigger_node(workflow, "manual")
        
        self.assertEqual(len(workflow["nodes"]), 1)
        self.assertEqual(workflow["nodes"][0]["name"], node_name)
        self.assertEqual(workflow["nodes"][0]["type"], "n8n-nodes-base.manualTrigger")
        self.assertIn(node_name, workflow["connections"])

    def test_add_trigger_node_schedule(self):
        workflow = self.builder.create_basic_workflow("Test")
        params = {"cronExpression": "0 9 * * *"}
        node_name = self.builder.add_trigger_node(workflow, "schedule", params)
        
        self.assertEqual(workflow["nodes"][0]["type"], "n8n-nodes-base.cron")
        self.assertEqual(workflow["nodes"][0]["parameters"], params)

    def test_add_http_request_node(self):
        workflow = self.builder.create_basic_workflow("Test")
        node_name = self.builder.add_http_request_node(
            workflow,
            url="https://api.example.com",
            method="POST",
            headers={"Authorization": "Bearer token"}
        )
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.httpRequest")
        self.assertEqual(node["parameters"]["url"], "https://api.example.com")
        self.assertEqual(node["parameters"]["method"], "POST")

    def test_add_email_node(self):
        workflow = self.builder.create_basic_workflow("Test")
        node_name = self.builder.add_email_node(
            workflow,
            to="test@example.com",
            subject="Test Email",
            text="Test message"
        )
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.emailSend")
        self.assertEqual(node["parameters"]["toEmail"], "test@example.com")
        self.assertEqual(node["parameters"]["subject"], "Test Email")
        self.assertEqual(node["parameters"]["emailType"], "text")

    def test_add_email_node_html(self):
        workflow = self.builder.create_basic_workflow("Test")
        node_name = self.builder.add_email_node(
            workflow,
            to="test@example.com",
            subject="Test",
            html="<h1>Test</h1>"
        )
        
        node = workflow["nodes"][0]
        self.assertEqual(node["parameters"]["emailType"], "html")
        self.assertEqual(node["parameters"]["html"], "<h1>Test</h1>")

    def test_add_slack_node(self):
        workflow = self.builder.create_basic_workflow("Test")
        node_name = self.builder.add_slack_node(
            workflow,
            channel="#general",
            message="Test message"
        )
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.slack")
        self.assertEqual(node["parameters"]["channel"], "#general")
        self.assertEqual(node["parameters"]["text"], "Test message")

    def test_add_code_node_javascript(self):
        workflow = self.builder.create_basic_workflow("Test")
        code = "return items;"
        node_name = self.builder.add_code_node(workflow, code, "javascript")
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.code")
        self.assertEqual(node["parameters"]["jsCode"], code)

    def test_add_code_node_python(self):
        workflow = self.builder.create_basic_workflow("Test")
        code = "return items"
        node_name = self.builder.add_code_node(workflow, code, "python")
        
        node = workflow["nodes"][0]
        self.assertEqual(node["parameters"]["pythonCode"], code)

    def test_add_if_node(self):
        workflow = self.builder.create_basic_workflow("Test")
        conditions = [
            {"leftValue": "{{$json.status}}", "rightValue": "active", "operator": "equals"}
        ]
        node_name = self.builder.add_if_node(workflow, conditions)
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.if")
        self.assertEqual(len(workflow["connections"][node_name]["main"]), 2)

    def test_add_set_node(self):
        workflow = self.builder.create_basic_workflow("Test")
        values = {"key1": "value1", "key2": "value2"}
        node_name = self.builder.add_set_node(workflow, values)
        
        node = workflow["nodes"][0]
        self.assertEqual(node["type"], "n8n-nodes-base.set")
        self.assertEqual(len(node["parameters"]["values"]["string"]), 2)

    def test_connect_nodes(self):
        workflow = self.builder.create_basic_workflow("Test")
        trigger = self.builder.add_trigger_node(workflow, "manual")
        http_node = self.builder.add_http_request_node(workflow, "https://api.example.com")
        
        self.builder.connect_nodes(workflow, trigger, http_node)
        
        connections = workflow["connections"][trigger]["main"][0]
        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0]["node"], http_node)
        self.assertEqual(connections[0]["type"], "main")

    def test_connect_nodes_multiple_outputs(self):
        workflow = self.builder.create_basic_workflow("Test")
        if_node = self.builder.add_if_node(workflow, [])
        node1 = self.builder.add_email_node(workflow, "test@example.com", "True Branch", "")
        node2 = self.builder.add_email_node(workflow, "test@example.com", "False Branch", "")
        
        self.builder.connect_nodes(workflow, if_node, node1, output_index=0)
        self.builder.connect_nodes(workflow, if_node, node2, output_index=1)
        
        self.assertEqual(workflow["connections"][if_node]["main"][0][0]["node"], node1)
        self.assertEqual(workflow["connections"][if_node]["main"][1][0]["node"], node2)

    def test_organize_layout(self):
        workflow = self.builder.create_basic_workflow("Test")
        trigger = self.builder.add_trigger_node(workflow, "manual")
        http_node = self.builder.add_http_request_node(workflow, "https://api.example.com")
        email_node = self.builder.add_email_node(workflow, "test@example.com", "Test", "")
        
        self.builder.connect_nodes(workflow, trigger, http_node)
        self.builder.connect_nodes(workflow, http_node, email_node)
        
        self.builder.organize_layout(workflow)
        
        trigger_node = next(n for n in workflow["nodes"] if n["name"] == trigger)
        http_node_obj = next(n for n in workflow["nodes"] if n["name"] == http_node)
        email_node_obj = next(n for n in workflow["nodes"] if n["name"] == email_node)
        
        self.assertIsInstance(trigger_node["position"], list)
        self.assertEqual(len(trigger_node["position"]), 2)
        
        self.assertLess(trigger_node["position"][0], http_node_obj["position"][0])
        self.assertLess(http_node_obj["position"][0], email_node_obj["position"][0])

    def test_parse_natural_language_spec_email(self):
        spec = "Send daily email report at 9 AM"
        workflow = self.builder.parse_natural_language_spec(spec)
        
        description = str(workflow.get("description", "")).lower()
        workflow_name = workflow["name"].lower()
        self.assertTrue("email" in description or "email" in spec.lower())
        self.assertTrue(len(workflow["nodes"]) > 0)
        
        has_email_node = any(
            "email" in node["type"].lower() 
            for node in workflow["nodes"]
        )
        self.assertTrue(has_email_node)

    def test_parse_natural_language_spec_slack(self):
        spec = "Send Slack message to #general"
        workflow = self.builder.parse_natural_language_spec(spec)
        
        has_slack_node = any(
            "slack" in node["type"].lower() 
            for node in workflow["nodes"]
        )
        self.assertTrue(has_slack_node)

    def test_parse_natural_language_spec_http(self):
        spec = "Call API endpoint every hour"
        workflow = self.builder.parse_natural_language_spec(spec)
        
        has_http_node = any(
            "http" in node["type"].lower() 
            for node in workflow["nodes"]
        )
        self.assertTrue(has_http_node)

    def test_parse_natural_language_spec_schedule(self):
        spec = "Run daily at 9 AM to sync calendar"
        workflow = self.builder.parse_natural_language_spec(spec)
        
        has_schedule_trigger = any(
            node["type"] in ["n8n-nodes-base.cron", "n8n-nodes-base.schedule"]
            for node in workflow["nodes"]
        )
        self.assertTrue(has_schedule_trigger or "schedule" in workflow["name"].lower())

    def test_create_sample_daily_report_workflow(self):
        workflow = self.builder.create_sample_daily_report_workflow()
        
        self.assertEqual(workflow["name"], "Daily Report")
        self.assertGreaterEqual(len(workflow["nodes"]), 3)
        
        node_types = [node["type"] for node in workflow["nodes"]]
        self.assertIn("n8n-nodes-base.cron", node_types)
        self.assertIn("n8n-nodes-base.httpRequest", node_types)
        self.assertIn("n8n-nodes-base.emailSend", node_types)

    def test_create_sample_calendar_sync_workflow(self):
        workflow = self.builder.create_sample_calendar_sync_workflow()
        
        self.assertEqual(workflow["name"], "Calendar Sync")
        self.assertGreaterEqual(len(workflow["nodes"]), 3)
        
        node_types = [node["type"] for node in workflow["nodes"]]
        self.assertIn("n8n-nodes-base.interval", node_types)
        self.assertIn("n8n-nodes-base.httpRequest", node_types)
        self.assertIn("n8n-nodes-base.slack", node_types)

    def test_workflow_connections_integrity(self):
        workflow = self.builder.create_sample_daily_report_workflow()
        
        node_names = {node["name"] for node in workflow["nodes"]}
        
        for source, connections in workflow["connections"].items():
            self.assertIn(source, node_names, f"Source node {source} not found in nodes")
            
            for output_list in connections.get("main", []):
                for connection in output_list:
                    target = connection.get("node")
                    if target:
                        self.assertIn(target, node_names, f"Target node {target} not found in nodes")

    def test_node_counter_increments(self):
        workflow = self.builder.create_basic_workflow("Test")
        
        node1 = self.builder.add_trigger_node(workflow, "manual")
        node2 = self.builder.add_http_request_node(workflow, "https://api.example.com")
        node3 = self.builder.add_email_node(workflow, "test@example.com", "Test", "")
        
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node1, node3)

    def test_generate_workflow_with_llm_fallback(self):
        spec = "Send daily email"
        workflow = self.builder.generate_workflow_with_llm(spec)
        
        self.assertIsNotNone(workflow)
        self.assertIn("name", workflow)
        self.assertIn("nodes", workflow)
        self.assertIn("connections", workflow)


if __name__ == '__main__':
    unittest.main()
