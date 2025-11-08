# Technical Roadmap - From Text to Spatial Computing

**Based on GPT design advice + our Phase planning**

## 🎯 Current State (Phase 1) ✅

**What we have:**
- Autonomous character system
- Field note generation
- LLM integration
- Paintable moments extractor ⭐ NEW
- Web interface
- 10 weird characters
- Emergence tracking

**Foundation is solid. Now we build on it.**

---

## 📹 Phase 2a: Video/Image Path (Next 3 Months)

### 1. Strengthen World State Model

**Current:** JSON files, session-based  
**Upgrade to:**

```json
// Shot metadata format
{
  "shot_id": "shot_001_measurer_collector_burial",
  "timestamp": "18:47",
  "location": "burial_ground",
  "characters": ["measurer", "collector"],
  "focal_length": 50,
  "camera_move": "static" | "slow_push" | "dolly_left",
  "palette_bias": {
    "primary": "pink",
    "secondary": "aqua", 
    "accent": "yellow"
  },
  "char_refs": {
    "measurer": ["visual_references/characters/measurer_01.jpg"],
    "collector": ["visual_references/characters/collector_02.jpg"]
  },
  "negative_list": ["desert tones", "brown", "realistic lighting"],
  "field_note": "...",
  "paintable_score": 8.5
}
```

### 2. Image Generation with Continuity

**Character Reference Boards:**
- Lock colors per character (Measurer = aqua blazer, pink stripes)
- Lock silhouette/appearance
- Reference images in `visual_references/characters/`

**Process:**
```
Field Note 
  → Extract composition/colors/gesture
  → Pull character reference images
  → Generate with locked styling
  → Reuse seed for same character (consistency)
  → Use last frame as guidance for next frame
```

**Tech Stack:**
- ComfyUI or Automatic1111 (local Stable Diffusion)
- OR Replicate API (cloud)
- ControlNet for composition guidance
- LoRA trained on your work (optional)

### 3. Video Compilation

**Frame-to-Video:**
- Generate key frames (2-5 per interaction)
- Interpolate with: Runway Gen-3, Pika, or (when available) Sora
- "Cut on action" - compile shots based on field note sequence

**Output:**
```
Session_courtyard_20250104/
├── shots/
│   ├── shot_001.mp4 (2-5 seconds)
│   ├── shot_002.mp4
│   └── shot_003.mp4
├── compiled.mp4 (all shots)
├── trim_sheet.json (EDL-like)
└── field_notes.srt (captions)
```

### 4. Sound + Captions

**Auto-generate:**
- Field notes → SRT captions
- Sparse Foley: wind, fabric, footsteps, motorcycle hum
- Ambient track (Hermanos Gutiérrez vibe)

**Why:** Sells realism, prepares for MR later

---

## 🌐 Phase 2b: Interactive 2.5D Web (6 Months)

### Tech: Three.js + WebGPU

**What it enables:**
- Depth-from-image parallax
- Camera slides through 2.5D space
- WebXR toggle for headset passthrough
- Same assets, MR-ready

**Architecture:**
```
Director Agent (Python) ↔ WebSocket ↔ Three.js Viewer (Browser)
    ↓                                        ↓
World State JSON                    Composited Layers
    ↓                                        ↓
Character updates                    Real-time visual updates
```

**User Experience:**
- View simulation in browser
- Subtle camera movement (parallax depth)
- Toggle WebXR → same scene in headset passthrough
- State updates in real-time

**Implementation:**
- Depth maps from generated images
- Layer system (background, mid, foreground)
- Smooth camera interpolation
- WebXR API integration

---

## 🎮 Phase 3: Full 3D Pipeline (12 Months)

### Engine Choice

**Option A: Unreal 5**
- ✅ Highest fidelity
- ✅ Path-tracing (beautiful lighting)
- ✅ Niagara (particle systems, birds flocking)
- ✅ PCG (procedural generation)
- ❌ Heavier, steeper learning curve

**Option B: Unity**
- ✅ Faster MR deployment
- ✅ Bigger plugin ecosystem
- ✅ Easier integration
- ❌ Slightly less visual fidelity

**Recommendation:** Unity for Phase 3, migrate to Unreal for Phase 4 if needed.

### Asset Flow

