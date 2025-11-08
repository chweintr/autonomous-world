# Phase 2: Visual Integration (Next 3-6 Months)

## 🎨 Your Imagery → The System

This is where your existing visual work becomes part of the generative engine.

## 📁 Visual Reference Structure (Ready Now)

I've created this directory structure for your images:

```
visual_references/
├── characters/           ← Images that inform character appearance
├── locations/           ← Images that define spatial environments
├── atmosphere/          ← Light, color, mood references
└── reference_works/     ← Your existing paintings/images that inspire
```

### What to Put There

**`characters/`**
- Clothing patterns (leopard print, stripes, embroidery)
- Postures and gestures
- Color palettes for each character
- Animal references (horses, pigs, wolves, birds)
- Body language studies
- Your paintings of similar figures

**`locations/`**
- Desert spaces
- Courtyards and architectural fragments
- Fire/bonfire images
- Patterned walls/interiors
- Any existing work that shows these spaces

**`atmosphere/`**
- Dusk/dawn light studies
- Color relationships (pink sky, etc.)
- Dust, weather effects
- Shadows and light quality
- Your paintings with strong atmospheric qualities

**`reference_works/`**
- Finished paintings from this visual world
- Studies and sketches
- Any work that captures the tone/feeling
- Color studies
- Compositional references

## 🔄 Integration Roadmap

### Phase 2a: Visual Anchoring (Month 1-2)

**What we build:**

1. **Character Visual Profiles**
   ```python
   @dataclass
   class Character:
       ...
       visual_references: List[str]  # Paths to your images
       color_palette: List[str]      # Extracted colors
       style_notes: str              # Visual description
   ```

2. **Location Visual Database**
   - Link each location to your reference images
   - Extract dominant colors, lighting, spatial qualities
   - Use as input for image generation

3. **Image Analysis Pipeline**
   - Analyze your images for:
     - Color palettes
     - Composition patterns
     - Lighting qualities
     - Spatial arrangements
   - Feed these into generation prompts

**Technical needs:**
- Image processing libraries (PIL, OpenCV)
- Color extraction tools
- Optional: CLIP for semantic understanding

**Your role:**
- Organize existing images into folders
- Tag them with relevant characters/locations
- Note which pieces best capture the world

### Phase 2b: Image Generation (Month 2-4)

**Generate images from field notes using your visual language**

**Options (in order of sophistication):**

1. **Midjourney/DALL-E Integration**
   - Feed field notes + your reference images
   - Generate in your visual style
   - Quick but less control

2. **Stable Diffusion + LoRA Training**
   - Train on your existing work
   - Generate in your specific style
   - More control, more setup

3. **Stable Diffusion XL + ControlNet**
   - Use your compositions as structural guides
   - Apply your color palettes
   - Maintain your spatial sensibility
   - Most sophisticated

**Workflow:**
```
Field Note (text) 
  → Extract visual elements
  → Build prompt from your reference palette
  → Generate image
  → Refine with your aesthetic parameters
  → Present for your selection/editing
```

**Output:**
- Image per field note (optional, you choose which)
- Image sequences for key scenarios
- Visual reference library auto-generated
- Still requires your curation and finishing

### Phase 2c: Image-to-Image Workflows (Month 4-6)

**Your images influence future generations**

1. **Compositional Templates**
   - Your paintings become composition guides
   - System generates variations using same structure
   - Preserves your spatial language

2. **Color Transfer**
   - Extract palettes from your work
   - Apply to generated images
   - Maintains color consistency with your aesthetic

3. **Style Transfer**
   - Generate rough compositions
   - Apply your painterly style
   - Creates "sketches" in your visual language

**Example:**
```
Your painting of courtyard scene
  → Extract: composition, colors, light direction
  → New field note: different characters, same space
  → Generate: new image using your visual structure
  → Result: Feels like your work, new content
```

## 🛠️ Technical Implementation

