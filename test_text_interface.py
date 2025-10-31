#!/usr/bin/env python3
"""
Basic tests for the text interface
"""
import pytest
from jarvis_core import JarvisCore
from fastapi.testclient import TestClient
from text_api import app, API_KEY
import json


class TestJarvisCore:
    """Test the core command processing logic"""
    
    def test_time_command(self):
        core = JarvisCore()
        response = core.process_command("what time is it")
        assert response['success'] is True
        assert response['action'] == 'get_time'
        assert 'time' in response['message'].lower()
        assert response['data'] is not None
    
    def test_wikipedia_command(self):
        core = JarvisCore()
        response = core.process_command("wikipedia python")
        assert response['success'] is True
        assert response['action'] == 'wikipedia_search'
        assert 'Wikipedia' in response['message']
    
    def test_open_youtube_command(self):
        core = JarvisCore()
        response = core.process_command("open youtube")
        assert response['success'] is True
        assert response['action'] == 'open_website'
        assert response['data'] == 'youtube.com'
    
    def test_open_google_command(self):
        core = JarvisCore()
        response = core.process_command("open google")
        assert response['success'] is True
        assert response['action'] == 'open_website'
        assert response['data'] == 'google.com'
    
    def test_unknown_command(self):
        core = JarvisCore()
        response = core.process_command("do something unknown")
        assert response['success'] is True
        assert response['action'] == 'unknown'
        assert 'not sure' in response['message'].lower()
    
    def test_exit_command(self):
        core = JarvisCore()
        response = core.process_command("exit")
        assert response['success'] is True
        assert response['action'] == 'exit'
        assert 'goodbye' in response['message'].lower()
    
    def test_get_status(self):
        core = JarvisCore()
        core.process_command("test command")
        status = core.get_status()
        assert status['status'] == 'active'
        assert status['commands_processed'] >= 1
    
    def test_get_greeting(self):
        core = JarvisCore()
        greeting = core.get_greeting()
        assert 'Jarvis' in greeting
        assert any(word in greeting for word in ['Morning', 'Afternoon', 'Evening'])


class TestFastAPI:
    """Test the FastAPI endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
        self.headers = {"X-API-Key": API_KEY}
    
    def test_root_endpoint(self):
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
        assert 'Jarvis' in data['name']
    
    def test_commands_endpoint_success(self):
        response = self.client.post(
            "/commands",
            json={"command": "what time is it"},
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['action'] == 'get_time'
    
    def test_commands_endpoint_no_auth(self):
        response = self.client.post(
            "/commands",
            json={"command": "what time is it"}
        )
        assert response.status_code == 403
    
    def test_commands_endpoint_invalid_auth(self):
        response = self.client.post(
            "/commands",
            json={"command": "what time is it"},
            headers={"X-API-Key": "invalid-key"}
        )
        assert response.status_code == 403
    
    def test_status_endpoint_success(self):
        response = self.client.get("/status", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'active'
        assert 'commands_processed' in data
    
    def test_status_endpoint_no_auth(self):
        response = self.client.get("/status")
        assert response.status_code == 403
    
    def test_websocket_invalid_auth(self):
        with pytest.raises(Exception):
            with self.client.websocket_connect("/stream?api_key=invalid"):
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
