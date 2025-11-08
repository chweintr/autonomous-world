// Autonomous World Studio - Frontend

// Helpers
const $ = (s, el=document)=>el.querySelector(s);
const $$ = (s, el=document)=>[...el.querySelectorAll(s)];
const on = (el,ev,fn)=>el.addEventListener(ev,fn);

let characters = [];
let locations = [];

// Theme
const themeSel = $('#theme');
on(themeSel,'change',()=>{ 
  document.documentElement.setAttribute('data-theme', themeSel.value); 
  toast('Theme changed'); 
});

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  await loadCharacters();
  await loadLocations();
  setupCharacterPlacements();
  updateStatus();
  toast('Ready');
});

// Load characters
async function loadCharacters() {
  try {
    const response = await fetch('/api/characters');
    characters = await response.json();
  } catch (error) {
    console.error('Error loading characters:', error);
  }
}

// Load locations
async function loadLocations() {
  try {
    const response = await fetch('/api/locations');
    locations = await response.json();
  } catch (error) {
    console.error('Error loading locations:', error);
  }
}

// Setup character placement dropdowns
function setupCharacterPlacements() {
  const container = $('#character-placements');
  container.innerHTML = '';
  container.className = 'form';

  characters.forEach(char => {
    const label = document.createElement('label');
    label.textContent = char.name;
    label.htmlFor = `char-${char.id}`;

    const select = document.createElement('select');
    select.id = `char-${char.id}`;
    
    const noneOption = document.createElement('option');
    noneOption.value = '';
    noneOption.textContent = '— Not placed —';
    select.appendChild(noneOption);

    locations.forEach(loc => {
      const option = document.createElement('option');
      option.value = loc.id;
      option.textContent = loc.name;
      select.appendChild(option);
    });

    container.appendChild(label);
    container.appendChild(select);
  });
}

// Seed scenario
on($('#seed'),'click', async ()=>{
  const placements = {};
  characters.forEach(char => {
    const select = $(`#char-${char.id}`);
    if (select && select.value) {
      placements[char.id] = select.value;
    }
  });

  if (Object.keys(placements).length === 0) {
    toast('Place at least one character');
    return;
  }

  try {
    const config = {
      autonomy_level: parseFloat($('#autonomy')?.value || 0.75),
      randomness: parseFloat($('#randomness')?.value || 0.25),
      interaction_density: $('#density').value,
      time_compression: 60
    };

    const useLLM = $('#useLLM').checked;

    const response = await fetch('/api/scenario/seed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ placements, config, use_llm: useLLM })
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      updateStatus();
      toast('Scenario seeded - ready to run');
    }
  } catch (error) {
    console.error('Error:', error);
    toast('Error seeding scenario');
  }
});

// Run simulation
on($('#run'),'click', async ()=>{
  try {
    $('#statusVal').textContent='running';
    $('#fps').textContent = 'Simulating...';
    toast('Simulation started');

    const duration = parseInt($('#duration').value);
    
    const response = await fetch('/api/simulation/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ duration_minutes: duration })
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      displayInteractions(result.interactions);
      updateStatus();
      toast(`Complete: ${result.interactions_count} interactions`);
      $('#fps').textContent = 'Complete';
    }
  } catch (error) {
    console.error('Error:', error);
    toast('Error running simulation');
    $('#statusVal').textContent='error';
  }
});

// Display field notes
function displayInteractions(interactions) {
  const container = $('#notes');
  container.innerHTML = '';

  if (!interactions || interactions.length === 0) {
    container.innerHTML = '<li style="color: var(--muted); text-align: center; padding: 40px;">No interactions generated.</li>';
    return;
  }

  interactions.forEach(interaction => {
    const li = document.createElement('li');
    li.className = 'note';

    const time = new Date(interaction.timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });

    const tempClass = interaction.emotional_temperature || 'uncertain';

    li.innerHTML = `
      <div class="note-head">
        <div class="timestamp">${time}</div>
        <div class="pill">${interaction.location_name} · ${interaction.time_of_day}</div>
        ${interaction.is_unexpected ? '<div class="chip emergent">EMERGENT</div>' : ''}
      </div>
      <p class="note-body">${interaction.action_description}</p>
      <div class="aside">
        <span class="tag">Material details</span>
        <span class="muted">${interaction.material_details}</span>
      </div>
      <div class="temp-line ${tempClass}">
        <span>Emotional temperature:</span> <strong>${tempClass.charAt(0).toUpperCase() + tempClass.slice(1)}</strong>
      </div>
    `;

    container.appendChild(li);
  });
}

