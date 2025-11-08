# LLM Integration Setup Guide

LLM integration enables high-quality, vivid field note descriptions using AI models like GPT-4 or Claude.

## Quick Setup (Recommended)

Run the automated setup script:

```bash
cd autonomous-world
chmod +x setup_llm.sh
./setup_llm.sh
```

This will:
- Install required packages
- Help you set your API key
- Test the connection
- Confirm configuration

## Manual Setup

### Step 1: Install OpenAI Package

```bash
pip install openai==1.3.0
```

Or for Claude:
```bash
pip install anthropic
```

### Step 2: Get API Key

**For OpenAI (GPT-4)**:
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-`)

**For Anthropic (Claude)**:
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Create an API key

### Step 3: Set API Key

**Option A: Environment Variable (Recommended)**

Add to your shell profile:

```bash
# For zsh (macOS default)
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Option B: .env File**

1. Copy the example:
```bash
cp .env.example .env
```

2. Edit `.env` and add your key:
```
OPENAI_API_KEY=sk-your-key-here
```

**Option C: Session Only (Temporary)**

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

This only lasts until you close the terminal.

### Step 4: Enable in Configuration

The config is already set to enabled. To verify:

```bash
grep "enabled" config/default_config.json
```

Should show: `"enabled": true`

If it shows `false`, edit `config/default_config.json`:

```json
"llm": {
  "enabled": true,
  ...
}
```

### Step 5: Test It

Run the example:

```bash
python example_scenario.py
```

Or start the web interface:

```bash
python run.py
```

Then check "Use LLM" in the web interface.

## Configuration Options

Edit `config/default_config.json`:

```json
"llm": {
  "enabled": true,           // Turn LLM on/off
  "provider": "openai",      // "openai", "anthropic", or "ollama"
  "model": "gpt-4",          // Model to use
  "temperature": 0.8,        // Creativity (0.0-1.0)
  "max_tokens": 300          // Response length
}
```

### Available Models

**OpenAI**:
- `gpt-4` - Best quality, slower, more expensive
- `gpt-4-turbo` - Faster GPT-4
- `gpt-3.5-turbo` - Faster, cheaper, less quality

**Anthropic**:
- `claude-3-opus-20240229` - Best quality
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fastest, cheapest

### Temperature Settings

- **0.6-0.7**: More consistent, predictable descriptions
- **0.8**: Default - balanced creativity
- **0.9-1.0**: More varied, creative, sometimes unexpected

## Cost Considerations

### OpenAI Pricing (approximate)

**GPT-4**:
- ~$0.03 per 1K input tokens
- ~$0.06 per 1K output tokens
- A 60-minute simulation (12 interactions) ≈ $0.50-$1.00

**GPT-3.5-Turbo**:
- ~$0.0015 per 1K input tokens
- ~$0.002 per 1K output tokens
- A 60-minute simulation ≈ $0.05-$0.10

### Cost-Saving Tips

1. **Use templates for exploration**: Disable LLM while testing scenarios
2. **Enable for production runs**: Only use LLM for final sessions you'll use
3. **Try GPT-3.5**: 90% of the quality at 5% of the cost
4. **Batch similar scenarios**: Get more value from API calls

## Using Without LLM

If you prefer not to use LLM (to save costs or work offline):

1. **Disable in config**:
```json
"enabled": false
```

2. **Or uncheck "Use LLM"** in the web interface

The system will use template-based generation:
- Still creates valid field notes
- Faster and free
- Less specific and varied
- Good for exploration and testing

## Troubleshooting

### "No module named 'openai'"

```bash
pip install openai==1.3.0
```

### "Incorrect API key"

Check that your key is set correctly:

```bash
echo $OPENAI_API_KEY
```

Should show your key (starting with `sk-`).

### "LLM generation failed: ..."

The system automatically falls back to templates if LLM fails. Check:

1. API key is valid and has credits
2. Internet connection is working
3. Model name is correct in config
4. Check console for detailed error message

### Rate Limits

If you hit rate limits:

1. Reduce interaction density (fewer API calls)
2. Add delays between simulations
3. Use GPT-3.5 instead of GPT-4
4. Upgrade your OpenAI plan

### API Credits Exhausted

1. Check your OpenAI account billing
2. Add credits at https://platform.openai.com/account/billing
3. Or switch to template mode temporarily

## Advanced: Using Ollama (Local LLM)

For completely free, offline LLM:

1. Install Ollama: https://ollama.ai
2. Pull a model:
```bash
ollama pull llama2
```

3. Update config:
```json
"llm": {
  "enabled": true,
  "provider": "ollama",
  "model": "llama2"
}
```

4. Install Python package:
```bash
pip install ollama
```

Note: Requires modifying `description_generator.py` to add Ollama support (not included by default).

## Comparison: LLM vs Templates

### With LLM (GPT-4)

```
[18:47 - Courtyard - Dusk]
Marcus leans into Redline's neck, his scarred hands gripping the 
reins with visible tension. The horse's ears flatten backward, 
muscles bunching beneath the saddle. Three pink pigs emerge from 
the archway's shadow, circling the pair twice before Spindle stops 
at Marcus's boot. Above them, the sky shifts from bakery pink to 
deep violet. A coiled white rope lies undisturbed near the wall.

Material details: Leopard print sharp against chestnut coat. Pink 
bodies against cracked concrete. White rope bright in fading light. 
Long shadows reaching across the courtyard.

Emotional temperature: Tense, verging on rupture
```

### Without LLM (Templates)

```
[18:47 - Courtyard - Dusk]
Marcus approaches Redline. The animal's response is uncertain. 
A moment of contact, then separation. Three pigs circle them.

Material details: Dusk light. Colors muted. The ground catches 
the eye.

Emotional temperature: Tense
```

Both work, but LLM provides much richer source material for visual art.

## Recommended Settings

### For Production Work (Final Field Notes)

```json
"llm": {
  "enabled": true,
  "provider": "openai",
  "model": "gpt-4",
  "temperature": 0.8
}
```

### For Exploration (Testing Scenarios)

```json
"llm": {
  "enabled": false
}
```

Or use GPT-3.5:
```json
"model": "gpt-3.5-turbo"
```

### For Maximum Creativity

```json
"temperature": 0.9
```

### For Consistency

```json
"temperature": 0.6
```

---

**Questions?** Check the main [README.md](README.md) or [TECHNICAL.md](TECHNICAL.md) for more details.


