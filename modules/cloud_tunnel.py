"""
Aadi — Cloud Tunnel & Port Forwarding Module (Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import shutil
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

console = Console()


def start_cloud_tunnel(port: Optional[int] = None) -> None:
    """Expose local ports (like RAT listener or web dashboard) to the internet securely with robust error handling."""
    console.rule("[bold magenta]🌐 Cloud Tunnel & Port Forwarding Manager[/]")

    # यदि बाहर से पोर्ट पास नहीं किया गया है, तो यूजर से पूछें
    if port is None:
        port = IntPrompt.ask("[cyan]Enter local port to forward (e.g., RAT listener port 4444)[/]", default=4444)

    if not (1 <= port <= 65535):
        console.print("[bold red]✗ Invalid port number. Must be between 1 and 65535.[/]")
        return

    tunnel_type = Prompt.ask(
        "[cyan]Select tunneling tool[/]",
        choices=["cloudflared", "ngrok", "localhost.run"],
        default="cloudflared"
    )

    try:
        if tunnel_type == "cloudflared":
            if not shutil.which("cloudflared"):
                console.print("[bold red]✗ 'cloudflared' not found.[/] Please install it via manual binary download.")
                return

            console.print(f"[green]Starting secure Cloudflare tunnel for port {port}...[/]")
            console.print("[yellow]Note: Look at the generated *.trycloudflare.com URL in the output below and copy it.[/]")
            console.print("[dim]Press Ctrl+C to stop the tunnel session.[/]\n")

            subprocess.run(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"], check=True)

        elif tunnel_type == "ngrok":
            if not shutil.which("ngrok"):
                console.print("[bold red]✗ 'ngrok' not found.[/] Please install ngrok and configure your auth token.")
                return

            proto = Prompt.ask("[cyan]Select protocol[/]", choices=["tcp", "http"], default="tcp")
            console.print(f"[green]Starting ngrok {proto.upper()} tunnel for port {port}...[/]")

            if proto == "tcp":
                subprocess.run(["ngrok", "tcp", str(port)], check=True)
            else:
                subprocess.run(["ngrok", "http", str(port)], check=True)

        elif tunnel_type == "localhost.run":
            if not shutil.which("ssh"):
                console.print("[bold red]✗ 'ssh' client not found.[/] OpenSSH client is required for localhost.run tunnels.")
                return

            console.print(f"[green]Connecting to localhost.run SSH tunnel for port {port}...[/]")
            console.print("[dim]Press Ctrl+C to stop the tunnel session.[/]\n")

            subprocess.run(["ssh", "-R", f"80:localhost:{port}", "nokey@localhost.run"], check=True)

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Tunnel session closed by user.[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"\n[bold red]✗ Tunnel process exited with error code {e.returncode}.[/]")
    except Exception as e:
        console.print(f"\n[bold red]✗ Unexpected error during tunneling: {e}[/]")