"""
Voice-Based Shopping Assistant with ScaleDown Integration
A simple voice-controlled shopping assistant that searches the web for products
and uses ScaleDown API to optimize prompts for efficient LLM responses.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import queue
import sys
import subprocess
import platform

# ============================================================================
# CONFIGURATION
# ============================================================================

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY", "")
SCALEDOWN_API_URL = "https://api.scaledown.xyz/compress/raw/"

# Detect platform for text-to-speech
IS_MAC = platform.system() == "Darwin"

# Initialize Vosk model (will be loaded in main)
model = None
audio_queue = queue.Queue()


# ============================================================================
# VOICE FUNCTIONS
# ============================================================================

def speak(text):
    """Convert text to speech using native macOS 'say' command"""
    print(f"🔊 Assistant: {text}")
    
    if IS_MAC:
        # Use macOS native text-to-speech (much more reliable)
        subprocess.run(['say', text], check=False)
    else:
        # Fallback for other platforms
        print("   [Text-to-speech not available on this platform]")


def audio_callback(indata, frames, time_info, status):
    """Callback for audio stream"""
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))


def listen():
    """Listen for user voice input and convert to text using Vosk"""
    global model
    
    if model is None:
        speak("Speech recognition model not loaded. Please check setup.")
        return None
    
    print("🎤 Listening...")
    
    try:
        # Create recognizer
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetWords(True)
        
        # Clear the queue
        while not audio_queue.empty():
            audio_queue.get()
        
        # Start recording
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            
            silence_threshold = 30  # frames of silence
            silence_count = 0
            has_speech = False
            
            while True:
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get('text', '').strip()
                    
                    if text:
                        has_speech = True
                        print(f"👤 You said: {text}")
                        return text.lower()
                else:
                    # Check for partial results to detect speech
                    partial = json.loads(recognizer.PartialResult())
                    if partial.get('partial', ''):
                        has_speech = True
                        silence_count = 0
                    elif has_speech:
                        silence_count += 1
                        
                        # Stop after silence
                        if silence_count > silence_threshold:
                            result = json.loads(recognizer.FinalResult())
                            text = result.get('text', '').strip()
                            
                            if text:
                                print(f"👤 You said: {text}")
                                return text.lower()
                            else:
                                speak("I didn't catch that. Please try again.")
                                return None
    
    except Exception as e:
        print(f"Error during listening: {e}")
        speak("Sorry, there was an error with the microphone.")
        return None


# ============================================================================
# WEB SCRAPING FUNCTIONS
# ============================================================================

def search_products(query, max_results=5):
    """
    Search for products on the web using DuckDuckGo (no API key needed)
    Returns a list of product results with titles, prices, and links
    """
    search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' buy online')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        search_results = soup.find_all('div', class_='result')[:max_results]
        
        for idx, result in enumerate(search_results, 1):
            title_tag = result.find('a', class_='result__a')
            snippet_tag = result.find('a', class_='result__snippet')
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href', '')
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else "No description available"
                
                results.append({
                    'rank': idx,
                    'title': title,
                    'link': link,
                    'description': snippet[:150]  # Limit description length
                })
        
        return results
    
    except Exception as e:
        print(f"Error searching products: {e}")
        return []


# ============================================================================
# SCALEDOWN INTEGRATION
# ============================================================================

def compress_with_scaledown(context, prompt, model="gpt-4o"):
    """
    Use ScaleDown API to compress the prompt before sending to LLM
    """
    if not SCALEDOWN_API_KEY:
        print("⚠️  Warning: SCALEDOWN_API_KEY not set. Skipping compression.")
        return prompt
    
    headers = {
        'x-api-key': SCALEDOWN_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "context": context,
        "prompt": prompt,
        "model": model,
        "scaledown": {
            "rate": "auto"
        }
    }
    
    try:
        response = requests.post(SCALEDOWN_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            compressed_prompt = result.get('compressed_prompt', prompt)
            
            # Show compression stats
            original_tokens = result.get('original_prompt_tokens', 0)
            compressed_tokens = result.get('compressed_prompt_tokens', 0)
            
            if original_tokens > 0:
                savings = ((original_tokens - compressed_tokens) / original_tokens) * 100
                print(f"✅ ScaleDown: {original_tokens} → {compressed_tokens} tokens ({savings:.1f}% saved)")
            
            return compressed_prompt
        else:
            print(f"⚠️  ScaleDown API error: {response.status_code}")
            return prompt
    
    except Exception as e:
        print(f"⚠️  ScaleDown error: {e}")
        return prompt


def generate_shopping_summary(products, user_query):
    """
    Generate a natural language summary of products using ScaleDown optimization
    In a real implementation, this would call an LLM API (OpenAI, Anthropic, etc.)
    For this demo, we'll create a simple formatted response
    """
    if not products:
        return "I couldn't find any products matching your search. Please try a different query."
    
    # Build context from search results
    context = f"User is searching for: {user_query}\n\nSearch Results:\n"
    for product in products:
        context += f"{product['rank']}. {product['title']}\n   {product['description']}\n   Link: {product['link']}\n\n"
    
    # Create prompt for summarization
    prompt = "Summarize the top 3 most relevant products for the user in a friendly, conversational way. Include product names and brief descriptions."
    
    # Compress with ScaleDown
    compressed_prompt = compress_with_scaledown(context, prompt)
    
    # For demo purposes, create a simple summary
    # In production, you'd send compressed_prompt to your LLM API here
    summary = f"I found {len(products)} results for '{user_query}'. Here are the top options:\n\n"
    
    for i, product in enumerate(products[:3], 1):
        summary += f"{i}. {product['title']}\n"
    
    summary += f"\nWould you like more details about any of these?"
    
    return summary


# ============================================================================
# MAIN ASSISTANT LOGIC
# ============================================================================

def shopping_assistant():
    """Main function to run the voice shopping assistant"""
    
    speak("Hello! I'm your voice shopping assistant. What can I help you find today?")
    
    while True:
        # Listen for user input
        user_input = listen()
        
        if user_input is None:
            continue
        
        # Check for exit commands
        if any(word in user_input for word in ['exit', 'quit', 'goodbye', 'bye']):
            speak("Thank you for using the shopping assistant. Goodbye!")
            break
        
        # Check for help command
        if 'help' in user_input:
            speak("Just tell me what product you're looking for, and I'll search for it online. "
                  "Say 'goodbye' when you're done shopping.")
            continue
        
        # Search for products
        speak(f"Searching for {user_input}...")
        products = search_products(user_input, max_results=5)
        
        if not products:
            speak("I couldn't find any products. Please try describing what you're looking for differently.")
            continue
        
        # Generate summary with ScaleDown optimization
        summary = generate_shopping_summary(products, user_input)
        speak(summary)
        
        # Ask if user wants to continue
        speak("Would you like to search for something else?")
        response = listen()
        
        if response and any(word in response for word in ['no', 'nope', 'exit', 'quit']):
            speak("Thank you for shopping! Goodbye!")
            break


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🛍️  VOICE SHOPPING ASSISTANT WITH SCALEDOWN")
    print("=" * 70)
    print("\nSetup Instructions:")
    print("1. Set your ScaleDown API key:")
    print("   export SCALEDOWN_API_KEY='your-api-key-here'")
    print("\n2. Make sure your microphone is connected and working")
    print("\n3. Speak clearly when prompted")
    print("\n" + "=" * 70 + "\n")
    
    # Load Vosk model
    print("Loading speech recognition model...")
    model_path = "vosk-model-small-en-us-0.15"
    
    if not os.path.exists(model_path):
        print(f"\n❌ ERROR: Speech model not found at '{model_path}'")
        print("\nPlease download the model:")
        print("1. Download from: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
        print("2. Extract the zip file")
        print("3. Place the 'vosk-model-small-en-us-0.15' folder in the same directory as this script")
        print("\nOr run this command:")
        print("  curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
        print("  unzip vosk-model-small-en-us-0.15.zip")
        sys.exit(1)
    
    model = Model(model_path)
    print("✅ Speech model loaded successfully!\n")
    
    if not SCALEDOWN_API_KEY:
        print("⚠️  WARNING: SCALEDOWN_API_KEY not set!")
        print("The assistant will work but won't use prompt compression.")
        print("Set the API key using: export SCALEDOWN_API_KEY='your-key'\n")
    
    try:
        shopping_assistant()
    except KeyboardInterrupt:
        print("\n\nAssistant stopped by user.")
        speak("Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        speak("Sorry, something went wrong. Please restart the assistant.")
