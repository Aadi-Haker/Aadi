"""
Aadi — System Health Doctor & Dependency Checker
Author: Aaditya Kumar Pandey
"""

import shutil
import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def check_system_health() -> bool:
    console.rule("[bold magenta]🩺 AADI System Health & Dependency Doctor[/]")

    tools = {
        "apktool": "Required for APK decompilation & recompilation",
        "apksigner": "Required for cryptographic APK signing",
        "adb": "Required for Android Debug Bridge device management",
        "scrcpy": "Required for live screen streaming & remote control",
        "msfvenom": "Required for payload generation"
    }

    table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold cyan")
    table.add_column("Dependency", style="bold white")
    table.add_column("Status", style="green")
    table.add_column("Purpose", style="dim")

    all_passed = True
    for tool, desc in tools.items():
        if shutil.which(tool):
            table.add_row(tool, "[bold green]✓ Installed[/]", desc)
        else:
            table.add_row(tool, "[bold yellow]⚠ Missing (Optional/Required)[/]", desc)
            # चाहें तो यहाँ critical tools के लिए all_passed = False कर सकते हैं

    console.print(table)
    return all_passed