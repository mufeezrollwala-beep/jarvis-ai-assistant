#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ui.dashboard import JarvisDashboard


def main():
    parser = argparse.ArgumentParser(
        description='Launch the Jarvis AI Assistant Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_ui.py              # Launch with real-time data
  python scripts/run_ui.py --mock       # Launch with mock data for development
  python scripts/run_ui.py --headless   # Launch in headless-safe mode
        """
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Run in mock data mode for development and testing'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless-safe mode (uses offscreen rendering)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Jarvis Dashboard 1.0.0'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  J.A.R.V.I.S - Just A Rather Very Intelligent System")
    print("  Dashboard Interface v1.0.0")
    print("=" * 70)
    
    if args.mock:
        print("  Mode: Mock Data (Development)")
    else:
        print("  Mode: Real-Time")
    
    if args.headless:
        print("  Display: Headless (Offscreen)")
    else:
        print("  Display: Normal")
    
    print("=" * 70)
    print()
    
    try:
        dashboard = JarvisDashboard(mock_mode=args.mock, headless_safe=args.headless)
        exit_code = dashboard.run()
        
        print()
        print("Dashboard closed.")
        return exit_code
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user.")
        return 0
    except Exception as e:
        print(f"\n\nError: {e}")
        if args.headless:
            print("Dashboard failed to initialize in headless mode.")
        else:
            print("Dashboard failed to initialize.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
