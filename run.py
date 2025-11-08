#!/usr/bin/env python3
"""
Main entry point for the Autonomous World System.

This script can be used to run the web interface or command-line simulations.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.api.app import app, initialize_world


def main():
    """Run the web application."""
    print("=" * 60)
    print("AUTONOMOUS WORLD SYSTEM")
    print("A generative engine for visual art production")
    print("=" * 60)
    print()
    
    # Initialize world
    print("Initializing world...")
    world_state = initialize_world()
    
    print(f"✓ Loaded {len(world_state.characters)} characters:")
    for char in world_state.characters.values():
        print(f"  - {char.name} ({char.archetype})")
    
    print(f"\n✓ Loaded {len(world_state.locations)} locations:")
    for loc in world_state.locations.values():
        print(f"  - {loc.name}")
    
    print("\n" + "=" * 60)
    print("Starting web server...")
    print("Access the interface at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Run Flask app
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()


