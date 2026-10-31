"""
Aadi — Live Screen Streaming & Remote Control Helper (HD Version, Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import shutil
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel

console = Console()


def start_screen_stream(device_id: Optional[str] = None) -> None:
    """Launch scrcpy with high-definition settings for crystal-clear live mirroring & control."""
    console.print(Panel("[cyan]Launching High-Definition Live Screen Mirroring...[/]", border_style="magenta"))

    # Check if scrcpy is installed before executing
    if not shutil.which("scrcpy"):
        console.print("[bold red]✗ 'scrcpy' is not installed or not found in system PATH.[/]")
        console.print(
            "[yellow][*] Tip: Install it using `sudo apt install scrcpy` (Linux) or `winget install scrcpy` (Windows).[/]")
        return

    try:
        # Constructing scrcpy command dynamically
        cmd: List[str] = ["scrcpy"]
        if device_id:
            cmd.extend(["-s", device_id])

        cmd.extend(["--max-size=1920", "-b", "8M", "--max-fps=60"])

        console.print("[yellow][*] Starting HD stream window. Close the video window to return to AADI.[/]")
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ scrcpy process exited with error code {e.returncode}.[/]")
    except KeyboardInterrupt:
        console.print("\n[yellow][*] Screen streaming session terminated by user.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Error starting screen stream: {e}[/]")