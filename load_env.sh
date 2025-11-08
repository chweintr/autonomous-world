#!/bin/bash
# Load environment variables from .env file

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✓ Loaded API key from .env file"
    echo "  Key: ${OPENAI_API_KEY:0:8}...${OPENAI_API_KEY: -4}"
else
    echo "✗ .env file not found"
    exit 1
fi


