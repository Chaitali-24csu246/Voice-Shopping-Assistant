#!/bin/bash

# Voice Shopping Assistant - Quick Setup Script
# This script downloads the speech recognition model and sets up the environment

echo "================================"
echo "Voice Shopping Assistant Setup"
echo "================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your internet connection."
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

# Download Vosk model if not present
MODEL_DIR="vosk-model-small-en-us-0.15"
if [ -d "$MODEL_DIR" ]; then
    echo "✅ Speech model already downloaded!"
else
    echo "📥 Downloading speech recognition model (~40MB)..."
    echo "This may take a minute..."
    
    curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download model. Please check your internet connection."
        exit 1
    fi
    
    echo "📦 Extracting model..."
    unzip -q vosk-model-small-en-us-0.15.zip
    rm vosk-model-small-en-us-0.15.zip
    
    echo "✅ Speech model downloaded and extracted!"
fi

echo ""
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Set your ScaleDown API key:"
echo "   export SCALEDOWN_API_KEY='sk-your-api-key-here'"
echo ""
echo "2. Run the assistant:"
echo "   python3 voice_shopping_assistant.py"
echo ""
echo "Need help? Check README.md for detailed instructions."
echo ""
