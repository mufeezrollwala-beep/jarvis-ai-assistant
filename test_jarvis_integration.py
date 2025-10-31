import sys

print("Testing Jarvis Home Automation Integration...")
print()

print("1. Testing imports...")
try:
    from home_automation import HomeAutomationService, DeviceType, DeviceState
    print("   ✓ home_automation module imported")
except Exception as e:
    print(f"   ✗ Failed to import home_automation: {e}")
    sys.exit(1)

print()
print("2. Testing jarvis module structure...")
try:
    import jarvis
    print("   ✓ jarvis module imported")
    
    if hasattr(jarvis, 'Jarvis'):
        print("   ✓ Jarvis class found")
    else:
        print("   ✗ Jarvis class not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_initialize_home_automation'):
        print("   ✓ _initialize_home_automation method found")
    else:
        print("   ✗ _initialize_home_automation method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_handle_light_command'):
        print("   ✓ _handle_light_command method found")
    else:
        print("   ✗ _handle_light_command method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_handle_thermostat_command'):
        print("   ✓ _handle_thermostat_command method found")
    else:
        print("   ✗ _handle_thermostat_command method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_handle_plug_command'):
        print("   ✓ _handle_plug_command method found")
    else:
        print("   ✗ _handle_plug_command method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_handle_scene_command'):
        print("   ✓ _handle_scene_command method found")
    else:
        print("   ✗ _handle_scene_command method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_list_devices'):
        print("   ✓ _list_devices method found")
    else:
        print("   ✗ _list_devices method not found")
        sys.exit(1)
    
    if hasattr(jarvis.Jarvis, '_show_home_status'):
        print("   ✓ _show_home_status method found")
    else:
        print("   ✗ _show_home_status method not found")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ Failed to test jarvis module: {e}")
    sys.exit(1)

print()
print("3. Checking file structure...")
import os

expected_files = [
    'jarvis.py',
    'home_automation/__init__.py',
    'home_automation/base.py',
    'home_automation/service.py',
    'home_automation/config.py',
    'home_automation/mock_api.py',
    'home_automation/adapters/__init__.py',
    'home_automation/adapters/home_assistant.py',
    'home_automation/adapters/hue.py',
    'home_automation/adapters/tplink.py',
    'tests/test_home_automation.py',
    'demo_home_automation.py',
    'README.md',
    'HOME_AUTOMATION_GUIDE.md',
    'QUICK_START.md',
    'requirements.txt',
    'config.example.json',
    '.gitignore'
]

missing_files = []
for file in expected_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} (missing)")
        missing_files.append(file)

if missing_files:
    print(f"\n   Missing {len(missing_files)} file(s)")
    sys.exit(1)

print()
print("=" * 60)
print("✓ All integration checks passed!")
print("=" * 60)
print()
print("The home automation integration is ready to use.")
print()
print("Next steps:")
print("  • Run: python tests/test_home_automation.py")
print("  • Run: python demo_home_automation.py")
print("  • Read: HOME_AUTOMATION_GUIDE.md for full documentation")
