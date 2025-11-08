# Quick Start Guide

Get the Autonomous World System running in 5 minutes.

## Installation

```bash
# 1. Navigate to the directory
cd autonomous-world

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the system
python run.py
```

## First Scenario

1. Open browser to `http://localhost:5000`

2. In the Control Panel, place characters:
   - Marcus Vale (The Rider) → The Courtyard
   - Iris Kahn (The Handler) → Stable Ruin

3. Set parameters:
   - Duration: 60 minutes
   - Keep other settings at defaults

4. Click **"Seed Scenario"**

5. Click **"Run Simulation"**

6. Watch field notes appear in the right panel

7. Click **"Generate Report"** to see patterns

8. Click **"Save Session"** to export as markdown

## What You'll See

Field notes like:

```
[14:23 - The Courtyard - Afternoon]
Marcus approaches Redline. His hands grip the reins too tight. 
The horse's ears flatten. In the distance, three pigs appear 
at the courtyard entrance, then retreat.

Material details: Leopard print jacket against chestnut coat. 
White rope coiled near the archway. Harsh afternoon shadows.

Emotional temperature: Tense
```

## Next Steps

- Read [USAGE_GUIDE.md](USAGE_GUIDE.md) for scenario design tips
- Read [README.md](README.md) for full documentation
- Experiment with different character combinations
- Try longer durations (120+ minutes) to see patterns emerge

## Optional: Enable LLM

For higher-quality descriptions:

```bash
# Install OpenAI package
pip install openai

# Set API key
export OPENAI_API_KEY="your-key-here"
```

Then check "Use LLM" in the web interface.

## Troubleshooting

**"ModuleNotFoundError: No module named 'flask'"**
- Run: `pip install -r requirements.txt`

**Web interface not loading**
- Check console for errors
- Ensure nothing else is using port 5000
- Try: `http://127.0.0.1:5000` instead of localhost

**No interactions generated**
- Make sure you clicked "Seed Scenario" first
- Check that characters are placed in locations
- Try increasing duration to 90 minutes

---

**You're ready!** The system is designed to be explored. Run scenarios, read field notes, discover patterns.


