import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'jarvis'))

from integrations.n8n_client import N8nClient, N8nClientError


class TestN8nClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5678"
        self.api_key = "test-api-key"
        self.client = N8nClient(base_url=self.base_url, api_key=self.api_key)

    def test_initialization_with_api_key(self):
        client = N8nClient(base_url=self.base_url, api_key=self.api_key)
        self.assertEqual(client.base_url, self.base_url)
        self.assertEqual(client.api_key, self.api_key)
        self.assertIn('X-N8N-API-KEY', client.session.headers)

    def test_initialization_with_auth_token(self):
        auth_token = "test-token"
        client = N8nClient(base_url=self.base_url, auth_token=auth_token)
        self.assertEqual(client.auth_token, auth_token)
        self.assertIn('Authorization', client.session.headers)

    @patch('requests.Session.request')
    def test_list_workflows_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "1", "name": "Test Workflow", "active": True},
                {"id": "2", "name": "Another Workflow", "active": False}
            ]
        }
        mock_request.return_value = mock_response

        workflows = self.client.list_workflows()
        
        self.assertEqual(len(workflows), 2)
        self.assertEqual(workflows[0]["name"], "Test Workflow")
        self.assertTrue(workflows[0]["active"])

    @patch('requests.Session.request')
    def test_list_workflows_with_filter(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_request.return_value = mock_response

        self.client.list_workflows(active=True)
        
        call_args = mock_request.call_args
        self.assertIn('params', call_args.kwargs)
        self.assertEqual(call_args.kwargs['params']['active'], 'true')

    @patch('requests.Session.request')
    def test_get_workflow_success(self, mock_request):
        workflow_id = "test-id"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": workflow_id,
            "name": "Test Workflow",
            "nodes": [],
            "connections": {}
        }
        mock_request.return_value = mock_response

        workflow = self.client.get_workflow(workflow_id)
        
        self.assertEqual(workflow["id"], workflow_id)
        self.assertEqual(workflow["name"], "Test Workflow")

    @patch('requests.Session.request')
    def test_create_workflow_success(self, mock_request):
        workflow_data = {
            "name": "New Workflow",
            "nodes": [
                {
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [250, 300]
                }
            ],
            "connections": {}
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {**workflow_data, "id": "new-id"}
        mock_request.return_value = mock_response

        result = self.client.create_workflow(workflow_data)
        
        self.assertEqual(result["name"], "New Workflow")
        self.assertIn("id", result)

    def test_create_workflow_missing_fields(self):
        invalid_workflow = {
            "name": "Invalid Workflow"
        }
        
        with self.assertRaises(N8nClientError) as context:
            self.client.create_workflow(invalid_workflow)
        
        self.assertIn("Missing required field", str(context.exception))

    @patch('requests.Session.request')
    def test_update_workflow_success(self, mock_request):
        workflow_id = "test-id"
        update_data = {"name": "Updated Name"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {**update_data, "id": workflow_id}
        mock_request.return_value = mock_response

        result = self.client.update_workflow(workflow_id, update_data)
        
        self.assertEqual(result["name"], "Updated Name")

    @patch('requests.Session.request')
    def test_delete_workflow_success(self, mock_request):
        workflow_id = "test-id"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        result = self.client.delete_workflow(workflow_id)
        
        self.assertTrue(result.get("success"))

    @patch('requests.Session.request')
    def test_execute_workflow_success(self, mock_request):
        workflow_id = "test-id"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"executionId": "exec-123"}
        mock_request.return_value = mock_response

        result = self.client.execute_workflow(workflow_id)
        
        self.assertIn("executionId", result)

    @patch('requests.Session.request')
    def test_api_error_handling(self, mock_request):
        import requests
        mock_request.side_effect = requests.exceptions.RequestException("Not Found")

        with self.assertRaises(N8nClientError):
            self.client.list_workflows()

    def test_validate_workflow_valid(self):
        valid_workflow = {
            "name": "Valid Workflow",
            "nodes": [
                {
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "position": [250, 300]
                }
            ],
            "connections": {}
        }
        
        is_valid, errors = self.client.validate_workflow(valid_workflow)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_workflow_missing_name(self):
        invalid_workflow = {
            "nodes": [],
            "connections": {}
        }
        
        is_valid, errors = self.client.validate_workflow(invalid_workflow)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("name" in err.lower() for err in errors))

    def test_validate_workflow_no_nodes(self):
        invalid_workflow = {
            "name": "No Nodes",
            "nodes": [],
            "connections": {}
        }
        
        is_valid, errors = self.client.validate_workflow(invalid_workflow)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("at least one node" in err.lower() for err in errors))

    def test_validate_workflow_duplicate_node_names(self):
        invalid_workflow = {
            "name": "Duplicate Nodes",
            "nodes": [
                {"name": "Node1", "type": "test", "position": [0, 0]},
                {"name": "Node1", "type": "test", "position": [100, 100]}
            ],
            "connections": {}
        }
        
        is_valid, errors = self.client.validate_workflow(invalid_workflow)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("duplicate" in err.lower() for err in errors))

    def test_get_workflow_preview(self):
        workflow = {
            "name": "Test Workflow",
            "active": True,
            "nodes": [
                {"name": "Start", "type": "n8n-nodes-base.start", "parameters": {}},
                {"name": "HTTP", "type": "n8n-nodes-base.httpRequest", "parameters": {"url": "test"}}
            ],
            "connections": {
                "Start": {
                    "main": [[{"node": "HTTP"}]]
                }
            }
        }
        
        preview = self.client.get_workflow_preview(workflow)
        
        self.assertIn("Test Workflow", preview)
        self.assertIn("Start", preview)
        self.assertIn("HTTP", preview)
        self.assertIn("Active: True", preview)

    @patch('requests.Session.request')
    def test_activate_workflow(self, mock_request):
        workflow_id = "test-id"
        
        get_response = Mock()
        get_response.status_code = 200
        get_response.json.return_value = {
            "id": workflow_id,
            "name": "Test",
            "active": False,
            "nodes": [],
            "connections": {}
        }
        
        update_response = Mock()
        update_response.status_code = 200
        update_response.json.return_value = {
            "id": workflow_id,
            "name": "Test",
            "active": True,
            "nodes": [],
            "connections": {}
        }
        
        mock_request.side_effect = [get_response, update_response]
        
        result = self.client.activate_workflow(workflow_id)
        
        self.assertTrue(result["active"])

    @patch('requests.Session.request')
    def test_get_executions(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "exec-1", "status": "success"},
                {"id": "exec-2", "status": "running"}
            ]
        }
        mock_request.return_value = mock_response
        
        executions = self.client.get_executions(limit=10)
        
        self.assertEqual(len(executions), 2)
        self.assertEqual(executions[0]["status"], "success")


if __name__ == '__main__':
    unittest.main()
