# Architecture

THUNAI is a browser app served by a small local Python server. There is no build step.

```text
User (phone browser, laptop browser or desktop window)
  |
index.html  (PWA front end, with manifest.json and sw.js)
  |-- Home chat and voice (browser speech recognition and synthesis)
  |-- Medicines, Health, Caregiver and Relax screens
  |-- Relaxation music (Web Audio API)
  |
server.py  (local Python web server)
  |-- GET   /api/status, /api/state, /api/tts
  |-- POST  /api/chat, /api/state, /api/measurements,
  |         /api/scan-medicine, /api/emergency
  |
  |-- agent_brain.py       language detection, intents, replies
  |                        (Gemini 2.5 Flash, or offline rules)
  |-- medicine_scanner.py  label analysis (Gemini vision, or demo data)
  |-- state.py             profile, reminders, music library, memory
  |                        -> saved to thunai_data.json
  |
thunai_app.py  opens the same app in a desktop-style window
```

## Reasoning layer
`agent_brain.py` and `state.py` include a MeTTa-style knowledge base and reasoning trace, shown in the app as **MeTTa Logic**. It is written in Python and does not run a Hyperon engine.

## Keys and data
- No API key is stored in the code. Gemini is enabled through the `GEMINI_API_KEY` environment variable or a key entered in the app.
- A key entered in the app is kept in that browser and sent only to the local server. For any public deployment, use the environment variable instead.
- `thunai_data.json` holds saved app data, so it is kept out of GitHub (see [INTEGRATION.md](INTEGRATION.md)).
