"""
Aadi — Keystore & Sensitive Data Extractor
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def dump_app_data(device_id: str, package_name: str, output_dir: str = "./dumped_data"):
    """Extract private app data, databases, and shared prefs from rooted device."""
    console.print(Panel(f"[cyan]Extracting private data for {package_name}...[/]", border_style="magenta"))
    try:
        subprocess.run(["adb", "-s", device_id, "root"], capture_output=True)
        remote_path = f"/data/data/{package_name}/"
        os.makedirs(output_dir, exist_ok=True)

        cmd = ["adb", "-s", device_id, "pull", remote_path, output_dir]
        res = subprocess.run(cmd, capture_output=True, text=True)

        if res.returncode == 0:
            console.print(f"[bold green]✓ Successfully pulled app private data to {output_dir}/{package_name}[/]")
        else:
            console.print(f"[bold red]✗ Pull failed: {res.stderr.strip()}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Error during data extraction: {e}[/]")