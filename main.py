#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jarvis import Jarvis
from jarvis.config import load_config


def main():
    try:
        config = load_config()
        jarvis = Jarvis(config)
        jarvis.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
