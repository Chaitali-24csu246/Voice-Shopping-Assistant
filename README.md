# 🛍️ Voice Shopping Assistant with ScaleDown

A voice-controlled shopping assistant that searches the web for products and uses ScaleDown API to optimize prompts for efficient processing.

## Features

- 🎤 **Voice Input**: Speak naturally to search for products
- 🔊 **Voice Output**: Assistant speaks back to you
- 🌐 **Web Search**: Searches for products online automatically
- ⚡ **ScaleDown Integration**: Optimizes prompts to save tokens and costs
- 🚀 **Simple & Lightweight**: Easy to set up and run
- 🔒 **Offline Speech Recognition**: Uses Vosk (no internet needed for speech-to-text)
- ✅ **Python 3.13 Compatible**: Works with the latest Python version

## Prerequisites

- Python 3.8 or higher
- A microphone (for voice input)
- ScaleDown API key (get one from [scaledown.ai](https://scaledown.ai))
- Internet connection

## Installation

### Step 1: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

**Works with Python 3.13!** This version uses Vosk for offline speech recognition (no PyAudio issues).

### Step 2: Download Speech Recognition Model

Download the Vosk English model (~40MB):

```bash
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

**Or download manually:**
1. Visit: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
2. Download and extract the zip file
3. Place the `vosk-model-small-en-us-0.15` folder in the same directory as `voice_shopping_assistant.py`

The folder structure should look like:
```
your-folder/
├── voice_shopping_assistant.py
├── requirements.txt
├── README.md
└── vosk-model-small-en-us-0.15/
    ├── am/
    ├── conf/
    ├── graph/
    └── ...
```

### Step 3: Set Up ScaleDown API Key

Set your ScaleDown API key as an environment variable:

**On macOS/Linux:**
```bash
export SCALEDOWN_API_KEY='sk-your-api-key-here'
```

**On Windows (Command Prompt):**
```cmd
set SCALEDOWN_API_KEY=sk-your-api-key-here
```

**On Windows (PowerShell):**
```powershell
$env:SCALEDOWN_API_KEY='sk-your-api-key-here'
```

## Usage

### Running the Assistant

```bash
python voice_shopping_assistant.py
```

### How to Use

1. **Start the program** - The assistant will greet you and ask what you're looking for
2. **Speak your query** - Say something like "wireless headphones" or "running shoes"
3. **Wait for results** - The assistant will search and read out the top products
4. **Continue or exit** - Say "yes" to search again, or "goodbye" to exit

### Voice Commands

- **Search**: Just speak the product name (e.g., "laptop", "coffee maker")
- **Help**: Say "help" to hear instructions
- **Exit**: Say "goodbye", "exit", "quit", or "bye" to stop

### Example Interaction

```
🔊 Assistant: Hello! I'm your voice shopping assistant. What can I help you find today?

🎤 Listening...
👤 You said: wireless mouse

🔊 Assistant: Searching for wireless mouse...
✅ ScaleDown: 450 → 189 tokens (58.0% saved)

🔊 Assistant: I found 5 results for 'wireless mouse'. Here are the top options:

1. Logitech MX Master 3S Wireless Mouse
2. Razer DeathAdder V3 Pro Wireless Gaming Mouse
3. Apple Magic Mouse - Wireless, Rechargeable

Would you like more details about any of these?

🔊 Assistant: Would you like to search for something else?

🎤 Listening...
👤 You said: goodbye

🔊 Assistant: Thank you for shopping! Goodbye!
```

## How ScaleDown Integration Works

The assistant uses ScaleDown to optimize prompts before processing:

1. **Collects product data** from web searches
2. **Builds a context** with all product information
3. **Sends to ScaleDown API** for compression
4. **Receives optimized prompt** with 40-60% fewer tokens
5. **Processes efficiently** with reduced cost and latency

### Token Savings Example

```
Before ScaleDown:
Context: 1,200 tokens
Prompt: 150 tokens
Total: 1,350 tokens

After ScaleDown:
Compressed: 540 tokens
Savings: 60% (810 tokens saved)
```

## Troubleshooting

### Model Not Found Error

If you see "Speech model not found":
- Make sure you downloaded and extracted the Vosk model
- Check that the folder name is exactly `vosk-model-small-en-us-0.15`
- Verify it's in the same directory as `voice_shopping_assistant.py`

### Microphone Issues

If the assistant can't hear you:
- Check microphone permissions in system settings
- Make sure your microphone is set as the default input device
- Try speaking louder and closer to the microphone
- On Mac: Go to System Preferences > Security & Privacy > Microphone and allow Terminal

### Speech Recognition Errors

If recognition is inaccurate:
- Speak more clearly and at a moderate pace
- Reduce background noise
- Try the larger Vosk model for better accuracy: `vosk-model-en-us-0.22` (1.8GB)

### ScaleDown API Errors

If you see ScaleDown errors:
- Verify your API key is correct: `echo $SCALEDOWN_API_KEY`
- Check your internet connection
- Ensure you have API credits remaining

### Installation Issues

**Vosk won't install:**
- Make sure you have Python 3.8+ installed
- Try: `pip3 install --upgrade pip` then reinstall

**pyttsx3 speech issues:**
- On Linux, install espeak: `sudo apt-get install espeak`
- On macOS, it should work out of the box
- On Windows, try running as administrator

## Configuration Options

You can modify these settings in `voice_shopping_assistant.py`:

```python
# Text-to-speech speed (words per minute)
tts_engine.setProperty('rate', 175)  # Default: 175

# Number of search results
products = search_products(user_input, max_results=5)  # Default: 5

# ScaleDown compression model
compress_with_scaledown(context, prompt, model="gpt-4o")  # Options: gpt-4o, gpt-4o-mini, gemini-2.5-flash

# Vosk model path (if using a different model)
model_path = "vosk-model-small-en-us-0.15"
```

### Using a Better Speech Model

For improved accuracy, download a larger model:
- **Standard** (1.8GB): https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
- **Small** (40MB, current): https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

Extract and update the `model_path` variable in the code.

## Advanced Features

### Adding LLM Integration

The current version generates simple summaries. To add full LLM integration:

1. Install OpenAI or Anthropic SDK:
```bash
pip install openai  # or anthropic
```

2. Modify `generate_shopping_summary()` function to call your LLM with the compressed prompt

### Customizing Voice

Change the voice in the code:

```python
# List available voices
voices = tts_engine.getProperty('voices')
for voice in voices:
    print(voice.name)

# Set a specific voice
tts_engine.setProperty('voice', voices[0].id)
```

## Project Structure

```
voice-shopping-assistant/
├── voice_shopping_assistant.py  # Main application
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## API Reference

### ScaleDown API Endpoint

```
POST https://api.scaledown.xyz/compress/raw/
```

### Required Headers
```json
{
  "x-api-key": "your-api-key",
  "Content-Type": "application/json"
}
```

### Request Payload
```json
{
  "context": "Your context here",
  "prompt": "Your prompt here",
  "model": "gpt-4o",
  "scaledown": {
    "rate": "auto"
  }
}
```

## Performance

- Average search time: 2-3 seconds
- ScaleDown compression: 1-2 seconds
- Token savings: 40-60% on average
- Voice recognition: ~1 second per phrase

## Limitations

- Requires internet connection for web search (but NOT for speech recognition!)
- Search results depend on DuckDuckGo availability
- Voice recognition accuracy varies with accent and background noise
- Product information may not include prices (depends on search results)
- First run requires downloading ~40MB speech model

## Future Enhancements

- [ ] Add multiple search engines
- [ ] Price comparison across stores
- [ ] Shopping cart functionality
- [ ] Order history
- [ ] Product recommendations
- [ ] Multi-language support

## License

MIT License - Feel free to use and modify for your event!

## Support

For ScaleDown API issues, visit: [docs.scaledown.ai](https://docs.scaledown.ai)

For project-specific issues, check the troubleshooting section above.

## Credits

Built with:
- [Vosk](https://alphacephei.com/vosk/) for offline speech recognition
- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio input
- [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- [ScaleDown](https://scaledown.ai) for prompt optimization

---

**Happy Shopping! 🛍️**