// Extract paintable moments
on($('#extractMoments'), 'click', async () => {
  try {
    const useLLM = $('#useLLM').checked;
    
    const response = await fetch('/api/paintable/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ top_n: 5, use_llm: useLLM })
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      displayPaintableMoments(result.moments);
      toast(`Extracted ${result.count} moments`);
    } else {
      toast('Error: ' + result.message);
    }
  } catch (error) {
    console.error('Error:', error);
    toast('Error extracting moments');
  }
});

// Display paintable moments
function displayPaintableMoments(moments) {
  const container = $('#paintableBody');
  container.innerHTML = '';

  if (!moments || moments.length === 0) {
    container.innerHTML = '<div style="color: var(--muted); text-align: center; padding: 20px;">No moments found.</div>';
    return;
  }

  moments.forEach((moment, index) => {
    const div = document.createElement('div');
    div.className = 'paintable-moment';

    const time = new Date(moment.timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });

    div.innerHTML = `
      <div class="paintable-header">Moment ${index + 1} [${time}] - ${moment.location}</div>
      
      <div class="paintable-section">
        <strong>COMPOSITION</strong>
        ${moment.composition}
      </div>
      
      <div class="paintable-section">
        <strong>COLOR</strong>
        ${moment.color_notes}
      </div>
      
      <div class="paintable-section">
        <strong>KEY GESTURE</strong>
        ${moment.gesture_notes}
      </div>
      
      <div class="paintable-prompt">
        <strong>FOR YOU (PAINTER)</strong><br>
        ${moment.painting_prompt}
      </div>
      
      <div class="paintable-prompt" style="border-left-color: var(--accent-3)">
        <strong>FOR IMAGE GENERATION</strong><br>
        ${moment.image_gen_prompt}
      </div>
      
      <div class="paintable-section">
        <strong>WHY PAINTABLE</strong>
        ${moment.why_paintable}
      </div>
    `;

    container.appendChild(div);
  });
}

// Generate emergence report
on($('#genReport'), 'click', async () => {
  try {
    const response = await fetch('/api/emergence/report');
    const result = await response.json();
    
    if (result.status === 'success') {
      $('#reportBody').innerHTML = `<pre>${result.report}</pre>`;
      toast('Report generated');
    } else {
      toast('Error: ' + result.message);
    }
  } catch (error) {
    console.error('Error:', error);
    toast('Run a simulation first');
  }
});

// Update status
async function updateStatus() {
  try {
    const response = await fetch('/api/simulation/status');
    const status = await response.json();
    
    if (status.status === 'no_simulation') {
      $('#statusVal').textContent = 'Not initialized';
      $('#interactionCount').textContent = '0';
      $('#charStates').innerHTML = '<li>Seed a scenario to begin</li>';
    } else {
      $('#statusVal').textContent = status.status;
      $('#interactionCount').textContent = status.interactions_count || 0;
      
      if (status.characters) {
        const statesList = $('#charStates');
        statesList.innerHTML = '';
        
        Object.entries(status.characters).forEach(([id, state]) => {
          const char = characters.find(c => c.id === id);
          if (char) {
            const locName = state.location ? 
              locations.find(l => l.id === state.location)?.name : 'None';
            const li = document.createElement('li');
            li.textContent = `${char.name}: ${state.emotional_state} at ${locName}`;
            statesList.appendChild(li);
          }
        });
      }
    }
  } catch (error) {
    console.error('Error updating status:', error);
  }
}

