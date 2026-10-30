"""
Aadi — Live Screen Streaming & Remote Control Helper (HD Version)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()


# def start_screen_stream(device_id: str):
#     """Launch scrcpy with high-definition settings for crystal-clear live mirroring & control."""
#     console.print(Panel("[cyan]Launching High-Definition Live Screen Mirroring...[/]", border_style="magenta"))
#     try:
#         # High-quality scrcpy arguments:
#         # --max-size=1920 -> Full HD Resolution
#         # --bit-rate=8M   -> High Bitrate for crisp graphics & zero pixelation
#         # --max-fps=60    -> Smooth 60 FPS motion
#
#         if device_id:
#             cmd = ["scrcpy", "-s", device_id, "--max-size=1920", "--bit-rate=8M", "--max-fps=60"]
#         else:
#             cmd = ["scrcpy", "--max-size=1920", "--bit-rate=8M", "--max-fps=60"]
#
#         console.print("[yellow][*] Starting HD stream window. Close the video window to return to AADI.[/]")
#         subprocess.run(cmd)
#
#     except FileNotFoundError:
#         console.print("[bold red]✗ 'scrcpy' is not installed or not found in system PATH.[/]")
#         console.print(
#             "[yellow][*] Tip: Install it using `sudo apt install scrcpy` (Linux) or `winget install scrcpy` (Windows).[/]")
#     except Exception as e:
#         console.print(f"[bold red]✗ Error starting screen stream: {e}[/]")


def start_screen_stream(device_id: str):
    """Launch scrcpy with high-definition settings for crystal-clear live mirroring & control."""
    console.print(Panel("[cyan]Launching High-Definition Live Screen Mirroring...[/]", border_style="magenta"))
    try:
        # यहाँ '--bit-rate=8M' की जगह '-b 8M' का उपयोग करें
        if device_id:
            cmd = ["scrcpy", "-s", device_id, "--max-size=1920", "-b", "8M", "--max-fps=60"]
        else:
            cmd = ["scrcpy", "--max-size=1920", "-b", "8M", "--max-fps=60"]

        console.print("[yellow][*] Starting HD stream window. Close the video window to return to AADI.[/]")
        subprocess.run(cmd)

    except FileNotFoundError:
        console.print("[bold red]✗ 'scrcpy' is not installed or not found in system PATH.[/] [[cite: 1]]")
    except Exception as e:
        console.print(f"[bold red]✗ Error starting screen stream: {e}[/]")