**Library Structure:**
```
assets/
├── characters/
│   ├── measurer.usd / .gltf
│   ├── collector.usd
│   └── ...
├── motifs/
│   ├── embroidery_patterns/
│   ├── quilts/
│   ├── glyphs/
│   └── gloves/
├── colors/
│   ├── palette_pink_aqua.lut
│   ├── citrine_accent.lut
│   └── ...
└── environments/
    ├── courtyard.usd
    ├── burial_ground.usd
    └── ...
```

**Format:** USD or GLTF (universal, MR-compatible)

**Post-Processing Stack:**
- Bloom threshold (glow on aqua/pink)
- Film grain (texture)
- LUT (lock color palette)
- Slight stylization (painterly read, not photorealistic)

### Runtime Control: "Conductor" Plugin

**Thin layer that:**
```python
# Your Python world state
world_state.json
    ↓
# Conductor reads and spawns
{
  "characters": [...],
  "interactions": [...]
}
    ↓
# Unreal/Unity receives
- Spawn character actors
- Trigger animation clips
- Set lighting
- Apply post settings
- Update flocking (birds)
- Cloth simulation (ribbons, fabric)
```

**Director pushes beats → Engine responds**

---

## 🥽 Phase 4: MR Integration (18 Months)

### Platform Support

**Vision Pro / Quest / WebXR:**
- Shared USD/GLTF assets
- Simple shaders (cross-platform)
- World JSON drives all platforms

**Implementation:**
```
World State (JSON)
    ↓
Compile to → Unity/Unreal/WebXR
    ↓
Deploy to → Vision Pro, Quest, Web
```

### Spatial Anchors

**Example:**
- Burial Ground → Maps to your studio corner
- Courtyard → Maps to floor space
- Characters appear in real space
- Fade fog based on room size
- Light estimation affects rendering

**User Experience:**
- Put on headset
- See Measurer in your studio
- Walk around him
- He's measuring the distance to your wall
- Pig at his feet
- You observe, capture angles for painting

---

## 🎨 Phase 5: Studio Polish Tools

### 1. Shot Board (Priority)

**Grid view of all generated frames:**
```
[Frame 1] [Frame 2] [Frame 3]
[Frame 4] [Frame 5] [Frame 6]
```

**Features:**
- Drag to reorder
- Click to enlarge
- Export EDL (edit decision list)
- Generates compiled video

### 2. Style Dials

**Three sliders:**
- **Palette Weight:** How much to push pink/aqua/yellow
- **Noise/Grain:** Film grain amount
- **Gloss:** Matte to glossy (post-processing)

**Maps to:**
- Generator parameters (image gen)
- Engine post stack (3D)
- Unified control

### 3. State Graph

**Visual graph:**
```
[Measurer] ←→ [Burial Ground] ←→ [Measuring tape]
     ↓              ↓                    ↓
  [Field Notes] [Shots]            [Props]
```

**Features:**
- Click character → filter notes/shots
- Click location → see all moments there
- Click prop → see all uses
- Visual navigation of content

---

## 🔄 Integration Phases

### **Now → 3 Months:**
1. ✅ Keep current system (foundation)
2. Add shot metadata to interactions
3. Build character reference board system
4. Integrate first image generator (Replicate/ComfyUI)
5. Generate single images with continuity
6. Build shot board UI

### **3 → 6 Months:**
7. Frame-to-video (Runway/Pika)
8. Auto-caption to SRT
9. Basic Foley
10. EDL export
11. Compiled video output
12. Three.js 2.5D viewer

### **6 → 12 Months:**
13. WebXR mode
14. Depth map generation
15. Unity/Unreal integration begins
16. "Conductor" plugin
17. Character USD/GLTF models
18. Flocking, cloth, particles

### **12 → 18 Months:**
19. Full 3D real-time
20. MR deployment (Vision Pro/Quest)
21. Spatial anchors
22. Room-scale observation
23. Style dials active across stack

### **18+ Months:**
24. Google Genie integration (when available)
25. Persistent world mode
26. Multi-user observation
27. Full autonomous spatial computing

---

## 💾 Data Format Evolution

### Current (Phase 1):
```python
Interaction → Field Note (text)
```

### Phase 2a:
```python
Interaction → Field Note + Shot Metadata + Paintable Prompt
```

### Phase 2b:
```python
Shot Metadata → Generated Image → Video Clip
```

### Phase 3:
```python
World State JSON → 3D Scene (Unity/Unreal)
```

### Phase 4:
```python
World State JSON → MR Experience (Vision Pro/Quest/WebXR)
```

**Same source data, multiple output formats.**

---

## 🛠️ Technical Stack (Full Vision)

