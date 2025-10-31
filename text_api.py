import os
import asyncio
from typing import Optional, List, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from jarvis_core import JarvisCore
import json


app = FastAPI(title="Jarvis Text API", description="Text interface for Jarvis assistant", version="1.0.0")

jarvis_core = JarvisCore()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

API_KEY = os.environ.get("JARVIS_API_KEY", "jarvis-secret-key-123")


class CommandRequest(BaseModel):
    command: str
    user_id: Optional[str] = None


class CommandResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    action: Optional[str] = None
    timestamp: str


class StatusResponse(BaseModel):
    status: str
    uptime: float
    commands_processed: int
    last_command: Optional[dict] = None
    timestamp: str


class ConnectionManager:
    """Manages WebSocket connections for streaming updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass


manager = ConnectionManager()


def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    """Verify API key from header"""
    if api_key is None or api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )
    return api_key


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Jarvis Text API",
        "version": "1.0.0",
        "endpoints": {
            "POST /commands": "Send a text command",
            "GET /status": "Get system status",
            "WebSocket /stream": "Real-time command updates"
        },
        "authentication": f"Include '{API_KEY_NAME}' header with your API key"
    }


@app.post("/commands", response_model=CommandResponse)
async def process_command(
    request: CommandRequest,
    api_key: str = Depends(verify_api_key)
) -> CommandResponse:
    """
    Process a text command
    
    Requires authentication via X-API-Key header
    """
    try:
        response = jarvis_core.process_command(request.command)
        
        broadcast_data = {
            'type': 'command_processed',
            'command': request.command,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(broadcast_data))
        
        return CommandResponse(
            success=response['success'],
            message=response['message'],
            data=response.get('data'),
            action=response.get('action'),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status", response_model=StatusResponse)
async def get_status(api_key: str = Depends(verify_api_key)) -> StatusResponse:
    """
    Get current system status
    
    Requires authentication via X-API-Key header
    """
    try:
        status = jarvis_core.get_status()
        return StatusResponse(
            status=status['status'],
            uptime=status['uptime'],
            commands_processed=status['commands_processed'],
            last_command=status['last_command'],
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    
    Sends incremental updates about command processing, transcripts, and task status
    
    Query parameter authentication: ws://host/stream?api_key=your-key
    """
    api_key = websocket.query_params.get("api_key")
    
    if api_key != API_KEY:
        await websocket.close(code=1008, reason="Invalid API key")
        return
    
    await manager.connect(websocket)
    
    try:
        await websocket.send_text(json.dumps({
            'type': 'connection',
            'message': 'Connected to Jarvis stream',
            'timestamp': datetime.now().isoformat()
        }))
        
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                if message_data.get('type') == 'command':
                    command = message_data.get('command', '')
                    
                    await websocket.send_text(json.dumps({
                        'type': 'processing',
                        'message': f'Processing command: {command}',
                        'timestamp': datetime.now().isoformat()
                    }))
                    
                    response = jarvis_core.process_command(command)
                    
                    await websocket.send_text(json.dumps({
                        'type': 'result',
                        'command': command,
                        'response': response,
                        'timestamp': datetime.now().isoformat()
                    }))
                    
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON format',
                    'timestamp': datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
