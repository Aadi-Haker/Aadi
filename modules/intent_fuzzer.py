"""
Aadi — Advanced Intent & Deep-Link Fuzzer
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()


def fuzz_exported_activities(device_id: str, package_name: str, activity_list: list):
    """Fuzz exported activities using random or malicious intent actions/extras."""
    console.print(Panel(f"[cyan]Fuzzing exported activities for package: {package_name}[/]", border_style="magenta"))

    payload_actions = [
        "android.intent.action.VIEW",
        "android.intent.action.MAIN",
        "com.malicious.action.TEST"
    ]

    for act in activity_list:
        for actn in payload_actions:
            cmd = ["adb", "-s", device_id, "shell", "am", "start", "-a", actn, "-n", f"{package_name}/{act}"]
            console.print(f"[dim]Executing: {' '.join(cmd)}[/]")
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                if "Error" in res.stderr or "Exception" in res.stderr:
                    console.print(f"[bold yellow][!] Potential crash or error on {act} with action {actn}[/]")
            except Exception:
                pass
    console.print("[bold green]✓ Intent fuzzing sequence completed.[/]")