### Phase 1 (Current):
- Python + Flask
- OpenAI API
- JSON data
- Web interface

### Phase 2a (Image):
- + Stable Diffusion (ComfyUI/Automatic1111/Replicate)
- + ControlNet
- + Optional LoRA (trained on your work)
- + PIL/OpenCV (image processing)

### Phase 2b (Video):
- + Runway Gen-3 / Pika / Sora
- + ffmpeg (compilation)
- + SRT generation
- + Basic audio (Foley)

### Phase 3 (3D):
- + Unity OR Unreal 5
- + USD/GLTF pipeline
- + Post-processing stack
- + "Conductor" plugin (Python → Engine)

### Phase 4 (MR):
- + WebXR API
- + Three.js + WebGPU
- + Vision Pro SDK / Quest SDK
- + Spatial anchors

### Phase 5 (Genie):
- + Google Genie (or equivalent)
- + Persistent world hosting
- + Multi-user sync

---

## 📋 Immediate Next Steps (Phase 2a Start)

### 1. Shot Metadata System
Add to each interaction:
```python
shot_id: str
camera_angle: str  # "medium_shot", "close_up", "wide"
focal_length: int  # 35, 50, 85mm
palette_bias: Dict[str, str]  # {"primary": "pink", ...}
character_references: List[str]  # paths to ref images
```

### 2. Character Reference System
```
visual_references/
└── characters/
    ├── measurer/
    │   ├── canonical_01.jpg (primary reference)
    │   ├── color_palette.json
    │   ├── embroidery_pattern.jpg
    │   └── silhouette_mask.png
    └── collector/
        └── ...
```

### 3. Shot Board UI Component
- Grid display of generated images
- Drag to reorder
- Click "Export EDL"
- Generates trim sheet JSON

### 4. Image Generator Integration
- Connect to Replicate OR local ComfyUI
- Use character references
- Lock colors per character
- Generate consistent look

### 5. Style Controls
- Palette weight slider
- Noise/grain slider  
- Gloss slider
- Maps to generator params

---

## 🎨 What Stays from Current Build

**Everything we built is the foundation:**

✅ **Autonomous character system** → Drives everything  
✅ **Field notes** → Source for all generation  
✅ **Paintable moments** → Shot selection  
✅ **Character profiles** → Reference for visuals  
✅ **LLM integration** → Descriptions + prompt extraction  
✅ **Web interface** → Evolves into shot board  
✅ **Emergence tracking** → Pattern-based shot selection

**We don't throw anything away - we ADD layers on top.**

---

## 📐 Architecture (Evolved)

### Current:
```
Characters → Decisions → Field Notes → Display
```

### Phase 2a:
```
Characters → Decisions → Field Notes → Paintable Moments
                              ↓              ↓
                         Shot Metadata  → Image Gen
                                            ↓
                                        Shot Board
```

### Phase 2b:
```
Shot Board → EDL → Video Compilation
              ↓
            SRT Captions + Foley
```

### Phase 3:
```
World State JSON → Conductor → Unity/Unreal
                                    ↓
                            Real-time 3D Scene
```

### Phase 4:
```
World State JSON → WebXR / Vision Pro / Quest
                         ↓
                   MR Experience
```

---

## 🎬 Shot Board Design (Priority Next)

### UI Layout:
```
┌─────────────────────────────────────────┐
│ Shot Board                               │
├─────────────────────────────────────────┤
│ [Filter: All | Charged | Emergent]      │
│ [Sort: Time | Score | Location]         │
├─────────────────────────────────────────┤
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐    │
│ │Img1│ │Img2│ │Img3│ │Img4│ │Img5│    │
│ │8.5 │ │7.2 │ │9.1 │ │6.8 │ │8.0 │    │
│ └────┘ └────┘ └────┘ └────┘ └────┘    │
│  [metadata]  [metadata]  ...            │
│                                          │
│ [Drag to reorder]                       │
│ [Export EDL] [Generate Video]           │
└─────────────────────────────────────────┘
```

**Features:**
- Grid of generated images
- Paintability score shown
- Drag-drop reordering
- Click → Show full prompt/metadata
- Export EDL JSON
- Generate compiled video

