"""
News Monitoring and Analytics Application
CO7095 - Software Measurement and Quality Assurance (2026-2027)

Main application entry point.
Run with: python main.py
"""

import sys
import os

# Ensure the project root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface.menu import MainMenu


def main():
    """Main execution function."""
    try:
        app = MainMenu()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting safely...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected exception occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
