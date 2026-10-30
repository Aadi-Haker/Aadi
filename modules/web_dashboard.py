"""
Aadi — Local Web Dashboard UI (Flask / HTTP Server)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from rich.console import Console

console = Console()

class AadiDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <html>
        <head><title>AADI Security Dashboard</title></head>
        <body style="background:#121212; color:#00ffcc; font-family:monospace; text-align:center; padding-top:50px;">
            <h1>👻 AADI — Advanced Android Pentesting Suite</h1>
            <p>Status: <span style="color:#00ff00;">Online & Secure</span></p>
            <hr style="border:1px solid #333; width:50%;">
            <p>Local C2 & Device Audit Server is running smoothly.</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

def start_web_server(port: int = 8000):
    """Start local HTTP web dashboard server."""
    try:
        server = HTTPServer(("127.0.0.1", port), AadiDashboardHandler)
        console.print(f"[bold green]✓ AADI Web Dashboard running at http://127.0.0.1:{port}[/]")
        server.serve_forever()
    except Exception as e:
        console.print(f"[bold red]✗ Web server error:[/] {e}")

def run_web_dashboard_background(port: int = 8000):
    t = threading.Thread(target=start_web_server, args=(port,), daemon=True)
    t.start()