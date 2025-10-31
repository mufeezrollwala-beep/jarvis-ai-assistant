import asyncio
import sys
from home_automation import HomeAutomationService, DeviceType


async def demo():
    print("=" * 60)
    print("JARVIS HOME AUTOMATION DEMO")
    print("=" * 60)
    print()
    
    print("Initializing home automation service...")
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    print()
    
    print("-" * 60)
    print("DEVICE DISCOVERY")
    print("-" * 60)
    devices = service.list_devices()
    print(f"✓ Discovered {len(devices)} devices")
    
    lights = service.list_devices(device_type=DeviceType.LIGHT)
    plugs = service.list_devices(device_type=DeviceType.PLUG)
    thermostats = service.list_devices(device_type=DeviceType.THERMOSTAT)
    
    print(f"  - {len(lights)} lights")
    print(f"  - {len(plugs)} smart plugs")
    print(f"  - {len(thermostats)} thermostats")
    print()
    
    print("-" * 60)
    print("SCENE DISCOVERY")
    print("-" * 60)
    scenes = service.list_scenes()
    print(f"✓ Discovered {len(scenes)} scenes:")
    for scene in scenes:
        print(f"  - {scene.name}: {scene.description}")
    print()
    
    print("-" * 60)
    print("DEMONSTRATION: Good Morning Routine")
    print("-" * 60)
    print("Voice command: 'Good morning scene'")
    await asyncio.sleep(1)
    await service.activate_scene("good morning")
    print("✓ Bedroom lights turned on")
    print("✓ Kitchen lights turned on")
    print("✓ Coffee maker started")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("DEMONSTRATION: Office Work Setup")
    print("-" * 60)
    print("Voice command: 'Turn on office lights'")
    await asyncio.sleep(1)
    await service.turn_on_device("office lights")
    print("✓ Office lights turned on at 100% brightness")
    print()
    
    print("Voice command: 'Set thermostat to 22 degrees'")
    await asyncio.sleep(1)
    await service.set_thermostat_temperature("main thermostat", 22)
    print("✓ Thermostat set to 22°C")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("DEMONSTRATION: Movie Time")
    print("-" * 60)
    print("Voice command: 'Activate movie time scene'")
    await asyncio.sleep(1)
    await service.activate_scene("movie time")
    print("✓ Living room lights dimmed to 20%")
    print("✓ Ambient lighting enabled")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("DEMONSTRATION: Leaving Home")
    print("-" * 60)
    print("Voice command: 'Activate away mode'")
    await asyncio.sleep(1)
    await service.activate_scene("away")
    print("✓ All lights turned off")
    print("✓ Smart plugs turned off")
    print("✓ Front door locked")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("CURRENT HOME STATUS")
    print("-" * 60)
    print(service.get_device_summary())
    print()
    
    print("-" * 60)
    print("DEMONSTRATION: Individual Light Control")
    print("-" * 60)
    print("Voice command: 'Turn on living room lights'")
    await service.turn_on_device("living room lights")
    print("✓ Living room lights on")
    print()
    
    print("Voice command: 'Dim living room lights'")
    await asyncio.sleep(1)
    await service.dim_light("living room lights", 50)
    device = await service.get_device_state("light.living_room")
    print(f"✓ Living room lights dimmed to {device.attributes.get('brightness')}%")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("DEMONSTRATION: Room Control")
    print("-" * 60)
    print("Voice command: 'Turn off bedroom'")
    await asyncio.sleep(1)
    await service.turn_off_room("bedroom")
    print("✓ All bedroom devices turned off")
    print()
    
    await asyncio.sleep(2)
    
    print("-" * 60)
    print("ADAPTER INFORMATION")
    print("-" * 60)
    print(f"Active adapters: {', '.join(service.adapters.keys())}")
    for adapter_name, adapter in service.adapters.items():
        devices = adapter.list_devices()
        scenes = adapter.list_scenes()
        print(f"  {adapter_name}:")
        print(f"    - {len(devices)} devices")
        print(f"    - {len(scenes)} scenes")
    print()
    
    print("-" * 60)
    print("CLEANUP")
    print("-" * 60)
    await service.shutdown()
    print("✓ Home automation service shut down")
    print()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print("Try these voice commands with Jarvis:")
    print("  • 'Turn on office lights'")
    print("  • 'Dim bedroom lights'")
    print("  • 'Set thermostat to 20 degrees'")
    print("  • 'Turn on the coffee maker'")
    print("  • 'Activate good morning scene'")
    print("  • 'List devices'")
    print("  • 'Show home status'")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