### EDL Format:
```json
{
  "project": "session_courtyard_001",
  "shots": [
    {
      "shot_id": "shot_001",
      "in_frame": 0,
      "out_frame": 120,
      "duration_sec": 5.0,
      "image_path": "shots/shot_001.png",
      "field_note": "...",
      "transition": "cut"
    },
    ...
  ],
  "audio": {
    "foley": ["wind", "fabric_rustle", "footsteps"],
    "ambient": "hermanos_gutierrez_vibe.mp3",
    "captions": "field_notes.srt"
  }
}
```

---

## 🎨 Style Dials (Unified Control)

### Three Master Controls:

**1. Palette Weight (0-100%)**
- 0% = Original colors from generation
- 100% = Force pink/aqua/yellow/green palette
- Maps to: Image gen "guidance scale" + 3D engine LUT

**2. Noise/Grain (0-100%)**
- 0% = Clean digital
- 100% = Heavy film grain
- Maps to: Image gen "noise" param + 3D post-process grain

**3. Gloss (0-100%)**
- 0% = Matte, flat
- 100% = Glossy, reflective
- Maps to: Material roughness in 3D + image gen style

**Saved per session** → Consistent look across all outputs

---

## 🗺️ State Graph (Visual Navigation)

### Graph View:
```
    [Measurer] ─── talks to ─── [Collector]
        │                           │
    located at                  located at
        │                           │
    [Burial Ground]           [Burial Ground]
        │                           │
    contains                    contains
        │                           │
    [Tombstones] ────────────── [Fallen Words]
```

**Click Measurer:**
- Filters to all his field notes
- Shows all his shots
- Highlights his locations
- Lists his props

**Click Burial Ground:**
- All moments there
- All characters who've visited
- Emotional temperature history
- Generated shots of that location

**Visual navigation** instead of scrolling text.

---

## 🔌 API Extensions Needed

### New Endpoints:

```python
POST /api/shots/generate
# Generate images for selected field notes
{
  "interaction_ids": [...],
  "use_character_refs": true,
  "palette_bias": "pink_aqua",
  "style": "cinematic_editorial"
}

GET /api/shots/list
# List all generated shots

POST /api/shots/reorder
# Reorder shots, update EDL

POST /api/video/compile
# Compile shots into video with EDL

POST /api/video/add_audio
# Add captions + Foley

GET /api/graph/state
# Get state graph data for visualization
```

---

## 💡 Implementation Priority

### **Immediate (This Month):**
1. ✅ Paintable moments extractor (DONE!)
2. Shot metadata schema
3. Character reference board system
4. First image generation integration

### **Next 3 Months:**
5. Shot board UI
6. EDL export
7. Image generation with continuity
8. Video compilation (ffmpeg)
9. SRT caption generation

### **6 Months:**
10. Three.js 2.5D viewer
11. WebXR toggle
12. State graph visualization

### **12 Months:**
13. Unity integration
14. Conductor plugin
15. Real-time 3D

### **18+ Months:**
16. MR deployment
17. Google Genie when available

---

## 🎯 What to Build Next

**You decide:**

**A) Image Generation First**
- Connect Stable Diffusion / Replicate
- Character reference boards
- Generate images from field notes
- Visual continuity system

**B) Shot Board First**
- Even without generated images
- Organize field notes visually
- EDL export
- Prepares for when images come

**C) Three.js 2.5D**
- Skip single images
- Go straight to interactive viewer
- Use your paintings as placeholder frames

**D) Keep Testing Phase 1**
- Use text system more
- Build up field notes library
- Images later

---

## 📦 Data Persistence

### Current: Files
```
data/sessions/*.md
```

### Phase 2+: Database
```
SQLite or PostgreSQL:
- interactions
- shots
- generated_images
- edls
- character_refs
- palette_configs
```

**Query capabilities:**
- "All charged moments at Burial Ground"
- "Every time Measurer + Collector interact"
- "Shots with pink+aqua palette"

---

## 🚀 My Recommendation

**Incremental build:**

1. **This week:** Keep testing Phase 1, get comfortable
2. **Next week:** Add shot metadata schema
3. **Week 3:** Connect to Replicate API (easiest image gen)
4. **Week 4:** Build shot board UI
5. **Month 2:** Video compilation
6. **Month 3:** Three.js viewer

**By Month 3** you'd have:
- Autonomous characters ✓
- Field notes ✓
- Generated images ✓
- Video compilation ✓
- Interactive 2.5D web view ✓

**Solid foundation for MR/3D later.**

---

**Want me to start on shot metadata + character reference system next? Or keep refining Phase 1?**

The roadmap is clear. We build incrementally. Nothing is "too crazy" - it's all achievable! 🎬✨


