"""
AADI — Cloud Tunnel & Port Forwarding Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import shutil
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

console = Console()


def start_cloud_tunnel():
    """Expose local ports (like RAT listener or web dashboard) to the internet securely."""
    console.rule("[bold magenta]🌐 Cloud Tunnel & Port Forwarding Manager[/]")

    port = IntPrompt.ask("[cyan]Enter local port to forward (e.g., RAT listener port 4444)[/]", default=4444)

    tunnel_type = Prompt.ask(
        "[cyan]Select tunneling tool[/]",
        choices=["cloudflared", "ngrok", "localhost.run"],
        default="cloudflared"
    )

    if tunnel_type == "cloudflared":
        if not shutil.which("cloudflared"):
            console.print("[bold red]cloudflared not found.[/] Please install it via manual binary download.")
            return

        console.print(f"[green]Starting secure Cloudflare tunnel for port {port}...[/]")
        console.print("[yellow]Note: Look at the generated *.trycloudflare.com URL in the output below and copy it.[/]")
        console.print("[dim]Press Ctrl+C to stop the tunnel session.[/]\n")

        try:
            # क्लाउडफ्लेयर टनल कमांड को सही तरीके से एक्जीक्यूट करना
            subprocess.run(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"])
        except KeyboardInterrupt:
            console.print("\n[yellow]Cloudflare tunnel closed.[/]")

    elif tunnel_type == "ngrok":
        if not shutil.which("ngrok"):
            console.print("[bold red]ngrok not found.[/] Please install ngrok and configure your auth token.")
            return

        proto = Prompt.ask("[cyan]Select protocol[/]", choices=["tcp", "http"], default="tcp")
        console.print(f"[green]Starting ngrok {proto.upper()} tunnel for port {port}...[/]")
        try:
            if proto == "tcp":
                subprocess.run(["ngrok", "tcp", str(port)])
            else:
                subprocess.run(["ngrok", "http", str(port)])
        except KeyboardInterrupt:
            console.print("\n[yellow]Ngrok tunnel closed.[/]")

    elif tunnel_type == "localhost.run":
        console.print(f"[green]Connecting to localhost.run SSH tunnel for port {port}...[/]")
        try:
            subprocess.run(["ssh", "-R", f"80:localhost:{port}", "nokey@localhost.run"])
        except KeyboardInterrupt:
            console.print("\n[yellow]SSH tunnel closed.[/]")