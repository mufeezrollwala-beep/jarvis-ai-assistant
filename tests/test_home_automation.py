import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from home_automation import HomeAutomationService, DeviceType, DeviceState


async def test_basic_operations():
    print("=== Testing Home Automation Service ===\n")
    
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    print("\n1. Testing device discovery...")
    devices = service.list_devices()
    print(f"   Found {len(devices)} devices")
    assert len(devices) > 0, "Should discover devices"
    
    print("\n2. Testing device listing by type...")
    lights = service.list_devices(device_type=DeviceType.LIGHT)
    print(f"   Found {len(lights)} lights")
    assert len(lights) > 0, "Should find lights"
    
    print("\n3. Testing find device by name...")
    device = service.find_device_by_name("office lights")
    assert device is not None, "Should find office lights"
    print(f"   Found: {device.name} ({device.device_id})")
    
    print("\n4. Testing turn on light...")
    success = await service.turn_on_device("office lights")
    assert success, "Should turn on office lights"
    device = await service.get_device_state(device.device_id)
    assert device.state == DeviceState.ON, "Office lights should be on"
    print(f"   Office lights state: {device.state.value}")
    
    print("\n5. Testing dim light...")
    success = await service.dim_light("office lights", 50)
    assert success, "Should dim office lights"
    device = await service.get_device_state(device.device_id)
    assert device.attributes.get('brightness') == 50, "Brightness should be 50"
    print(f"   Office lights brightness: {device.attributes.get('brightness')}")
    
    print("\n6. Testing turn off light...")
    success = await service.turn_off_device("office lights")
    assert success, "Should turn off office lights"
    device = await service.get_device_state(device.device_id)
    assert device.state == DeviceState.OFF, "Office lights should be off"
    print(f"   Office lights state: {device.state.value}")
    
    print("\n7. Testing thermostat control...")
    success = await service.set_thermostat_temperature("main thermostat", 22)
    assert success, "Should set thermostat temperature"
    device = service.find_device_by_name("main thermostat")
    print(f"   Thermostat target temperature: {device.attributes.get('target_temperature')}")
    
    print("\n8. Testing smart plug control...")
    success = await service.turn_on_device("coffee maker")
    assert success, "Should turn on coffee maker"
    device = await service.get_device_state("plug.coffee_maker")
    assert device.state == DeviceState.ON, "Coffee maker should be on"
    print(f"   Coffee maker state: {device.state.value}")
    
    print("\n9. Testing scene listing...")
    scenes = service.list_scenes()
    print(f"   Found {len(scenes)} scenes")
    assert len(scenes) > 0, "Should find scenes"
    for scene in scenes:
        print(f"   - {scene.name}: {scene.description}")
    
    print("\n10. Testing scene activation...")
    success = await service.activate_scene("movie time")
    assert success, "Should activate movie time scene"
    print("   Movie time scene activated")
    
    print("\n11. Testing room control...")
    success = await service.turn_off_room("office")
    assert success, "Should turn off office devices"
    print("   Office devices turned off")
    
    print("\n12. Testing device summary...")
    summary = service.get_device_summary()
    print(summary)
    
    await service.shutdown()
    
    print("\n=== All tests passed! ===")


async def test_multiple_adapters():
    print("\n=== Testing Multiple Adapters ===\n")
    
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    print(f"Active adapters: {list(service.adapters.keys())}")
    
    for adapter_name, adapter in service.adapters.items():
        devices = adapter.list_devices()
        scenes = adapter.list_scenes()
        print(f"  {adapter_name}: {len(devices)} devices, {len(scenes)} scenes")
    
    await service.shutdown()
    
    print("\n=== Adapter test passed! ===")


async def test_natural_language_commands():
    print("\n=== Testing Natural Language Commands ===\n")
    
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    test_commands = [
        ("Turn on living room lights", lambda: service.turn_on_device("living room")),
        ("Dim bedroom lights", lambda: service.dim_light("bedroom lights", 30)),
        ("Activate good morning scene", lambda: service.activate_scene("good morning")),
        ("Turn off kitchen", lambda: service.turn_off_room("kitchen")),
    ]
    
    for description, command in test_commands:
        print(f"Command: {description}")
        result = await command()
        print(f"  Result: {'Success' if result else 'Failed'}\n")
    
    await service.shutdown()
    
    print("=== Natural language test completed! ===")


if __name__ == "__main__":
    print("Starting Home Automation Tests...\n")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(test_basic_operations())
        loop.run_until_complete(test_multiple_adapters())
        loop.run_until_complete(test_natural_language_commands())
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        loop.close()
    
    print("\n✓ All tests completed successfully!")
