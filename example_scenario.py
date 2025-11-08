#!/usr/bin/env python3
"""
Example scenario demonstrating command-line usage of the simulation system.

This script shows how to use the system programmatically without the web interface.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.engine.world_state import WorldState
from src.engine.simulation import Simulation, SimulationConfig
from src.models.interaction import Interaction


def print_separator():
    print("\n" + "=" * 70 + "\n")


def run_example_scenario():
    """Run an example scenario: 'Confrontation at the Courtyard'"""
    
    print_separator()
    print("AUTONOMOUS WORLD SYSTEM - Example Scenario")
    print("Scenario: 'Confrontation at the Courtyard'")
    print_separator()
    
    # Load world data
    print("Loading world data...")
    base_dir = os.path.dirname(__file__)
    characters_dir = os.path.join(base_dir, 'data', 'characters')
    locations_dir = os.path.join(base_dir, 'data', 'locations')
    
    characters = WorldState.load_characters_from_directory(characters_dir)
    locations = WorldState.load_locations_from_directory(locations_dir)
    
    print(f"✓ Loaded {len(characters)} characters")
    print(f"✓ Loaded {len(locations)} locations")
    
    # Create world state
    world = WorldState(characters, locations)
    
    # Configure simulation
    config = SimulationConfig(
        autonomy_level=0.75,      # Characters mostly follow their drivers
        randomness=0.25,          # 25% chance of unexpected behavior
        interaction_density="moderate",  # Action every ~5 sim minutes
        time_compression=60       # 1 real second = 1 sim minute for this example
    )
    
    # Create simulation
    sim = Simulation(world, config, use_llm=False)
    
    # Seed the scenario
    print("\nSeeding scenario...")
    scenario_placements = {
        'rider_01': 'loc_courtyard',    # Marcus at courtyard
        'handler_01': 'loc_courtyard',  # Iris at courtyard (tension!)
        'witness_01': 'loc_rooftop'     # Witness observing from above
    }
    
    sim.seed_scenario(scenario_placements)
    
    print("✓ Placed Marcus Vale (The Rider) at The Courtyard")
    print("✓ Placed Iris Kahn (The Handler) at The Courtyard")
    print("✓ Placed The Witness at The Rooftop")
    
    # Run simulation
    print("\nRunning simulation for 60 simulated minutes...")
    print_separator()
    
    interaction_count = 0
    
    def interaction_callback(interaction: Interaction):
        """Called after each interaction is generated."""
        nonlocal interaction_count
        interaction_count += 1
        
        # Print field note
        print(interaction.to_field_note())
        print_separator()
    
    # Run for 60 simulated minutes
    sim.run_simulation(60, callback=interaction_callback)
    
    print(f"\nSimulation complete. Generated {interaction_count} interactions.")
    
    # Generate emergence report
    print("\nGenerating emergence patterns report...")
    print_separator()
    report = sim.get_emergence_report()
    print(report)
    print_separator()
    
    # Save session
    sessions_dir = os.path.join(base_dir, 'data', 'sessions')
    filepath = world.save_session('example_confrontation', sessions_dir)
    print(f"\n✓ Session saved to: {filepath}")
    
    print("\nExample complete!")
    print("\nTry modifying this script to:")
    print("  - Place different characters")
    print("  - Adjust simulation parameters")
    print("  - Run for longer durations")
    print("  - Enable LLM (set OPENAI_API_KEY and use_llm=True)")
    print_separator()


if __name__ == '__main__':
    run_example_scenario()


