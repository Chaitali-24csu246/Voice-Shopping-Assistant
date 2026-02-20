# =============================
# README.md
# =============================
# 🎙 Voice Shopping Assistant (Terminal)

A simple voice-powered shopping search assistant that converts speech → text → Google Shopping results using SerpAPI.
note(earlier features such as gemini optimization scaledown token reduction, and streamlmit were removed to focus on cleaner functionality, and cross platform availability of voice model)

This version is intentionally minimal and stable:
- 🎤 Offline speech recognition using Vosk
- 🛍 Real shopping results via SerpAPI (Google Shopping)
- 🔊 Cross-platform text-to-speech
- 🧼  no keyword rewriting, no bloat

---

## ✨ Features

- Voice input using your microphone
- Real-time product search
- Speaks results aloud
- Works fully in terminal
- Cross-platform (macOS, Windows, Linux)

---

## 📦 Requirements

- Python 3.9+
- Microphone access
- SerpAPI key (free tier available)

---

## 🔧 Installation

### 1️⃣ Clone or Download Project

```bash
git clone <your-repo-url>
cd voice-shopping-assistant
```

Or just place the script in a folder.

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Download Vosk Speech Model

Download a small English model:

👉 https://alphacephei.com/vosk/models

Recommended model:
**vosk-model-small-en-us-0.15**

Steps:
1. Download ZIP
2. Extract it
3. Rename folder to:
   ```
   model
   ```
4. Place it next to your script

Folder structure should look like:

```
voice_search.py
model/
  ├── am/
  ├── conf/
  └── graph/
```

---

### 4️⃣ Get SerpAPI Key

Sign up at:
👉 https://serpapi.com

Free tier is enough for testing.

Create a `.env` file in the same folder:

```
SERP_API_KEY=your_key_here
```

⚠️ No quotes or spaces

---

## ▶️ Running the App

```bash
python voice_search.py
```

You will see:

```
🎙 Voice Shopping Search Assistant
Say something like: wireless headphones
```

Speak clearly for ~4 seconds.

---

## 🗣 Example Queries

- wireless headphones
- gaming mouse
- nike running shoes
- bluetooth speaker
- mechanical keyboard

---

## 🧠 How It Works

1. 🎤 Vosk records audio from microphone
2. 📝 Converts speech → text locally (offline)
3. 🌐 Sends query to SerpAPI Google Shopping
4. 📦 Displays top 5 product results
5. 🔊 Reads results aloud

---

## 🔊 Text-to-Speech by OS

| OS | Engine |
|----|--------|
| macOS | `say` (built-in) |
| Windows | SAPI via pyttsx3 |
| Linux | espeak |

---

## 🛠 Troubleshooting

### Microphone not working (macOS)
System Settings → Privacy → Microphone → Allow Terminal

---

### Linux audio issues
Install portaudio:

```bash
sudo apt install portaudio19-dev
```

---

### Windows mic issues

```bash
pip install pipwin
pipwin install pyaudio
```

---

### No results returned
- Ensure SerpAPI key is valid
- Check free tier usage limit
- Try simpler queries (e.g., "headphones")

---

## 🚀 Future Improvements (Optional)

- Voice commands (add to cart)
- Real-time streaming mic
- GUI (Streamlit or Electron)
- Keyword optimization layer
- Multi-language support

---

## 📄 License

MIT License — free to use and modify.

---

## ❤️ Credits

- Vosk for offline speech recognition
- SerpAPI for product search
- Python audio ecosystem

---

If you found this useful, consider adding:
⭐ GitHub star
🍴 Fork for your own assistant

