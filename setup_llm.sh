#!/bin/bash
# LLM Setup Helper Script

echo "========================================="
echo "  LLM Integration Setup"
echo "========================================="
echo ""

# Check if OpenAI package is installed
if python3 -c "import openai" 2>/dev/null; then
    echo "✓ OpenAI package is already installed"
else
    echo "Installing OpenAI package..."
    pip install openai==1.3.0
    if [ $? -eq 0 ]; then
        echo "✓ OpenAI package installed successfully"
    else
        echo "✗ Failed to install OpenAI package"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "  API Key Setup"
echo "========================================="
echo ""

# Check if API key is already set
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ OPENAI_API_KEY is already set in environment"
    echo "  Current value: ${OPENAI_API_KEY:0:8}..."
else
    echo "OPENAI_API_KEY is not set."
    echo ""
    read -p "Would you like to set it now? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenAI API key: " api_key
        
        # Set for current session
        export OPENAI_API_KEY="$api_key"
        
        # Add to shell profile for persistence
        echo ""
        echo "To make this permanent, add to your shell profile:"
        echo ""
        echo "  echo 'export OPENAI_API_KEY=\"$api_key\"' >> ~/.zshrc"
        echo "  # or for bash: >> ~/.bashrc"
        echo ""
        read -p "Add to ~/.zshrc now? (y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.zshrc
            echo "✓ Added to ~/.zshrc"
            echo "  Run 'source ~/.zshrc' or restart terminal"
        fi
    fi
fi

echo ""
echo "========================================="
echo "  Configuration"
echo "========================================="
echo ""

# Check config
if grep -q '"enabled": true' config/default_config.json; then
    echo "✓ LLM is enabled in config/default_config.json"
else
    echo "⚠ LLM is disabled in config/default_config.json"
    echo "  Edit config/default_config.json and set 'enabled': true"
fi

echo ""
echo "========================================="
echo "  Testing Connection"
echo "========================================="
echo ""

if [ -n "$OPENAI_API_KEY" ]; then
    echo "Testing OpenAI API connection..."
    python3 -c "
import os
try:
    import openai
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    # Simple test - just check if we can create a client
    print('✓ OpenAI package loaded successfully')
    print('✓ API key configured')
    print('')
    print('Note: Actual API test will occur when you run the simulation')
except Exception as e:
    print(f'✗ Error: {e}')
    exit(1)
"
else
    echo "⚠ Skipping connection test (no API key set)"
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Run the web interface: python run.py"
echo "  2. Check 'Use LLM' in the web interface"
echo "  3. Or run: python example_scenario.py"
echo ""
echo "LLM will generate higher-quality field note descriptions."
echo ""


