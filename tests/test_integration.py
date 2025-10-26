import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'jarvis'))

from integrations.n8n_client import N8nClient, N8nClientError
from workflow_builder import WorkflowBuilder


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.builder = WorkflowBuilder()
        self.client = N8nClient(base_url="http://localhost:5678", api_key="test-key")

    def test_end_to_end_workflow_creation(self):
        workflow = self.builder.create_sample_daily_report_workflow()
        
        is_valid, errors = self.client.validate_workflow(workflow)
        self.assertTrue(is_valid, f"Workflow validation failed: {errors}")
        self.assertEqual(len(errors), 0)
        
        self.assertEqual(workflow["name"], "Daily Report")
        self.assertFalse(workflow["active"])
        self.assertGreaterEqual(len(workflow["nodes"]), 3)

    def test_natural_language_to_validated_workflow(self):
        spec = "Send email report every day at 9 AM"
        workflow = self.builder.parse_natural_language_spec(spec)
        
        is_valid, errors = self.client.validate_workflow(workflow)
        self.assertTrue(is_valid, f"Generated workflow is invalid: {errors}")
        
        has_schedule = any(
            node["type"] in ["n8n-nodes-base.cron", "n8n-nodes-base.schedule"]
            for node in workflow["nodes"]
        )
        self.assertTrue(has_schedule)

    def test_custom_workflow_with_validation(self):
        workflow = self.builder.create_basic_workflow("Test Integration")
        trigger = self.builder.add_trigger_node(workflow, "manual")
        http = self.builder.add_http_request_node(workflow, "https://api.example.com")
        email = self.builder.add_email_node(workflow, "test@example.com", "Test", "Body")
        
        self.builder.connect_nodes(workflow, trigger, http)
        self.builder.connect_nodes(workflow, http, email)
        self.builder.organize_layout(workflow)
        
        is_valid, errors = self.client.validate_workflow(workflow)
        self.assertTrue(is_valid, f"Custom workflow invalid: {errors}")
        
        preview = self.client.get_workflow_preview(workflow)
        self.assertIn("Test Integration", preview)
        self.assertIn("3", preview)

    @patch('requests.Session.request')
    def test_full_workflow_lifecycle(self, mock_request):
        workflow = self.builder.create_basic_workflow("Lifecycle Test")
        trigger = self.builder.add_trigger_node(workflow, "manual")
        
        create_response = Mock()
        create_response.status_code = 200
        create_response.json.return_value = {**workflow, "id": "test-id-123"}
        
        get_response = Mock()
        get_response.status_code = 200
        get_response.json.return_value = {**workflow, "id": "test-id-123", "active": False}
        
        update_response = Mock()
        update_response.status_code = 200
        update_response.json.return_value = {**workflow, "id": "test-id-123", "active": True}
        
        execute_response = Mock()
        execute_response.status_code = 200
        execute_response.json.return_value = {"executionId": "exec-123"}
        
        mock_request.side_effect = [create_response, get_response, update_response, execute_response]
        
        created = self.client.create_workflow(workflow)
        self.assertEqual(created["id"], "test-id-123")
        
        activated = self.client.activate_workflow("test-id-123")
        self.assertTrue(activated["active"])
        
        result = self.client.execute_workflow("test-id-123")
        self.assertIn("executionId", result)

    def test_multiple_workflows_from_specs(self):
        specs = [
            "Send daily report at 9 AM",
            "Sync calendar every hour",
            "Monitor API and alert on failure"
        ]
        
        workflows = []
        for spec in specs:
            workflow = self.builder.parse_natural_language_spec(spec)
            is_valid, errors = self.client.validate_workflow(workflow)
            self.assertTrue(is_valid, f"Workflow for '{spec}' is invalid: {errors}")
            workflows.append(workflow)
        
        self.assertEqual(len(workflows), 3)
        
        for workflow in workflows:
            self.assertIn("name", workflow)
            self.assertIn("nodes", workflow)
            self.assertGreater(len(workflow["nodes"]), 0)

    def test_workflow_connection_integrity(self):
        workflow = self.builder.create_sample_calendar_sync_workflow()
        
        node_names = {node["name"] for node in workflow["nodes"]}
        
        for source, connections in workflow["connections"].items():
            self.assertIn(source, node_names)
            
            for output_list in connections.get("main", []):
                for connection in output_list:
                    target = connection.get("node")
                    if target:
                        self.assertIn(target, node_names)

    def test_error_handling_integration(self):
        invalid_workflow = {
            "name": "",
            "nodes": [],
            "connections": {}
        }
        
        with self.assertRaises(N8nClientError):
            self.client.create_workflow(invalid_workflow)

    def test_workflow_preview_completeness(self):
        workflow = self.builder.create_sample_daily_report_workflow()
        preview = self.client.get_workflow_preview(workflow)
        
        self.assertIn(workflow["name"], preview)
        self.assertIn("Nodes:", preview)
        self.assertIn("Connections:", preview)
        self.assertIn("Active:", preview)
        
        for node in workflow["nodes"]:
            self.assertIn(node["name"], preview)

    def test_complex_branching_workflow(self):
        workflow = self.builder.create_basic_workflow("Complex Branch")
        
        trigger = self.builder.add_trigger_node(workflow, "manual")
        http = self.builder.add_http_request_node(workflow, "https://api.example.com")
        if_node = self.builder.add_if_node(workflow, [])
        success_email = self.builder.add_email_node(workflow, "success@example.com", "Success", "")
        failure_slack = self.builder.add_slack_node(workflow, "#alerts", "Failed")
        
        self.builder.connect_nodes(workflow, trigger, http)
        self.builder.connect_nodes(workflow, http, if_node)
        self.builder.connect_nodes(workflow, if_node, success_email, output_index=0)
        self.builder.connect_nodes(workflow, if_node, failure_slack, output_index=1)
        
        self.builder.organize_layout(workflow)
        
        is_valid, errors = self.client.validate_workflow(workflow)
        self.assertTrue(is_valid, f"Complex workflow invalid: {errors}")
        
        self.assertEqual(len(workflow["nodes"]), 5)
        
        if_connections = workflow["connections"][if_node]["main"]
        self.assertEqual(len(if_connections), 2)

    def test_sample_workflows_are_deployable(self):
        samples = [
            self.builder.create_sample_daily_report_workflow(),
            self.builder.create_sample_calendar_sync_workflow()
        ]
        
        for workflow in samples:
            is_valid, errors = self.client.validate_workflow(workflow)
            self.assertTrue(is_valid, f"Sample workflow {workflow['name']} invalid: {errors}")
            
            preview = self.client.get_workflow_preview(workflow)
            self.assertIsNotNone(preview)
            self.assertGreater(len(preview), 0)


if __name__ == '__main__':
    unittest.main()
