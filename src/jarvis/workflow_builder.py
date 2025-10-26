import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class WorkflowBuilder:
    def __init__(self, llm_api_key: Optional[str] = None):
        self.llm_api_key = llm_api_key or os.environ.get('OPENAI_API_KEY')
        self.node_counter = 0

    def _generate_node_id(self) -> str:
        self.node_counter += 1
        return f"node_{self.node_counter}"

    def create_basic_workflow(self, name: str, description: str = "") -> Dict:
        workflow = {
            "name": name,
            "nodes": [],
            "connections": {},
            "active": False,
            "settings": {
                "executionOrder": "v1"
            },
            "tags": []
        }
        
        if description:
            workflow["settings"]["description"] = description
        
        return workflow

    def add_trigger_node(self, workflow: Dict, trigger_type: str = "manual", parameters: Optional[Dict] = None) -> str:
        node_name = f"Trigger_{self._generate_node_id()}"
        
        node_types = {
            "manual": "n8n-nodes-base.manualTrigger",
            "webhook": "n8n-nodes-base.webhook",
            "schedule": "n8n-nodes-base.cron",
            "interval": "n8n-nodes-base.interval"
        }
        
        node = {
            "name": node_name,
            "type": node_types.get(trigger_type, "n8n-nodes-base.manualTrigger"),
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": parameters or {}
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def add_http_request_node(self, workflow: Dict, url: str, method: str = "GET", 
                             headers: Optional[Dict] = None, body: Optional[Dict] = None) -> str:
        node_name = f"HTTP_Request_{self._generate_node_id()}"
        
        parameters = {
            "url": url,
            "method": method,
            "options": {}
        }
        
        if headers:
            parameters["headerParameters"] = {
                "parameters": [{"name": k, "value": v} for k, v in headers.items()]
            }
        
        if body:
            parameters["body"] = json.dumps(body)
            parameters["contentType"] = "json"
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [450, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def add_email_node(self, workflow: Dict, to: str, subject: str, text: str = "", html: str = "") -> str:
        node_name = f"Email_{self._generate_node_id()}"
        
        parameters = {
            "toEmail": to,
            "subject": subject,
            "emailType": "html" if html else "text"
        }
        
        if html:
            parameters["html"] = html
        else:
            parameters["text"] = text
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.emailSend",
            "typeVersion": 2,
            "position": [650, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def add_slack_node(self, workflow: Dict, channel: str, message: str) -> str:
        node_name = f"Slack_{self._generate_node_id()}"
        
        parameters = {
            "channel": channel,
            "text": message,
            "otherOptions": {}
        }
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.slack",
            "typeVersion": 2.1,
            "position": [650, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def add_code_node(self, workflow: Dict, code: str, language: str = "javascript") -> str:
        node_name = f"Code_{self._generate_node_id()}"
        
        mode = "runOnceForAllItems" if language == "javascript" else "runOnceForEachItem"
        
        parameters = {
            "mode": mode,
            "jsCode": code if language == "javascript" else "",
            "pythonCode": code if language == "python" else ""
        }
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [450, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def add_if_node(self, workflow: Dict, conditions: List[Dict]) -> str:
        node_name = f"IF_{self._generate_node_id()}"
        
        parameters = {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": conditions
            }
        }
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.if",
            "typeVersion": 2,
            "position": [450, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[], []]}
        
        return node_name

    def add_set_node(self, workflow: Dict, values: Dict) -> str:
        node_name = f"Set_{self._generate_node_id()}"
        
        parameters = {
            "values": {
                "string": [{"name": k, "value": v} for k, v in values.items()]
            },
            "options": {}
        }
        
        node = {
            "name": node_name,
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.2,
            "position": [450, 300],
            "parameters": parameters
        }
        
        workflow["nodes"].append(node)
        workflow["connections"][node_name] = {"main": [[]]}
        
        return node_name

    def connect_nodes(self, workflow: Dict, source_node: str, target_node: str, 
                     output_index: int = 0, input_index: int = 0):
        if source_node not in workflow["connections"]:
            workflow["connections"][source_node] = {"main": [[]]}
        
        while len(workflow["connections"][source_node]["main"]) <= output_index:
            workflow["connections"][source_node]["main"].append([])
        
        connection = {
            "node": target_node,
            "type": "main",
            "index": input_index
        }
        
        workflow["connections"][source_node]["main"][output_index].append(connection)

    def organize_layout(self, workflow: Dict):
        x_spacing = 200
        y_spacing = 150
        start_x = 250
        start_y = 300
        
        visited = set()
        node_levels = {}
        
        def get_node_level(node_name: str, level: int = 0):
            if node_name in visited:
                return
            visited.add(node_name)
            
            if node_name not in node_levels:
                node_levels[node_name] = level
            else:
                node_levels[node_name] = max(node_levels[node_name], level)
            
            if node_name in workflow["connections"]:
                for output_list in workflow["connections"][node_name].get("main", []):
                    for connection in output_list:
                        target_node = connection["node"]
                        get_node_level(target_node, level + 1)
        
        for node in workflow["nodes"]:
            if node["name"] not in visited:
                get_node_level(node["name"])
        
        level_counts = {}
        for node in workflow["nodes"]:
            node_name = node["name"]
            level = node_levels.get(node_name, 0)
            
            if level not in level_counts:
                level_counts[level] = 0
            
            x = start_x + (level * x_spacing)
            y = start_y + (level_counts[level] * y_spacing)
            
            node["position"] = [x, y]
            level_counts[level] += 1

    def parse_natural_language_spec(self, spec: str) -> Dict:
        workflow = self.create_basic_workflow(
            name=f"Generated Workflow {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            description=f"Auto-generated from: {spec[:100]}"
        )
        
        spec_lower = spec.lower()
        
        trigger_node = self.add_trigger_node(workflow, "manual")
        last_node = trigger_node
        
        if "schedule" in spec_lower or "daily" in spec_lower or "every day" in spec_lower:
            trigger_node = self.add_trigger_node(
                workflow, 
                "schedule", 
                {"cronExpression": "0 9 * * *", "triggerTimes": {"mode": "everyDay"}}
            )
            workflow["nodes"] = [node for node in workflow["nodes"] if node["name"] != last_node]
            last_node = trigger_node
        
        if "email" in spec_lower or "send report" in spec_lower:
            email_node = self.add_email_node(
                workflow,
                to="user@example.com",
                subject="Automated Report",
                text="This is an automated report generated by Jarvis"
            )
            self.connect_nodes(workflow, last_node, email_node)
            last_node = email_node
        
        if "slack" in spec_lower or "message" in spec_lower:
            slack_node = self.add_slack_node(
                workflow,
                channel="#general",
                message="Automated message from Jarvis"
            )
            self.connect_nodes(workflow, last_node, slack_node)
            last_node = slack_node
        
        if "api" in spec_lower or "http" in spec_lower or "webhook" in spec_lower:
            http_node = self.add_http_request_node(
                workflow,
                url="https://api.example.com/endpoint",
                method="GET"
            )
            self.connect_nodes(workflow, last_node, http_node)
            last_node = http_node
        
        if "calendar" in spec_lower or "sync" in spec_lower:
            code_node = self.add_code_node(
                workflow,
                code="// Add your calendar sync logic here\nreturn items;"
            )
            self.connect_nodes(workflow, last_node, code_node)
            last_node = code_node
        
        if "process data" in spec_lower or "transform" in spec_lower:
            set_node = self.add_set_node(
                workflow,
                values={"processed": "true", "timestamp": "{{$now}}"}
            )
            self.connect_nodes(workflow, last_node, set_node)
            last_node = set_node
        
        self.organize_layout(workflow)
        
        return workflow

    def generate_workflow_with_llm(self, spec: str) -> Dict:
        if not self.llm_api_key:
            return self.parse_natural_language_spec(spec)
        
        try:
            import openai
            openai.api_key = self.llm_api_key
            
            system_prompt = """You are an expert n8n workflow builder. Generate valid n8n workflow JSON based on user requirements.
The workflow must include:
- A name and description
- An array of nodes with proper structure (name, type, typeVersion, position, parameters)
- A connections object linking nodes
- Proper node types like n8n-nodes-base.manualTrigger, n8n-nodes-base.httpRequest, etc.

Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create an n8n workflow for: {spec}"}
                ],
                temperature=0.7
            )
            
            workflow_json = response.choices[0].message.content
            workflow = json.loads(workflow_json)
            
            if not all(k in workflow for k in ['name', 'nodes', 'connections']):
                raise ValueError("Invalid workflow structure from LLM")
            
            return workflow
            
        except Exception as e:
            print(f"LLM generation failed: {e}. Falling back to template-based generation.")
            return self.parse_natural_language_spec(spec)

    def create_sample_daily_report_workflow(self) -> Dict:
        workflow = self.create_basic_workflow(
            name="Daily Report",
            description="Sends a daily report email at 9 AM"
        )
        
        trigger = self.add_trigger_node(
            workflow, 
            "schedule", 
            {"cronExpression": "0 9 * * *"}
        )
        
        http_node = self.add_http_request_node(
            workflow,
            url="https://api.example.com/daily-stats",
            method="GET"
        )
        self.connect_nodes(workflow, trigger, http_node)
        
        code_node = self.add_code_node(
            workflow,
            code="""
const data = items[0].json;
const report = `Daily Report:\\n\\nTotal Users: ${data.users}\\nTotal Sales: ${data.sales}`;
return [{json: {report}}];
"""
        )
        self.connect_nodes(workflow, http_node, code_node)
        
        email_node = self.add_email_node(
            workflow,
            to="team@example.com",
            subject="Daily Report - {{$now.format('YYYY-MM-DD')}}",
            text="{{$json.report}}"
        )
        self.connect_nodes(workflow, code_node, email_node)
        
        self.organize_layout(workflow)
        return workflow

    def create_sample_calendar_sync_workflow(self) -> Dict:
        workflow = self.create_basic_workflow(
            name="Calendar Sync",
            description="Syncs calendar events every hour"
        )
        
        trigger = self.add_trigger_node(
            workflow, 
            "interval", 
            {"interval": 60}
        )
        
        http_node = self.add_http_request_node(
            workflow,
            url="https://calendar-api.example.com/events",
            method="GET"
        )
        self.connect_nodes(workflow, trigger, http_node)
        
        code_node = self.add_code_node(
            workflow,
            code="""
const events = items[0].json.events;
const upcomingEvents = events.filter(e => new Date(e.start) > new Date());
return upcomingEvents.map(e => ({json: e}));
"""
        )
        self.connect_nodes(workflow, http_node, code_node)
        
        slack_node = self.add_slack_node(
            workflow,
            channel="#calendar",
            message="Upcoming event: {{$json.title}} at {{$json.start}}"
        )
        self.connect_nodes(workflow, code_node, slack_node)
        
        self.organize_layout(workflow)
        return workflow
