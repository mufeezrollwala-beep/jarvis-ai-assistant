#!/usr/bin/env python3
"""
Quick verification script to check if all components are working
"""
import sys
import importlib


def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError:
        print(f"✗ {package_name or module_name} - NOT INSTALLED")
        return False


def verify_installation():
    """Verify that all required components are installed"""
    print("=" * 60)
    print("Jarvis Text Interface - Installation Verification")
    print("=" * 60)
    print("\nChecking dependencies...\n")
    
    # Core dependencies
    print("Core Dependencies:")
    core_deps = [
        ('wikipedia', 'wikipedia'),
        ('requests', 'requests'),
    ]
    
    core_ok = all(check_import(mod, pkg) for mod, pkg in core_deps)
    
    # FastAPI dependencies
    print("\nFastAPI Dependencies:")
    api_deps = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('pydantic', 'pydantic'),
        ('websockets', 'websockets'),
    ]
    
    api_ok = all(check_import(mod, pkg) for mod, pkg in api_deps)
    
    # CLI dependencies
    print("\nCLI Dependencies:")
    cli_deps = [
        ('typer', 'typer'),
        ('rich', 'rich'),
    ]
    
    cli_ok = all(check_import(mod, pkg) for mod, pkg in cli_deps)
    
    # Voice dependencies (optional)
    print("\nVoice Dependencies (optional):")
    voice_deps = [
        ('speech_recognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
    ]
    
    voice_ok = all(check_import(mod, pkg) for mod, pkg in voice_deps)
    
    # Check project modules
    print("\nProject Modules:")
    project_modules = [
        ('jarvis_core', 'jarvis_core.py'),
        ('text_api', 'text_api.py'),
        ('cli_client', 'cli_client.py'),
    ]
    
    project_ok = all(check_import(mod, pkg) for mod, pkg in project_modules)
    
    print("\n" + "=" * 60)
    
    if core_ok and api_ok and cli_ok and project_ok:
        print("✓ All required components are installed!")
        print("\nYou can now:")
        print("  1. Start the API server:  python text_api.py")
        print("  2. Use the CLI client:    python cli_client.py command \"time\" --direct")
        print("  3. Run the demo:          python demo.py")
        print("\nSee QUICKSTART.md for more details.")
        return True
    else:
        print("✗ Some components are missing!")
        print("\nInstall missing dependencies:")
        print("  pip install -r requirements.txt")
        return False
    
    print("=" * 60)


if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)
