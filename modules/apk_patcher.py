"""
Aadi — Automated APK Decompiler & Patcher (Optimized)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def decompile_apk(apk_path: str) -> str:
    """Decompile APK using apktool with a dynamic output directory."""
    if not os.path.exists(apk_path):
        console.print(f"[bold red]✗ APK not found: {apk_path}[/]")
        return None

    base_name = os.path.splitext(os.path.basename(apk_path))[0]
    output_dir = f"decoded_{base_name}"

    console.print(Panel(f"[cyan]Decompiling {os.path.basename(apk_path)} into '{output_dir}' using apktool...[/]",
                        border_style="magenta"))

    try:
        # If directory already exists, apktool might prompt or fail unless forced
        cmd = ["apktool", "d", apk_path, "-o", output_dir, "-f"]
        subprocess.run(cmd, check=True)

        console.print(f"[bold green]✓ APK decompiled successfully into '{output_dir}'.[/]")
        console.print(
            f"[yellow][*] Inspect Smali/Manifest in '{output_dir}' and rebuild using: [bold]apktool b {output_dir}[/][/]"
        )
        return output_dir
    except FileNotFoundError:
        console.print("[bold red]✗ 'apktool' not found in system PATH. Please install it first.[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Apktool execution failed with error code {e.returncode}.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Decompilation failed: {e}[/]")

    return None


def recompile_apk(output_dir: str, reconstructed_apk_name: str = "patched_output.apk"):
    """Rebuild the modified directory back into an APK file using apktool."""
    if not os.path.exists(output_dir):
        console.print(f"[bold red]✗ Directory not found: {output_dir}[/]")
        return False

    console.print(Panel(f"[cyan]Rebuilding APK from '{output_dir}'...[/]", border_style="magenta"))

    try:
        build_cmd = ["apktool", "b", output_dir, "-o", reconstructed_apk_name]
        subprocess.run(build_cmd, check=True)
        console.print(f"[bold green]✓ APK recompiled successfully: {reconstructed_apk_name}[/]")
        console.print(
            "[yellow][!] Note: The recompiled APK must be signed before installation on a physical device.[/]")
        return True
    except FileNotFoundError:
        console.print("[bold red]✗ 'apktool' not found in system PATH.[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Recompilation failed with error code {e.returncode}.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Recompilation failed: {e}[/]")

    return False