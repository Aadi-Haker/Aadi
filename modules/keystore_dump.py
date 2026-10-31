"""
Aadi — Keystore & Sensitive Data Extractor (Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
import time
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


def _run_adb(args: List[str], device_id: Optional[str] = None, capture: bool = True) -> Tuple[str, str, int]:
    """Helper function to execute ADB commands safely with timeout and error handling."""
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        res = subprocess.run(cmd, capture_output=capture, text=True, timeout=30)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Process timed out", -2
    except Exception as e:
        return "", str(e), -1


def dump_app_data(device_id: Optional[str], package_name: str, output_dir: str = "./dumped_data") -> bool:
    """Extract private app data, databases, and shared prefs from rooted device with fallback verification."""
    if not device_id:
        console.print("[bold red]✗ No device selected or Device ID is missing![/]")
        return False

    if not package_name or not package_name.strip():
        console.print("[bold red]✗ Package Name is missing or invalid![/]")
        return False

    console.print(Panel(
        f"[cyan]Target Package:[/] [bold magenta]{package_name}[/]\n"
        f"[cyan]Destination:[/] [white]{output_dir}[/]",
        title="[bold cyan]📦 AADI Sensitive Data Extractor[/]",
        border_style="magenta"
    ))

    # Attempt to restart adb in root mode
    console.print("[cyan]Requesting ADB root privileges...[/]")
    _, err, rc = _run_adb(["root"], device_id)
    time.sleep(1)  # Give adb daemon a moment to restart

    remote_path = f"/data/data/{package_name}/"
    pkg_output_dir = os.path.join(output_dir, package_name)
    os.makedirs(pkg_output_dir, exist_ok=True)

    console.print(f"[cyan]Pulling private files from {remote_path}...[/]")
    out, err, rc = _run_adb(["pull", remote_path, pkg_output_dir], device_id)

    if rc == 0:
        console.print(f"[bold green]✓ Successfully pulled app private data to:[/] [bold cyan]{pkg_output_dir}[/]")

        # Quick summary of pulled contents
        try:
            pulled_files = []
            for root, dirs, files in os.walk(pkg_output_dir):
                for file in files:
                    pulled_files.append(file)
            console.print(f"[green]ℹ Total files/databases extracted: [bold]{len(pulled_files)}[/][/]")
        except Exception:
            pass

        return True
    else:
        console.print(f"[bold red]✗ Pull failed. Device may lack root access or package path is invalid.[/]")
        if err:
            console.print(f"[dim red]Error details: {err}[/]")
        return False