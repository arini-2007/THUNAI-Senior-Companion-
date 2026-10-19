"""
THUNAI — Master AI & Elder-Care Assistant Web Server
Endpoints:
  GET  /                     -> Serves the master elder-care PWA
  GET  /api/status           -> System health, gTTS status, and Gemini SDK availability
  GET  /api/state            -> Returns full elder profile, medical data, and history
  POST /api/state            -> Saves updated state to persistent storage
  POST /api/chat             -> Agentic multilingual processing (Tamil, English, Tanglish)
  GET  /api/tts?text=&lang=  -> Streams real-time native Tamil / English audio via gTTS
  POST /api/measurements     -> Logs vitals measurements to medical record & care timeline
  POST /api/scan-medicine    -> Multimodal OCR label extractor with safe elder guidance
  POST /api/emergency        -> Triggers emergency protocol, logs timeline, formats alerts
"""

import os
import sys
import json
import socket
import urllib.parse
import webbrowser
import subprocess
import io
import hashlib
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Import THUNAI modules
from state import load_state, save_state
from agent_brain import process_elder_request, GOOGLE_GENAI_AVAILABLE
from medicine_scanner import analyze_medicine_image

# Configure standard output to utf-8 if available
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Try importing gTTS
GTTS_AVAILABLE = False
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

PORT = 8080
AUDIO_CACHE = {}  # In-memory MP3 audio cache by MD5 hash
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


class ThunaiRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    def end_headers(self):
        # Enable CORS and PWA headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Gemini-Key')
        self.send_header('Service-Worker-Allowed', '/')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        if path.endswith('.json') or path.endswith('manifest.json'):
            return 'application/manifest+json'
        if path.endswith('.js'):
            return 'application/javascript'
        if path.endswith('.png'):
            return 'image/png'
        if path.endswith('.ico'):
            return 'image/x-icon'
        if path.endswith('.svg'):
            return 'image/svg+xml'
        return super().guess_type(path)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # 1. API: System Status
        if path == "/api/status":
            status_data = {
                "app": "THUNAI — Your Caring AI Companion",
                "version": "2.5.0",
                "google_genai_available": GOOGLE_GENAI_AVAILABLE,
                "gtts_available": GTTS_AVAILABLE,
                "environment_api_key_set": bool(os.environ.get("GEMINI_API_KEY")),
                "supported_languages": ["ta", "en", "tanglish", "auto"]
            }
            self.send_json_response(200, status_data)
            return

        # 2. API: Get Current State
        if path == "/api/state":
            state = load_state()
            self.send_json_response(200, state)
            return

        # 3. API: Real-time Audio Stream via gTTS
        if path == "/api/tts":
            raw_text = query_params.get("text", [""])[0]
            req_lang = query_params.get("lang", ["auto"])[0]

            if not raw_text or not GTTS_AVAILABLE:
                self.send_response(400)
                self.end_headers()
                return

            # Clean text of markdown asterisks, hashes, and emojis for smooth TTS
            clean_text = raw_text.replace("*", "").replace("#", "").replace("`", "")
            # Determine TTS language code
            tts_lang = "ta" if (req_lang in ["ta", "tanglish"]) else "en"

            cache_key = hashlib.md5(f"{clean_text}_{tts_lang}".encode("utf-8")).hexdigest()

            if cache_key in AUDIO_CACHE:
                audio_bytes = AUDIO_CACHE[cache_key]
            else:
                try:
                    fp = io.BytesIO()
                    if tts_lang == "ta":
                        tts = gTTS(text=clean_text, lang="ta", slow=False)
                    else:
                        tts = gTTS(text=clean_text, lang="en", tld="co.in", slow=False)
                    tts.write_to_fp(fp)
                    audio_bytes = fp.getvalue()
                    AUDIO_CACHE[cache_key] = audio_bytes
                except Exception as e:
                    print(f"[THUNAI TTS] Error generating audio: {e}")
                    self.send_response(500)
                    self.end_headers()
                    return

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(audio_bytes)))
            self.end_headers()
            self.wfile.write(audio_bytes)
            return

        # Default static file serving (index.html, sw.js, manifest.json, etc.)
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)

        data = {}
        if post_body:
            try:
                data = json.loads(post_body.decode("utf-8"))
            except Exception as e:
                print(f"[THUNAI API] JSON parse error: {e}")

        # 1. API: Chat (Agentic Multilingual Processing)
        if path == "/api/chat":
            query = data.get("query") or data.get("message") or ""
            forced_lang = data.get("lang") or data.get("language") or "auto"
            custom_key = data.get("apiKey") or self.headers.get("X-Gemini-Key")

            # Run agent brain pipeline
            result = process_elder_request(query, forced_lang=forced_lang, api_key=custom_key)

            # Generate audio URL if gTTS is active
            if GTTS_AVAILABLE and result.get("reply"):
                tts_lang = "ta" if result.get("reply_language") in ["ta", "tanglish"] else "en"
                quoted_text = urllib.parse.quote(result["reply"][:300])
                result["audioUrl"] = f"/api/tts?text={quoted_text}&lang={tts_lang}"

            # Attach updated state snapshot
            result["latest_state"] = load_state()

            self.send_json_response(200, result)
            return

        # 2. API: Save State
        if path == "/api/state":
            if data:
                save_state(data)
                self.send_json_response(200, {"status": "saved", "message": "State updated successfully."})
            else:
                self.send_json_response(400, {"error": "Missing state data."})
            return

        # 3. API: Record Measurement
        if path == "/api/measurements":
            m_type = data.get("type", "Blood Pressure")
            m_val = data.get("value", "120/80")
            m_unit = data.get("unit", "mmHg")
            m_context = data.get("context", "Manual entry")
            
            from agent_brain import ThunaiTools
            res = ThunaiTools.recordMeasurement(m_type, m_val, m_unit, m_context)
            self.send_json_response(200, {"status": "recorded", "result": res, "latest_state": load_state()})
            return

        # 4. API: Scan Medicine Image
        if path == "/api/scan-medicine":
            image_b64 = data.get("image", "")
            filename = data.get("filename", "")
            custom_key = data.get("apiKey") or self.headers.get("X-Gemini-Key")
            
            res = analyze_medicine_image(image_b64, api_key=custom_key, filename=filename)
            self.send_json_response(200, res)
            return

        # 5. API: Emergency Trigger
        if path == "/api/emergency":
            symptom = data.get("symptom", "Immediate emergency button pressed")
            from agent_brain import ThunaiTools
            res = ThunaiTools.handleEmergency(symptom)
            self.send_json_response(200, {"status": "emergency_activated", "details": res, "latest_state": load_state()})
            return

        # Unknown POST route
        self.send_json_response(404, {"error": f"Route {path} not found"})

    def send_json_response(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def launch_standalone_app_window(url):
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".thunai_profile")
    for exe in edge_paths:
        if os.path.exists(exe):
            cmd = f'"{exe}" --app="{url}" --user-data-dir="{profile_dir}" --window-size=440,920 --no-first-run --no-default-browser-check'
            subprocess.Popen(cmd, shell=True)
            return True
    webbrowser.open(url)
    return False


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    local_ip = get_local_ip()
    local_url = f"http://localhost:{PORT}"
    network_url = f"http://{local_ip}:{PORT}"

    server_address = ('', PORT)
    try:
        httpd = HTTPServer(server_address, ThunaiRequestHandler)
    except OSError:
        # Port might be in use, fallback to 8085
        httpd = HTTPServer(('', 8085), ThunaiRequestHandler)
        local_url = f"http://localhost:8085"
        network_url = f"http://{local_ip}:8085"

    print("=" * 64)
    print("  THUNAI — Your Caring AI Companion (துணை)")
    print("=" * 64)
    print(f"  [1] Standalone Desktop App:  {local_url}")
    print(f"  [2] Mobile Phone on Wi-Fi:   {network_url}")
    print(f"  [3] Speech Engine (gTTS):    {'Active (Tamil & English)' if GTTS_AVAILABLE else 'Web Speech Fallback'}")
    print(f"  [4] Gemini 2.5 Flash SDK:    {'Active' if GOOGLE_GENAI_AVAILABLE else 'Rule Engine Active'}")
    print("-" * 64)
    print("  Press Ctrl+C to stop the THUNAI server.")
    print("=" * 64)

    # Launch standalone window unless requested not to
    if "--no-browser" not in sys.argv and not os.environ.get("NO_BROWSER"):
        launch_standalone_app_window(local_url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping THUNAI server...")
        httpd.server_close()


if __name__ == '__main__':
    main()
