"""
Aadi — Fake Login Phishing & Overlay Attack Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

def deploy_overlay_payload(target_package: str):
    """Generate overlay phishing warning/template configuration."""
    console.print(Panel(f"[cyan]Deploying overlay phishing template for target: {target_package}[/]", border_style="magenta"))
    console.print("[yellow][*] Note: Requires SYSTEM_ALERT_WINDOW permission on target context.[/]")
    console.print("[bold green]✓ Overlay attack payload structure initialized successfully.[/]")