### What We'll Add

**New Dependencies:**
```python
# Image processing
pillow==10.0.0
opencv-python==4.8.0
numpy==1.24.0

# AI/ML for generation
diffusers==0.21.0          # Stable Diffusion
transformers==4.33.0       # CLIP, other models
torch==2.0.0               # If using local generation

# Or API-based
replicate==0.11.0          # For Stable Diffusion API
openai>=1.0.0              # DALL-E 3 (already have)
```

**New Modules:**
```
src/
├── visual/
│   ├── image_analyzer.py      # Analyze your references
│   ├── palette_extractor.py   # Pull colors from images
│   ├── style_encoder.py       # Encode your visual style
│   └── generator.py           # Generate images from notes
└── models/
    └── visual_profile.py      # Extended character/location models
```

**Storage:**
```
data/
├── generated_images/          # System-generated visuals
│   ├── by_session/
│   ├── by_character/
│   └── by_location/
└── visual_references/         # Your source imagery (already created)
```

### Compute Considerations

**For Image Generation:**

**Option 1: Local (GPU Recommended)**
- **Need**: Mac with M1/M2/M3 (Metal support) OR NVIDIA GPU
- **Why**: Stable Diffusion runs locally
- **Cost**: $0 per image (after setup)
- **Speed**: 5-30 seconds per image
- **Control**: Maximum

**Option 2: Cloud APIs**
- **Need**: Just API keys
- **Services**: Replicate, Stability AI, Midjourney, DALL-E
- **Cost**: $0.01-$0.10 per image
- **Speed**: 10-60 seconds per image
- **Control**: Good

**Option 3: Cloud Compute (Railway, Modal, etc.)**
- **Need**: Deploy to GPU-enabled cloud
- **Cost**: ~$0.10-$0.50/hour GPU time
- **Speed**: Fast
- **Control**: Maximum
- **Benefit**: Can share via URL

**My Recommendation:**
- Start with **Option 2** (APIs) for Phase 2a/2b
- Move to **Option 3** (cloud GPU) for Phase 2c if you want to share/collaborate
- **Option 1** (local) if you have M1/M2/M3 Mac and want privacy

## 🎯 Phase 2 Milestones

### Milestone 1: Visual Reference System
**Timeline: Week 1-2**
- [ ] You organize existing images into folders
- [ ] System reads and catalogs them
- [ ] Extracts color palettes, tags, metadata
- [ ] Links to characters/locations
**Output**: Visual database of your aesthetic

### Milestone 2: Reference-Informed Prompts
**Timeline: Week 3-4**
- [ ] Field notes now include visual references
- [ ] Prompts built from your color palettes
- [ ] Character descriptions match your images
**Output**: Enhanced text descriptions tied to visuals

### Milestone 3: First Image Generation
**Timeline: Week 5-8**
- [ ] Connect to image generation API
- [ ] Generate single images from field notes
- [ ] Manual selection/curation by you
**Output**: First generated images in your style

### Milestone 4: Batch Generation
**Timeline: Week 9-12**
- [ ] Generate images for full sessions
- [ ] Automatic style application
- [ ] Image sequences for scenarios
**Output**: Visual narratives, not just text

### Milestone 5: Image-to-Image Pipeline
**Timeline: Week 13-20**
- [ ] Your paintings guide new generations
- [ ] Compositional templates active
- [ ] Style transfer working
**Output**: System generates in your visual language

### Milestone 6: Feedback Loop
**Timeline: Week 21-24**
- [ ] Generated images become references
- [ ] System learns from your selections
- [ ] Palette evolves with new work
**Output**: Self-improving visual engine

## 💰 Cost Estimates (Phase 2)

