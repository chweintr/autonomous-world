"""
Flask web application for the autonomous world system.
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from typing import Dict

from src.engine.world_state import WorldState
from src.engine.simulation import Simulation, SimulationConfig
from src.models.interaction import Interaction
from src.engine.prompt_extractor import PromptExtractor


app = Flask(__name__, 
           template_folder='../../web/templates',
           static_folder='../../web/static')

# Global simulation state
current_simulation: Simulation = None
world_state: WorldState = None


def initialize_world():
    """Initialize the world state from data files."""
    global world_state
    
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    characters_dir = os.path.join(base_dir, 'data', 'characters')
    locations_dir = os.path.join(base_dir, 'data', 'locations')
    
    characters = WorldState.load_characters_from_directory(characters_dir)
    locations = WorldState.load_locations_from_directory(locations_dir)
    
    world_state = WorldState(characters, locations)
    return world_state


@app.route('/')
def index():
    """Main interface page."""
    return render_template('index_v2.html')

@app.route('/classic')
def index_classic():
    """Classic interface (fallback)."""
    return render_template('index.html')


@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get list of all characters."""
    if world_state is None:
        initialize_world()
    
    characters = []
    for char in world_state.characters.values():
        characters.append({
            'id': char.id,
            'name': char.name,
            'archetype': char.archetype,
            'physical_description': char.physical_description[:100] + '...',
            'current_location': char.current_location,
            'emotional_state': char.emotional_state.value,
            'animal': {
                'species': char.animal_companion.species,
                'name': char.animal_companion.name
            }
        })
    
    return jsonify(characters)


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get list of all locations."""
    if world_state is None:
        initialize_world()
    
    locations = []
    for loc in world_state.locations.values():
        locations.append({
            'id': loc.id,
            'name': loc.name,
            'description': loc.description,
            'atmosphere': loc.atmosphere,
            'current_time': loc.current_time.value,
            'current_weather': loc.current_weather.value
        })
    
    return jsonify(locations)


@app.route('/api/scenario/seed', methods=['POST'])
def seed_scenario():
    """Seed a scenario by placing characters in locations."""
    global current_simulation, world_state
    
    if world_state is None:
        initialize_world()
    
    data = request.json
    placements = data.get('placements', {})
    config_data = data.get('config', {})
    use_llm = data.get('use_llm', False)
    
    # Create simulation config
    config = SimulationConfig(
        autonomy_level=config_data.get('autonomy_level', 0.75),
        time_compression=config_data.get('time_compression', 60),
        interaction_density=config_data.get('interaction_density', 'moderate'),
        narrative_coherence=config_data.get('narrative_coherence', 'loose'),
        randomness=config_data.get('randomness', 0.25)
    )
    
    # Create new simulation
    current_simulation = Simulation(world_state, config, use_llm=use_llm)
    
    # Place characters
    current_simulation.seed_scenario(placements)
    
    return jsonify({
        'status': 'success',
        'message': f'Scenario seeded with {len(placements)} characters'
    })


@app.route('/api/simulation/run', methods=['POST'])
def run_simulation():
    """Run the simulation for a specified duration."""
    global current_simulation
    
    if current_simulation is None:
        return jsonify({'status': 'error', 'message': 'No simulation initialized'}), 400
    
    data = request.json
    duration = data.get('duration_minutes', 60)
    
    # Run simulation
    interactions = []
    
    def callback(interaction: Interaction):
        interactions.append(interaction.to_dict())
    
    current_simulation.run_simulation(duration, callback=callback)
    
    return jsonify({
        'status': 'success',
        'interactions_count': len(interactions),
        'interactions': interactions
    })


@app.route('/api/simulation/status', methods=['GET'])
def get_simulation_status():
    """Get current simulation status."""
    if current_simulation is None:
        return jsonify({'status': 'no_simulation'})

    return jsonify({
        'status': 'active' if current_simulation.is_running else 'paused',
        'current_time': current_simulation.world.current_time.isoformat(),
        'interactions_count': len(current_simulation.world.interactions_log),
        'characters': {
            char.id: {
                'location': char.current_location,
                'emotional_state': char.emotional_state.value,
                'intensity': char.emotional_intensity
            }
            for char in current_simulation.world.characters.values()
        }
    })


@app.route('/api/interactions/recent', methods=['GET'])
def get_recent_interactions():
    """Get recent interactions."""
    if current_simulation is None:
        return jsonify([])

    count = request.args.get('count', 10, type=int)
    interactions = current_simulation.world.get_recent_interactions(count)

    return jsonify([interaction.to_dict() for interaction in interactions])


@app.route('/api/emergence/report', methods=['GET'])
def get_emergence_report():
    """Get emergence patterns report."""
    if current_simulation is None:
        return jsonify({'status': 'error', 'message': 'No simulation running'}), 400
    
    report = current_simulation.get_emergence_report()
    
    return jsonify({
        'status': 'success',
        'report': report
    })


@app.route('/api/session/save', methods=['POST'])
def save_session():
    """Save the current session as field notes."""
    if current_simulation is None:
        return jsonify({'status': 'error', 'message': 'No simulation to save'}), 400

    data = request.json
    session_name = data.get('name', 'session')

    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    sessions_dir = os.path.join(base_dir, 'data', 'sessions')

    filepath = current_simulation.world.save_session(session_name, sessions_dir)

    return jsonify({
        'status': 'success',
        'filepath': filepath,
        'message': f'Session saved to {filepath}'
    })


@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    """Reset the simulation."""
    global current_simulation, world_state
    
    initialize_world()
    current_simulation = None
    
    return jsonify({
        'status': 'success',
        'message': 'Simulation reset'
    })


@app.route('/api/paintable/extract', methods=['POST'])
def extract_paintable_moments():
    """Extract paintable moments and generate prompts."""
    if current_simulation is None or len(current_simulation.world.interactions_log) == 0:
        return jsonify({'status': 'error', 'message': 'No interactions to analyze'}), 400

    data = request.json
    top_n = data.get('top_n', 5)
    use_llm = data.get('use_llm', False)

    # Create extractor
    api_key = os.environ.get('OPENAI_API_KEY') if use_llm else None
    extractor = PromptExtractor(use_llm=use_llm, api_key=api_key)

    # Extract paintable moments
    prompts = extractor.extract_paintable_moments(
        current_simulation.world.interactions_log,
        top_n=top_n
    )
    
    # Format for response
    paintable_moments = []
    for prompt in prompts:
        paintable_moments.append({
            'timestamp': prompt.source_interaction.timestamp.isoformat(),
            'location': prompt.source_interaction.location_name,
            'composition': prompt.composition_description,
            'color_notes': prompt.color_notes,
            'gesture_notes': prompt.gesture_notes,
            'painting_prompt': prompt.painting_prompt,
            'image_gen_prompt': prompt.image_gen_prompt,
            'why_paintable': prompt.why_paintable,
            'original_field_note': prompt.source_interaction.to_field_note()
        })
    
    return jsonify({
        'status': 'success',
        'count': len(paintable_moments),
        'moments': paintable_moments
    })


# Initialize world state on module load for production (gunicorn)
try:
    initialize_world()
    print(f"✓ Initialized world: {len(world_state.characters)} characters, {len(world_state.locations)} locations")
except Exception as e:
    print(f"Warning: Could not initialize world state: {e}")


if __name__ == '__main__':
    if world_state is None:
        initialize_world()
    print("Starting Autonomous World System...")
    print(f"Loaded {len(world_state.characters)} characters")
    print(f"Loaded {len(world_state.locations)} locations")
    app.run(debug=True, port=5000)

