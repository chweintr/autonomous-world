// Autonomous World System - Frontend JavaScript

let characters = [];
let locations = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadCharacters();
    await loadLocations();
    setupCharacterPlacements();
    updateStatus();
});

// Load characters from API
async function loadCharacters() {
    try {
        const response = await fetch('/api/characters');
        characters = await response.json();
        console.log('Loaded characters:', characters);
    } catch (error) {
        console.error('Error loading characters:', error);
    }
}

// Load locations from API
async function loadLocations() {
    try {
        const response = await fetch('/api/locations');
        locations = await response.json();
        console.log('Loaded locations:', locations);
    } catch (error) {
        console.error('Error loading locations:', error);
    }
}

// Setup character placement controls
function setupCharacterPlacements() {
    const container = document.getElementById('character-placements');
    container.innerHTML = '';

    characters.forEach(char => {
        const div = document.createElement('div');
        div.className = 'character-placement';

        const label = document.createElement('label');
        label.textContent = char.name;

        const select = document.createElement('select');
        select.id = `placement-${char.id}`;
        
        // Add "Not placed" option
        const noneOption = document.createElement('option');
        noneOption.value = '';
        noneOption.textContent = '-- Not placed --';
        select.appendChild(noneOption);

        // Add location options
        locations.forEach(loc => {
            const option = document.createElement('option');
            option.value = loc.id;
            option.textContent = loc.name;
            select.appendChild(option);
        });

        div.appendChild(label);
        div.appendChild(select);
        container.appendChild(div);
    });
}

// Seed scenario
async function seedScenario() {
    const placements = {};
    
    characters.forEach(char => {
        const select = document.getElementById(`placement-${char.id}`);
        if (select.value) {
            placements[char.id] = select.value;
        }
    });

    if (Object.keys(placements).length === 0) {
        alert('Please place at least one character before seeding.');
        return;
    }

    const config = {
        autonomy_level: parseFloat(document.getElementById('autonomy').value),
        randomness: parseFloat(document.getElementById('randomness').value),
        interaction_density: document.getElementById('density').value,
        time_compression: 60
    };

    const useLLM = document.getElementById('use-llm').checked;

    try {
        const response = await fetch('/api/scenario/seed', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ placements, config, use_llm: useLLM })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            updateStatus();
            alert(result.message);
        } else {
            alert('Error seeding scenario: ' + result.message);
        }
    } catch (error) {
        console.error('Error seeding scenario:', error);
        alert('Error seeding scenario. Check console for details.');
    }
}

// Run simulation
async function runSimulation() {
    const duration = parseInt(document.getElementById('duration').value);
    const runBtn = document.getElementById('run-btn');
    
    runBtn.disabled = true;
    runBtn.textContent = 'Running...';
    
    try {
        const response = await fetch('/api/simulation/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ duration_minutes: duration })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            displayInteractions(result.interactions);
            updateStatus();
            alert(`Simulation complete. ${result.interactions_count} interactions generated.`);
        } else {
            alert('Error running simulation: ' + result.message);
        }
    } catch (error) {
        console.error('Error running simulation:', error);
        alert('Error running simulation. Check console for details.');
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = 'Run Simulation';
    }
}

