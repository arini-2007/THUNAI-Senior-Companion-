"""
THUNAI — Your Caring AI Companion (துணை)
Master Standalone Native Desktop Application
"""

import os
import sys
import time
import socket
import urllib.request
import urllib.error
import subprocess
import threading
import webbrowser
from http.server import HTTPServer

# Resolve base directory (handles PyInstaller bundle or standard script)
if getattr(sys, 'frozen', False):
    BUNDLE_DIR = sys._MEIPASS
    APP_DIR = os.path.dirname(sys.executable)
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = BUNDLE_DIR

# Ensure working directory is APP_DIR so relative files work
os.chdir(APP_DIR)

# Import local backend modules
sys.path.insert(0, BUNDLE_DIR)
sys.path.insert(0, APP_DIR)

import server

TARGET_PORT = 8080
FALLBACK_PORT = 8085


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def is_thunai_responsive(port):
    try:
        url = f"http://localhost:{port}/api/status"
        req = urllib.request.Request(url, headers={'User-Agent': 'THUNAI-Desktop-App'})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def start_background_server():
    """Starts the THUNAI server as an independent background process if not already running."""
    active_port = TARGET_PORT
    if is_thunai_responsive(TARGET_PORT):
        return TARGET_PORT

    pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = sys.executable

    server_script = os.path.join(APP_DIR, "server.py")
    subprocess.Popen([pythonw_exe, server_script], cwd=APP_DIR)

    # Wait up to 6 seconds for server to respond
    for _ in range(60):
        if is_thunai_responsive(active_port):
            return active_port
        time.sleep(0.1)

    return active_port


def launch_native_window(port):
    """
    Launches THUNAI as a dedicated standalone Windows Desktop Application.
    Uses MS Edge App Mode or Chrome App Mode (no address bar, no tabs, native titlebar).
    Falls back to pywebview or system default browser if needed.
    """
    app_url = f"http://localhost:{port}"

    # Search for Microsoft Edge or Chrome to run in standalone App Mode
    browser_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

    edge_exe = next((p for p in browser_candidates if os.path.exists(p)), None)

    if edge_exe:
        cmd = [
            edge_exe,
            f"--app={app_url}",
            "--window-size=480,900"
        ]
        try:
            subprocess.Popen(cmd)
            return
        except Exception as e:
            print(f"[THUNAI App] Edge App Mode error: {e}")

    # Fallback to pywebview
    try:
        import webview
        icon_path = os.path.join(BUNDLE_DIR, "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(APP_DIR, "icon.ico")
        
        window = webview.create_window(
            title="THUNAI — Your Caring AI Companion (துணை)",
            url=app_url,
            width=480,
            height=900,
            resizable=True
        )
        webview.start()
        return
    except Exception as e:
        print(f"[THUNAI App] pywebview fallback error: {e}")

    # Final fallback
    webbrowser.open(app_url)


def main():
    print("=" * 60)
    print("  🌸 Starting THUNAI — Your Caring AI Companion App 🌸")
    print("=" * 60)
    active_port = start_background_server()
    launch_native_window(active_port)


if __name__ == "__main__":
    main()
