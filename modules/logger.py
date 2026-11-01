"""
Aadi — Global Error Logger Module
Author: Aaditya Kumar Pandey
"""

import os
import traceback
import sys
from datetime import datetime
from rich.console import Console

console = Console()


def setup_global_logger():
    os.makedirs("loot", exist_ok=True)
    log_path = os.path.join("loot", "aadi_error.log")

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n[{timestamp}] UNHANDLED EXCEPTION:\n{error_msg}\n" + "=" * 50 + "\n")
        except Exception:
            pass

        console.print(f"\n[bold red]✗ An unexpected error occurred. Details saved to:[/] [cyan]{log_path}[/]")

    sys.excepthook = handle_exception