// Display interactions as field notes
function displayInteractions(interactions) {
    const container = document.getElementById('field-notes');
    container.innerHTML = '';

    if (interactions.length === 0) {
        container.innerHTML = '<p class="placeholder">No interactions generated.</p>';
        return;
    }

    interactions.forEach(interaction => {
        const note = document.createElement('div');
        note.className = 'field-note';

        const header = document.createElement('div');
        header.className = 'field-note-header';
        const time = new Date(interaction.timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        header.textContent = `[${time} - ${interaction.location_name} - ${interaction.time_of_day}]`;
        if (interaction.is_unexpected) {
            const badge = document.createElement('span');
            badge.className = 'emergence-badge';
            badge.textContent = 'EMERGENT';
            header.appendChild(badge);
        }

        const action = document.createElement('div');
        action.className = 'field-note-action';
        action.textContent = interaction.action_description;

        const material = document.createElement('div');
        material.className = 'field-note-material';
        material.textContent = 'Material details: ' + interaction.material_details;

        const temperature = document.createElement('div');
        temperature.className = 'field-note-temperature';
        temperature.textContent = 'Emotional temperature: ' + 
            interaction.emotional_temperature.charAt(0).toUpperCase() + 
            interaction.emotional_temperature.slice(1);

        note.appendChild(header);
        note.appendChild(action);
        note.appendChild(material);
        note.appendChild(temperature);

        container.appendChild(note);
    });

    // Scroll to top
    container.scrollTop = 0;
}

// Load and display emergence report
async function loadEmergenceReport() {
    try {
        const response = await fetch('/api/emergence/report');
        const result = await response.json();
        
        if (result.status === 'success') {
            const container = document.getElementById('emergence-report');
            container.innerHTML = '<pre>' + result.report + '</pre>';
        } else {
            alert('Error loading emergence report: ' + result.message);
        }
    } catch (error) {
        console.error('Error loading emergence report:', error);
        alert('Error loading emergence report. Make sure a simulation has been run.');
    }
}

// Update status display
async function updateStatus() {
    try {
        const response = await fetch('/api/simulation/status');
        const status = await response.json();
        
        const statusDiv = document.getElementById('status');
        
        if (status.status === 'no_simulation') {
            statusDiv.innerHTML = '<p>No simulation initialized. Seed a scenario to begin.</p>';
        } else {
            let html = `<p><strong>Status:</strong> ${status.status}</p>`;
            html += `<p><strong>Interactions:</strong> ${status.interactions_count}</p>`;
            
            if (status.characters) {
                html += '<p><strong>Character States:</strong></p><ul>';
                Object.entries(status.characters).forEach(([id, state]) => {
                    const char = characters.find(c => c.id === id);
                    if (char) {
                        const locName = state.location ? 
                            locations.find(l => l.id === state.location)?.name : 'None';
                        html += `<li>${char.name}: ${state.emotional_state} at ${locName}</li>`;
                    }
                });
                html += '</ul>';
            }
            
            statusDiv.innerHTML = html;
        }
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Save session
async function saveSession() {
    const name = prompt('Enter session name:', 'session_' + Date.now());
    if (!name) return;

    try {
        const response = await fetch('/api/session/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            alert(result.message);
        } else {
            alert('Error saving session: ' + result.message);
        }
    } catch (error) {
        console.error('Error saving session:', error);
        alert('Error saving session. Check console for details.');
    }
}

// Reset simulation
async function resetSimulation() {
    if (!confirm('Reset simulation? This will clear all current data.')) {
        return;
    }

    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const result = await response.json();
        
        if (result.status === 'success') {
            document.getElementById('field-notes').innerHTML = 
                '<p class="placeholder">Field notes will appear here after running the simulation...</p>';
            document.getElementById('emergence-report').innerHTML = 
                '<p class="placeholder">Pattern analysis will appear here...</p>';
            document.getElementById('paintable-moments').innerHTML = 
                '<p class="placeholder">Painting prompts will appear here...</p>';
            updateStatus();
            alert('Simulation reset successfully.');
        }
    } catch (error) {
        console.error('Error resetting simulation:', error);
        alert('Error resetting simulation. Check console for details.');
    }
}

// Extract paintable moments
async function extractPaintableMoments() {
    try {
        const useLLM = document.getElementById('use-llm').checked;
        
        const response = await fetch('/api/paintable/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ top_n: 5, use_llm: useLLM })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            displayPaintableMoments(result.moments);
        } else {
            alert('Error extracting moments: ' + result.message);
        }
    } catch (error) {
        console.error('Error extracting paintable moments:', error);
        alert('Error extracting moments. Make sure a simulation has been run.');
    }
}

// Display paintable moments
function displayPaintableMoments(moments) {
    const container = document.getElementById('paintable-moments');
    container.innerHTML = '';

    if (moments.length === 0) {
        container.innerHTML = '<p class="placeholder">No paintable moments found.</p>';
        return;
    }

    moments.forEach((moment, index) => {
        const div = document.createElement('div');
        div.className = 'paintable-moment';

        const header = document.createElement('div');
        header.className = 'paintable-header';
        const time = new Date(moment.timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        header.textContent = `Moment ${index + 1} [${time}] - ${moment.location}`;

        const composition = document.createElement('div');
        composition.className = 'paintable-section';
        composition.innerHTML = '<strong>COMPOSITION:</strong> ' + moment.composition;

        const color = document.createElement('div');
        color.className = 'paintable-section';
        color.innerHTML = '<strong>COLOR:</strong> ' + moment.color_notes;

        const gesture = document.createElement('div');
        gesture.className = 'paintable-section';
        gesture.innerHTML = '<strong>KEY GESTURE:</strong> ' + moment.gesture_notes;

        const paintingPrompt = document.createElement('div');
        paintingPrompt.className = 'paintable-prompt';
        paintingPrompt.innerHTML = '<strong>FOR YOU (PAINTER):</strong><br>' + moment.painting_prompt;

        const imagePrompt = document.createElement('div');
        imagePrompt.className = 'paintable-prompt';
        imagePrompt.innerHTML = '<strong>FOR IMAGE GENERATION:</strong><br>' + moment.image_gen_prompt;

        const why = document.createElement('div');
        why.className = 'paintable-section';
        why.innerHTML = '<strong>WHY PAINTABLE:</strong> ' + moment.why_paintable;

        div.appendChild(header);
        div.appendChild(composition);
        div.appendChild(color);
        div.appendChild(gesture);
        div.appendChild(paintingPrompt);
        div.appendChild(imagePrompt);
        div.appendChild(why);

        container.appendChild(div);
    });

    // Scroll to top
    container.scrollTop = 0;
}