// Save session
on($('#save'), 'click', async () => {
  const name = prompt('Session name:', 'session_' + Date.now());
  if (!name) return;

  try {
    const response = await fetch('/api/session/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });

    const result = await response.json();
    if (result.status === 'success') {
      toast('Session saved');
    }
  } catch (error) {
    console.error('Error:', error);
    toast('Error saving session');
  }
});

// Reset
on($('#reset'), 'click', async () => {
  if (!confirm('Reset simulation?')) return;

  try {
    await fetch('/api/reset', { method: 'POST' });
    $('#notes').innerHTML = '<li style="color: var(--muted); text-align: center; padding: 40px;">Field notes will appear here...</li>';
    $('#reportBody').innerHTML = '<div style="color: var(--muted); text-align: center; padding: 20px;">Pattern analysis will appear here</div>';
    $('#paintableBody').innerHTML = '<div style="color: var(--muted); text-align: center; padding: 20px;">Click "Extract" after running simulation</div>';
    updateStatus();
    $('#statusVal').textContent = 'paused';
    $('#fps').textContent = 'Ready';
    toast('Reset complete');
  } catch (error) {
    console.error('Error:', error);
    toast('Error resetting');
  }
});

// Toast notification
let toastTm;
function toast(msg){
  const el=$('#toast');
  el.textContent=msg;
  el.classList.add('show');
  clearTimeout(toastTm);
  toastTm=setTimeout(()=>el.classList.remove('show'),2000);
}

// Update map view
async function updateMap() {
  try {
    const response = await fetch('/api/map/view');
    const result = await response.json();
    if (result.status === 'success') {
      displayMap(result.locations);
    }
  } catch (error) {
    // Silent fail - map is optional
  }
}

// Display map
function displayMap(locations) {
  const mapContainer = $('#map-view');
  if (!mapContainer) return;

  let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px;">';

  locations.forEach(loc => {
    const hasChars = loc.characters.length > 0;
    const bgColor = hasChars ? 'var(--card-bg)' : 'var(--bg-2)';

    html += `<div style="background: ${bgColor}; padding: 10px; border: 1px solid var(--border); border-radius: 4px;">`;
    html += `<strong style="font-size: 11px;">${loc.name}</strong><br>`;
    html += `<small style="color: var(--muted); font-size: 10px;">${loc.time_of_day} · ${loc.weather}</small>`;

    if (hasChars) {
      html += '<div style="margin-top: 6px;">';
      loc.characters.forEach(char => {
        html += `<div style="margin: 3px 0; padding: 4px; background: var(--bg-3); border-radius: 2px; font-size: 10px;">`;
        html += `<span style="color: var(--accent);">${char.name}</span><br>`;
        html += `<small style="color: var(--muted);">${char.emotional_state}</small>`;
        html += `</div>`;
      });
      html += '</div>';
    }

    html += '</div>';
  });

  html += '</div>';
  mapContainer.innerHTML = html;
}

// Export for Lora training
async function exportForLora() {
  try {
    const useLLM = $('#useLLM')?.checked || false;

    const response = await fetch('/api/paintable/export-lora', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ top_n: 5, use_llm: useLLM })
    });

    const result = await response.json();

    if (result.status === 'success') {
      const blob = new Blob([JSON.stringify(result.dataset, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `lora-dataset-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      toast(`Exported ${result.count} moments for Lora`);
    }
  } catch (error) {
    console.error('Error exporting for Lora:', error);
    toast('Run simulation first');
  }
}

// Update map every 3 seconds
setInterval(updateMap, 3000);

// Expose for custom events (Phase 2)
window.AgentWorldsUI = {
  collectScenario() {
    const placements = {};
    characters.forEach(char => {
      const select = $(`#char-${char.id}`);
      if (select && select.value) placements[char.id] = select.value;
    });
    return {
      placements,
      duration: parseInt($('#duration').value),
      density: $('#density').value,
      useLLM: $('#useLLM').checked
    };
  },
  applyPalette([accent='#ffd44d',accent2='#ff5c9a',accent3='#6dd6ff']){
    const r=document.documentElement.style; 
    r.setProperty('--accent',accent); 
    r.setProperty('--accent-2',accent2); 
    r.setProperty('--accent-3',accent3);
  }
};


