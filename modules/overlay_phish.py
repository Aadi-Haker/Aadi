"""
Aadi — Fake Login Phishing & Overlay Attack Module (Enhanced, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import time
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


def _run_adb(args: List[str], device_id: Optional[str] = None) -> Tuple[str, str, int]:
    """Helper function to execute ADB commands safely with timeout and error handling."""
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Process timed out", -2
    except Exception as e:
        return "", str(e), -1


def deploy_overlay_payload(device_id: Optional[str], target_package: str, main_activity: str = "") -> bool:
    """Simulate overlay attack deployment and launch target application to capture interface focus."""
    if not target_package or not target_package.strip():
        console.print("[bold red]✗ Target package name is required and cannot be empty![/]")
        return False

    console.print(Panel(
        f"[cyan]Target Package:[/] [bold magenta]{target_package}[/]\n"
        "[white]Initializing transparent overlay window simulation...[/]\n"
        "[yellow]⚠ Requirement: Target context must possess 'SYSTEM_ALERT_WINDOW' permission.[/]",
        title="[bold red]🎭 AADI Overlay Phishing Engine[/]",
        border_style="magenta"
    ))

    # Check if target package is installed
    console.print("[cyan][*] Verifying target package installation on device...[/]")
    out, _, rc = _run_adb(["shell", "pm", "path", target_package], device_id)
    if rc != 0 or not out:
        console.print(f"[bold yellow]⚠ Warning: Package '{target_package}' not found on connected device.[/]")
    else:
        console.print(f"[green]✓ Target package verified on device.[/]")

    # If main activity is provided, launch it to bring it to foreground
    if main_activity and main_activity.strip():
        component = f"{target_package}/{main_activity}" if not main_activity.startswith(".") else f"{target_package}{main_activity}"
        console.print(f"[cyan][*] Bringing target activity to foreground: {component}[/]")
        _, err, launch_rc = _run_adb(["shell", "am", "start", "-n", component], device_id)
        if launch_rc == 0:
            console.print("[bold green]✓ Target application brought to foreground successfully.[/]")
        else:
            console.print(f"[dim red]Could not auto-launch activity: {err}[/]")

    console.print(Panel(
        "[bold green]✓ Overlay attack payload structure initialized successfully![/]\n"
        "[white]Tip: In a full attack chain, a background service draws an un-touch-transparent "
        "or fake login view over the target window to harvest user inputs.[/]",
        border_style="green"
    ))
    return True