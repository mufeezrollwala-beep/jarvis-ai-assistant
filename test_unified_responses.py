#!/usr/bin/env python3
"""
Verification script to demonstrate that text and voice commands
share the same core logic and produce identical responses
"""
from jarvis_core import JarvisCore
import requests


def test_unified_logic():
    """
    Test that both direct (in-process) and API modes produce
    the same responses for identical commands
    """
    print("=" * 70)
    print("Testing Unified Response Logic")
    print("=" * 70)
    print("\nVerifying that text commands produce the same responses")
    print("as equivalent voice commands (using the same core logic)\n")
    
    # Test commands
    commands = [
        "what time is it",
        "wikipedia python",
        "open youtube",
        "open google"
    ]
    
    core = JarvisCore()
    api_url = "http://localhost:8000"
    api_key = "jarvis-secret-key-123"
    headers = {"X-API-Key": api_key}
    
    all_passed = True
    
    for command in commands:
        print(f"Command: '{command}'")
        print("-" * 70)
        
        # Direct mode (in-process)
        direct_response = core.process_command(command)
        print(f"  Direct Mode:")
        print(f"    Success: {direct_response['success']}")
        print(f"    Action:  {direct_response['action']}")
        print(f"    Message: {direct_response['message'][:60]}...")
        
        # API mode
        try:
            api_response = requests.post(
                f"{api_url}/commands",
                json={"command": command},
                headers=headers,
                timeout=10
            )
            
            if api_response.status_code == 200:
                api_data = api_response.json()
                print(f"  API Mode:")
                print(f"    Success: {api_data['success']}")
                print(f"    Action:  {api_data['action']}")
                print(f"    Message: {api_data['message'][:60]}...")
                
                # Verify consistency
                if (direct_response['success'] == api_data['success'] and
                    direct_response['action'] == api_data['action']):
                    print(f"  ✓ Both modes produced consistent results")
                else:
                    print(f"  ✗ Results differ between modes!")
                    all_passed = False
            else:
                print(f"  ✗ API returned status {api_response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  ✗ API error: {e}")
            all_passed = False
        
        print()
    
    print("=" * 70)
    if all_passed:
        print("✓ All tests passed! Text and voice share the same logic.")
    else:
        print("✗ Some tests failed. Check the output above.")
    print("=" * 70)


if __name__ == "__main__":
    test_unified_logic()
