import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class N8nClientError(Exception):
    pass


class N8nClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.auth_token = auth_token
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'X-N8N-API-KEY': api_key})
        elif auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            if response.status_code == 204:
                return {}
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise N8nClientError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise N8nClientError(f"Invalid JSON response: {str(e)}")

    def test_connection(self) -> bool:
        try:
            self._make_request('GET', '/workflows')
            return True
        except N8nClientError:
            return False

    def list_workflows(self, active: Optional[bool] = None) -> List[Dict]:
        params = {}
        if active is not None:
            params['active'] = str(active).lower()
        
        try:
            response = self._make_request('GET', '/workflows', params=params)
            return response.get('data', []) if isinstance(response, dict) else response
        except N8nClientError as e:
            raise N8nClientError(f"Failed to list workflows: {str(e)}")

    def get_workflow(self, workflow_id: str) -> Dict:
        try:
            return self._make_request('GET', f'/workflows/{workflow_id}')
        except N8nClientError as e:
            raise N8nClientError(f"Failed to get workflow {workflow_id}: {str(e)}")

    def create_workflow(self, workflow_data: Dict) -> Dict:
        required_fields = ['name', 'nodes', 'connections']
        for field in required_fields:
            if field not in workflow_data:
                raise N8nClientError(f"Missing required field: {field}")
        
        if 'active' not in workflow_data:
            workflow_data['active'] = False
        
        if 'settings' not in workflow_data:
            workflow_data['settings'] = {}
        
        try:
            return self._make_request('POST', '/workflows', data=workflow_data)
        except N8nClientError as e:
            raise N8nClientError(f"Failed to create workflow: {str(e)}")

    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Dict:
        try:
            return self._make_request('PATCH', f'/workflows/{workflow_id}', data=workflow_data)
        except N8nClientError as e:
            raise N8nClientError(f"Failed to update workflow {workflow_id}: {str(e)}")

    def delete_workflow(self, workflow_id: str) -> Dict:
        try:
            return self._make_request('DELETE', f'/workflows/{workflow_id}')
        except N8nClientError as e:
            raise N8nClientError(f"Failed to delete workflow {workflow_id}: {str(e)}")

    def activate_workflow(self, workflow_id: str) -> Dict:
        workflow = self.get_workflow(workflow_id)
        workflow['active'] = True
        return self.update_workflow(workflow_id, workflow)

    def deactivate_workflow(self, workflow_id: str) -> Dict:
        workflow = self.get_workflow(workflow_id)
        workflow['active'] = False
        return self.update_workflow(workflow_id, workflow)

    def execute_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Dict:
        try:
            endpoint = f'/workflows/{workflow_id}/execute'
            payload = data if data else {}
            return self._make_request('POST', endpoint, data=payload)
        except N8nClientError as e:
            raise N8nClientError(f"Failed to execute workflow {workflow_id}: {str(e)}")

    def get_executions(self, workflow_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        params = {'limit': limit}
        if workflow_id:
            params['workflowId'] = workflow_id
        
        try:
            response = self._make_request('GET', '/executions', params=params)
            return response.get('data', []) if isinstance(response, dict) else response
        except N8nClientError as e:
            raise N8nClientError(f"Failed to get executions: {str(e)}")

    def get_execution(self, execution_id: str) -> Dict:
        try:
            return self._make_request('GET', f'/executions/{execution_id}')
        except N8nClientError as e:
            raise N8nClientError(f"Failed to get execution {execution_id}: {str(e)}")

    def validate_workflow(self, workflow_data: Dict) -> tuple[bool, List[str]]:
        errors = []
        
        if 'name' not in workflow_data or not workflow_data['name']:
            errors.append("Workflow name is required")
        
        if 'nodes' not in workflow_data or not isinstance(workflow_data['nodes'], list):
            errors.append("Workflow must have a 'nodes' array")
        elif len(workflow_data['nodes']) == 0:
            errors.append("Workflow must have at least one node")
        
        if 'connections' not in workflow_data or not isinstance(workflow_data['connections'], dict):
            errors.append("Workflow must have a 'connections' object")
        
        if 'nodes' in workflow_data and isinstance(workflow_data['nodes'], list):
            node_names = set()
            for idx, node in enumerate(workflow_data['nodes']):
                if 'name' not in node:
                    errors.append(f"Node {idx} is missing a name")
                elif node['name'] in node_names:
                    errors.append(f"Duplicate node name: {node['name']}")
                else:
                    node_names.add(node['name'])
                
                if 'type' not in node:
                    errors.append(f"Node {node.get('name', idx)} is missing a type")
                
                if 'position' not in node:
                    errors.append(f"Node {node.get('name', idx)} is missing position")
        
        return len(errors) == 0, errors

    def get_workflow_preview(self, workflow_data: Dict) -> str:
        preview = f"Workflow: {workflow_data.get('name', 'Unnamed')}\n"
        preview += f"Active: {workflow_data.get('active', False)}\n"
        preview += f"Nodes: {len(workflow_data.get('nodes', []))}\n\n"
        
        preview += "Node Structure:\n"
        for node in workflow_data.get('nodes', []):
            preview += f"  - {node.get('name', 'Unknown')} ({node.get('type', 'Unknown')})\n"
            if 'parameters' in node and node['parameters']:
                preview += f"    Parameters: {list(node['parameters'].keys())}\n"
        
        preview += "\nConnections:\n"
        connections = workflow_data.get('connections', {})
        if connections:
            for source, targets in connections.items():
                preview += f"  {source} ->\n"
                for conn_type, conn_list in targets.items():
                    for conn_group in conn_list:
                        for conn in conn_group:
                            preview += f"    -> {conn.get('node', 'Unknown')}\n"
        else:
            preview += "  No connections defined\n"
        
        return preview
