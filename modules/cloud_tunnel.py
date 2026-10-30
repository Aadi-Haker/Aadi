"""
Aadi — Cloudflare Tunnel Manager for Global ADB Access
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import shutil
import time
from rich.console import Console
from rich.panel import Panel

console = Console()

def start_cloud_tunnel(local_port: int = 5555):
    """Start a Cloudflare quick TCP tunnel for global ADB access."""
    if not shutil.which("cloudflared"):
        console.print("[bold red]✗ 'cloudflared' is not installed.[/] Install it first.")
        console.print("[dim]Run: sudo apt install cloudflared or download from Cloudflare docs.[/]")
        return False

    console.print(Panel(
        f"[bold cyan]🌐 Starting Cloudflare TCP Tunnel for port {local_port}...[/]\n"
        "[yellow]This will expose your local ADB bridge to the global internet.\n"
        "Press Ctrl+C to stop the tunnel when finished.[/]",
        border_style="cyan"
    ))

    try:
        # Run cloudflared quick tunnel for TCP
        cmd = ["cloudflared", "tunnel", "--url", f"tcp://localhost:{local_port}"]
        process = subprocess.Popen(cmd)
        process.wait()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠ Cloudflare tunnel closed.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to start tunnel:[/] {e}")