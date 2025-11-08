#!/usr/bin/env python3
"""
Test LLM integration to verify OpenAI is set up correctly.
"""
import os
import sys

print("=" * 60)
print("  LLM Integration Test")
print("=" * 60)
print()

# Check if OpenAI package is installed
print("1. Checking OpenAI package...")
try:
    import openai
    print("   ✓ OpenAI package installed")
    print(f"   Version: {openai.__version__}")
except ImportError:
    print("   ✗ OpenAI package not installed")
    print("   Run: python3 -m pip install openai")
    sys.exit(1)

print()

# Check if API key is set
print("2. Checking API key...")
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    print("   ✗ OPENAI_API_KEY not set")
    print()
    print("   To set it:")
    print("   1. Get key from: https://platform.openai.com/api-keys")
    print("   2. Run: export OPENAI_API_KEY='sk-your-key-here'")
    print("   3. Or add to ~/.zshrc for permanence")
    sys.exit(1)

if not api_key.startswith('sk-'):
    print("   ⚠ API key doesn't look right (should start with 'sk-')")
else:
    print(f"   ✓ API key found: {api_key[:8]}...{api_key[-4:]}")

print()

# Test API connection
print("3. Testing OpenAI API connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    # Simple test call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, World!' and nothing else."}
        ],
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"   ✓ API connection successful!")
    print(f"   Response: {result}")
    
except Exception as e:
    print(f"   ✗ API test failed: {e}")
    print()
    print("   Common issues:")
    print("   - Invalid API key")
    print("   - No credits on OpenAI account")
    print("   - Network connection problem")
    sys.exit(1)

print()
print("=" * 60)
print("  ✓ LLM Integration Ready!")
print("=" * 60)
print()
print("You can now:")
print("  1. Run: python run.py")
print("  2. Check 'Use LLM' in the web interface")
print("  3. Generate high-quality field notes")
print()
print("Note: Using GPT-4 costs ~$0.50-$1 per 60-min simulation")
print("      Using GPT-3.5 costs ~$0.05-$0.10 per simulation")
print()


