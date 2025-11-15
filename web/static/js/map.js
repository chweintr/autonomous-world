// Diorama Map View JavaScript

let locations = [];
let characters = [];
let currentLocationIndex = 0;
let autoScrollEnabled = false;
let updateInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    showLoading();
    await loadData();
    renderDiorama();
    startAutoUpdate();
    hideLoading();
});

function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading-indicator';
    loading.id = 'loading';
    loading.textContent = 'LOADING WORLD...';
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.remove();
}

// Load data from API
async function loadData() {
    try {
        // Load locations and their current state
        const mapResponse = await fetch('/api/map/view');
        const mapData = await mapResponse.json();

        if (mapData.status === 'success') {
            locations = mapData.locations;
        }

        // Update current time
        updateTimeDisplay();
    } catch (error) {
        console.error('Error loading map data:', error);
    }
}

// Render the diorama
function renderDiorama() {
    const container = document.getElementById('stage-container');
    container.innerHTML = '';

    locations.forEach((location, index) => {
        const stageSet = createStageSet(location, index);
        container.appendChild(stageSet);
    });
}

// Create a stage set for a location
function createStageSet(location, index) {
    const set = document.createElement('div');
    set.className = 'stage-set';
    set.id = `stage-${index}`;
    set.dataset.location = location.id;

    // Backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'stage-backdrop';
    set.appendChild(backdrop);

    // Wetness overlay
    const wetness = document.createElement('div');
    wetness.className = 'wetness-overlay';
    set.appendChild(wetness);

    // Reflection effect
    const reflection = document.createElement('div');
    reflection.className = 'reflection';
    set.appendChild(reflection);

    // Location label
    const label = document.createElement('div');
    label.className = 'location-label';
    label.innerHTML = `
        <h3>${location.name}</h3>
        <div class="location-meta">${location.time_of_day} · ${location.weather}</div>
    `;
    set.appendChild(label);

    // Neon sign decoration (random for some locations)
    if (Math.random() > 0.5) {
        const neon = document.createElement('div');
        neon.className = 'neon-sign';
        neon.textContent = getNeonSymbol(location.id);
        set.appendChild(neon);
    }

    // Characters present
    location.characters.forEach((char, charIndex) => {
        const figure = createCharacterFigure(char, charIndex);
        set.appendChild(figure);
    });

    // Click handler
    set.addEventListener('click', () => {
        scrollToLocationIndex(index);
    });

    return set;
}

// Get neon sign symbol based on location
function getNeonSymbol(locationId) {
    const symbols = {
        'loc_courtyard': '◆',
        'loc_bonfire': '◈',
        'loc_patterned': '◉',
        'loc_parade': '◊',
        'loc_stable': '⬡',
        'loc_desert': '✦',
        'loc_rooftop': '▲',
        'loc_crossroads': '✕',
        'loc_water': '≋',
        'loc_canyon': '◢',
        'loc_workshop': '⚙',
        'loc_burial': '✝'
    };
    return symbols[locationId] || '◆';
}

// Create character figure
function createCharacterFigure(character, index) {
    const figure = document.createElement('div');
    figure.className = 'character-figure';
    figure.dataset.emotion = character.emotional_state.toLowerCase();

    // Position characters horizontally across the stage
    const positions = [100, 200, 300, 380];
    figure.style.left = `${positions[index % positions.length]}px`;

    // Character body
    const body = document.createElement('div');
    body.className = 'character-body';
    figure.appendChild(body);

    // Character name
    const name = document.createElement('div');
    name.className = 'character-name';
    name.textContent = character.name.split(' ')[0]; // First name only
    figure.appendChild(name);

    // Animal companion
    if (character.animal) {
        const animal = document.createElement('div');
        animal.className = 'animal-companion';
        animal.title = character.animal;
        figure.appendChild(animal);
    }

    // Click handler to show details
    figure.addEventListener('click', (e) => {
        e.stopPropagation();
        showCharacterDetails(character);
    });

    return figure;
}

// Show character details overlay
function showCharacterDetails(character) {
    const overlay = document.getElementById('character-overlay');
    const content = document.getElementById('overlay-content');

    content.innerHTML = `
        <button class="overlay-close" onclick="closeOverlay()">✕</button>
        <h2 style="color: #4ECDC4; margin-bottom: 20px;">${character.name}</h2>
        <div style="margin-bottom: 15px;">
            <strong style="color: #FFE66D;">Emotional State:</strong>
            <span style="color: #FF69B4;">${character.emotional_state}</span>
        </div>
        <div style="margin-bottom: 15px;">
            <strong style="color: #FFE66D;">Animal Companion:</strong>
            <span>${character.animal}</span>
        </div>
        <div style="margin-bottom: 15px;">
            <strong style="color: #FFE66D;">Current Location:</strong>
            <span>${character.location || 'Unknown'}</span>
        </div>
    `;

    overlay.classList.add('active');
}

function closeOverlay() {
    const overlay = document.getElementById('character-overlay');
    overlay.classList.remove('active');
}

// Scroll to specific location
function scrollToLocation(direction) {
    if (direction === 'next') {
        currentLocationIndex = Math.min(currentLocationIndex + 1, locations.length - 1);
    } else if (direction === 'prev') {
        currentLocationIndex = Math.max(currentLocationIndex - 1, 0);
    }

    scrollToLocationIndex(currentLocationIndex);
}

function scrollToLocationIndex(index) {
    currentLocationIndex = index;
    const stage = document.getElementById(`stage-${index}`);
    if (stage) {
        stage.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'center' });

        // Highlight active stage
        document.querySelectorAll('.stage-set').forEach(s => s.classList.remove('active'));
        stage.classList.add('active');
    }
}

// Toggle auto-scroll to follow characters
function toggleAutoScroll() {
    autoScrollEnabled = document.getElementById('auto-scroll').checked;

    if (autoScrollEnabled) {
        followCharacters();
    }
}

// Follow characters automatically
function followCharacters() {
    if (!autoScrollEnabled) return;

    // Find location with most characters
    let maxChars = 0;
    let targetIndex = 0;

    locations.forEach((loc, index) => {
        if (loc.characters.length > maxChars) {
            maxChars = loc.characters.length;
            targetIndex = index;
        }
    });

    if (maxChars > 0) {
        scrollToLocationIndex(targetIndex);
    }
}

// Update time display
function updateTimeDisplay() {
    const timeDisplay = document.getElementById('current-time');
    const now = new Date();
    timeDisplay.textContent = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Start auto-update loop
function startAutoUpdate() {
    // Update every 5 seconds
    updateInterval = setInterval(async () => {
        await loadData();
        renderDiorama();
        updateTimeDisplay();

        if (autoScrollEnabled) {
            followCharacters();
        }
    }, 5000);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});

// Click outside overlay to close
document.addEventListener('click', (e) => {
    const overlay = document.getElementById('character-overlay');
    if (e.target === overlay) {
        closeOverlay();
    }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        scrollToLocation('prev');
    } else if (e.key === 'ArrowRight') {
        scrollToLocation('next');
    } else if (e.key === 'Escape') {
        closeOverlay();
    }
});