### Development Time
- Your time organizing references: 4-8 hours
- My time building integration: Included (we're doing this together)
- Testing and refinement: Ongoing

### Running Costs

**API-Based Generation:**
- Stable Diffusion (Replicate): $0.01/image
- DALL-E 3: $0.04-$0.08/image
- Midjourney: ~$30/month unlimited
- 60-min simulation (12 images): $0.12-$1.00

**Cloud GPU (if needed later):**
- Modal/Railway GPU: $0.10-$0.50/hour
- Only when generating, not when simulating

**Storage:**
- Local: Free (your disk)
- Cloud (if deploying): ~$5/month for images

## 🎨 What You Get (Phase 2 Complete)

### Before (Phase 1):
```
[18:47 - Courtyard - Dusk]
Text description of Marcus and Redline...
```

### After (Phase 2):
```
[18:47 - Courtyard - Dusk]
Text description of Marcus and Redline...

[GENERATED IMAGE]
- Uses YOUR leopard print pattern
- YOUR courtyard spatial arrangement  
- YOUR dusk color palette
- YOUR gestural style
- Specific to THIS moment
```

### The Workflow Becomes:

1. Run simulation (text)
2. System generates images automatically
3. You review/select/curate
4. Use as:
   - Direct reference for paintings
   - Compositional studies
   - Color/light studies
   - Sequence/narrative planning
   - Source for further refinement

## 🚀 Getting Started (Phase 2)

### Step 1: Organize Your Images (This Week)

Put your existing work in:
```
visual_references/
├── characters/
│   ├── rider_leopard_jacket_01.jpg
│   ├── handler_with_pigs_02.jpg
│   └── animal_studies/
├── locations/
│   ├── courtyard_dusk_series/
│   ├── desert_clearing/
│   └── bonfire_studies/
├── atmosphere/
│   ├── pink_dusk_skies/
│   ├── dust_and_light/
│   └── shadow_patterns/
└── reference_works/
    ├── completed_paintings/
    └── color_studies/
```

**Naming doesn't matter** - just organize by theme.

### Step 2: Tag Key Pieces (Optional)

Create `visual_references/index.md`:
```markdown
## Character References

### The Rider
- `characters/rider_01.jpg` - Leopard print jacket, posture
- `characters/rider_horse_02.jpg` - Relationship with Redline

### The Handler  
- `characters/handler_pigs_01.jpg` - Embroidered vest, pigs circling
...

## Locations

### Courtyard
- `locations/courtyard_01.jpg` - Best captures the space
- `locations/courtyard_dusk.jpg` - Perfect light
...
```

### Step 3: I Build the Integration

Once you have references organized, I'll:
1. Build image analysis pipeline
2. Extract your visual language (colors, compositions)
3. Integrate with field note generation
4. Add image generation capability
5. Test with your references

### Step 4: First Generations

We run a scenario and generate images using your visual vocabulary.

## 📋 What I Need from You

### To Start Phase 2:

1. **Your existing images** organized in `visual_references/`
   - 10-50 images is plenty to start
   - More is better but not required
   - Quality > quantity

2. **Notes on key pieces** (optional but helpful)
   - Which images best capture each character?
   - Which show the spaces most accurately?
   - Which have the color/light you want?

3. **Your visual priorities**
   - Color palette most important?
   - Composition/spatial arrangement?
   - Gestural quality?
   - Light/atmosphere?

4. **Image generation preference**
   - API-based (easier, costs $)
   - Local (M1 Mac can do this)
   - Cloud GPU (more powerful, shareable)

### Timeline

**You decide** - we can start Phase 2:
- After you've used Phase 1 for a while (recommended)
- Immediately (if you have references ready)
- Whenever you're ready

## 🔗 Links to Future Phases

**Phase 2 → Phase 3:**
- Images become video sequences
- Characters move through space
- Animation from your visual style

**Phase 2 → Phase 4:**
- Images define 3D spaces
- Your visual language in spatial computing
- Real-time world building

**All rooted in your imagery.**

---

**Next: See FUTURE_ROADMAP.md for the complete vision**


