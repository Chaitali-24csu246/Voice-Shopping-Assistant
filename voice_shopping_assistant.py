# SIMPLE Voice Search Assistant (Search Only Version)
# -------------------------------------------------
# Clean version:
# ✔ Uses Vosk for speech-to-text
# ✔ Uses OS-based TTS (say / SAPI / espeak)
# ✔ Uses SerpAPI Google Shopping ONLY
# ✔ No Gemini
# ✔ No ScaleDown
# ✔ No keyword rewriting
# ✔ No cart logic
# ✔ Just clean voice → shopping results

import os
import json
import requests
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import platform
import subprocess

# ---------------- ENV ----------------
load_dotenv()
SERPAPI_KEY = os.getenv("SERP_API_KEY")

if not SERPAPI_KEY:
    raise RuntimeError("SERP_API_KEY missing in .env file")

# ---------------- TTS ----------------
def speak(text: str):
    print("🔊", text)
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.run(["say", text])
        elif system == "Windows":
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        else:
            subprocess.run(["espeak", text])
    except:
        pass

# ---------------- VOSK ----------------
sd.default.samplerate = 16000
sd.default.channels = 1

MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Vosk model folder missing. Place model inside ./model")

vosk_model = Model(MODEL_PATH)


def listen_once(seconds=4):
    samplerate = 16000
    rec = KaldiRecognizer(vosk_model, samplerate)

    print("🎤 Listening...")
    recording = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()

    audio_bytes = recording.tobytes()

    if rec.AcceptWaveform(audio_bytes):
        result = json.loads(rec.Result())
    else:
        result = json.loads(rec.FinalResult())

    text = result.get("text", "").strip().lower()

    print("🗣 You said:", text)
    return text

# ---------------- SERP (GOOGLE SHOPPING ONLY) ----------------
def search_products(query):
    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google_shopping",
        "hl": "en",
        "gl": "in"
    }

    print("🛍 Searching:", query)

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for item in data.get("shopping_results", [])[:5]:
        results.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "link": item.get("link")
        })

    return results

# ---------------- MAIN LOOP ----------------
print("🎙 Voice Shopping Search Assistant")
print("Say something like: wireless headphones")
print("Ctrl+C to exit\n")

while True:
    try:
        query = listen_once()

        if not query:
            continue

        results = search_products(query)

        if not results:
            speak("I could not find shopping results. Please try again.")
            continue

        speak("Here are the top results")

        print("\nResults:")
        for i, item in enumerate(results):
            print(f"[{i}] {item['title']}")
            print(f"     💰 {item.get('price', 'N/A')}")
            print(f"     🔗 {item['link']}\n")

    except KeyboardInterrupt:
        print("\nGoodbye 👋")
        break
