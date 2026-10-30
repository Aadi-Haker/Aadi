"""
Aadi — Automated APK Decompiler & Patcher
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def decompile_and_patch_apk(apk_path: str):
    """Decompile APK using apktool for smali inspection and patching."""
    if not os.path.exists(apk_path):
        console.print(f"[bold red]✗ APK not found: {apk_path}[/]")
        return

    console.print(Panel(f"[cyan]Decompiling {os.path.basename(apk_path)} using apktool...[/]", border_style="magenta"))
    try:
        subprocess.run(["apktool", "d", apk_path, "-o", "decoded_apk"], check=True)
        console.print("[bold green]✓ APK decompiled successfully into './decoded_apk'.[/]")
        console.print(
            "[yellow][*] You can now inject custom smali hooks or recompile using 'apktool b decoded_apk'.[/]")
    except FileNotFoundError:
        console.print("[bold red]✗ 'apktool' not found in system PATH.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Decompilation failed: {e}[/]")