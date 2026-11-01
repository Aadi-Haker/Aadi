"""
Aadi — Progress & Background Task Helper
Author: Aaditya Kumar Pandey
"""

import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

def run_with_progress(task_description: str, task_func, *args, **kwargs):
    """किसी भी लंबे टास्क को एनिमेटेड प्रोग्रेस बार के साथ चलाता है।"""
    result = None
    with Progress(
        SpinnerColumn(spinner_name="dots", style="magenta"),
        TextColumn("[bold cyan]{task.description}[/]", justify="right"),
        BarColumn(bar_width=40, style="cyan", complete_style="green"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]{task_description}...", total=None)
        try:
            result = task_func(*args, **kwargs)
            progress.update(task, completed=100)
        except Exception as e:
            console.print(f"[bold red]✗ Task failed:[/] {e}")
        time.sleep(0.3)
    return result