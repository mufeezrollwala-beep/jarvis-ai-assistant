#!/usr/bin/env python3
"""
Demo script to showcase the text interface functionality
"""
import time
import requests
import json
from jarvis_core import JarvisCore


def demo_direct_mode():
    """Demonstrate direct command processing without API"""
    print("=" * 60)
    print("DEMO: Direct Mode (In-Process)")
    print("=" * 60)
    
    core = JarvisCore()
    
    # Test various commands
    test_commands = [
        "what time is it",
        "wikipedia python programming",
        "open youtube",
    ]
    
    for command in test_commands:
        print(f"\n➤ Command: {command}")
        response = core.process_command(command)
        print(f"✓ Response: {response['message']}")
        if response.get('data'):
            print(f"  Data: {json.dumps(response['data'], indent=2)}")
        time.sleep(1)
    
    print("\n" + "=" * 60)


def demo_api_mode():
    """Demonstrate API-based command processing"""
    print("\n" + "=" * 60)
    print("DEMO: API Mode (via FastAPI)")
    print("=" * 60)
    print("\nNote: This requires the API server to be running.")
    print("Start it with: python text_api.py\n")
    
    api_url = "http://localhost:8000"
    api_key = "jarvis-secret-key-123"
    headers = {"X-API-Key": api_key}
    
    try:
        # Test root endpoint
        print("Testing API availability...")
        response = requests.get(api_url, timeout=2)
        if response.status_code == 200:
            print("✓ API is running!")
        
        # Test status endpoint
        print("\n➤ Getting status...")
        response = requests.get(f"{api_url}/status", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Status: {data['status']}")
            print(f"  Commands processed: {data['commands_processed']}")
        
        # Test command endpoint
        test_commands = [
            "what time is it",
            "wikipedia artificial intelligence",
        ]
        
        for command in test_commands:
            print(f"\n➤ Command: {command}")
            response = requests.post(
                f"{api_url}/commands",
                json={"command": command},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Response: {data['message']}")
                if data.get('data'):
                    print(f"  Action: {data['action']}")
            else:
                print(f"✗ Error: HTTP {response.status_code}")
            
            time.sleep(1)
        
        print("\n" + "=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API server.")
        print("  Make sure to start it with: python text_api.py")
        print("\n" + "=" * 60)
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\n" + "=" * 60)


def print_usage():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("USAGE INSTRUCTIONS")
    print("=" * 60)
    print("""
1. Direct Mode (No API required):
   python cli_client.py command "what time is it" --direct
   python cli_client.py interactive --direct

2. API Mode (Requires API server):
   # Terminal 1: Start API server
   python text_api.py
   
   # Terminal 2: Use CLI client
   python cli_client.py command "what time is it"
   python cli_client.py interactive
   python cli_client.py stream

3. curl Examples:
   curl http://localhost:8000/
   
   curl -X POST http://localhost:8000/commands \\
     -H "X-API-Key: jarvis-secret-key-123" \\
     -H "Content-Type: application/json" \\
     -d '{"command": "what time is it"}'
   
   curl -X GET http://localhost:8000/status \\
     -H "X-API-Key: jarvis-secret-key-123"

4. Interactive Documentation:
   http://localhost:8000/docs (Swagger UI)
   http://localhost:8000/redoc (ReDoc)
""")
    print("=" * 60)


if __name__ == "__main__":
    print("\n🤖 Jarvis Text Interface Demo\n")
    
    # Run direct mode demo
    demo_direct_mode()
    
    # Run API mode demo
    demo_api_mode()
    
    # Print usage instructions
    print_usage()
    
    print("\n✓ Demo complete!\n")
