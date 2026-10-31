"""
Aadi — Automated APK Decompiler & Patcher (Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
from typing import Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


def decompile_apk(apk_path: str) -> Optional[str]:
    """Decompile APK using apktool with a dynamic output directory and robust error handling."""
    if not apk_path or not os.path.exists(apk_path):
        console.print(f"[bold red]✗ APK not found or invalid path: {apk_path}[/]")
        return None

    base_name = os.path.splitext(os.path.basename(apk_path))[0]
    output_dir = f"decoded_{base_name}"

    console.print(Panel(f"[cyan]Decompiling {os.path.basename(apk_path)} into '{output_dir}' using apktool...[/]",
                        border_style="magenta"))

    try:
        cmd = ["apktool", "d", apk_path, "-o", output_dir, "-f"]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        console.print(f"[bold green]✓ APK decompiled successfully into '{output_dir}'.[/]")
        console.print(
            f"[yellow][*] Inspect Smali/Manifest in '{output_dir}' and rebuild using: [bold]apktool b {output_dir}[/][/]"
        )
        return output_dir
    except FileNotFoundError:
        console.print("[bold red]✗ 'apktool' not found in system PATH. Please install it first.[/]")
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() if e.stderr else f"Exit code {e.returncode}"
        console.print(f"[bold red]✗ Apktool execution failed: {err_msg}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Decompilation failed: {e}[/]")

    return None


def decompile_and_patch_apk(apk_path: str) -> Optional[str]:
    """Wrapper function to match main menu integration for decompilation and patching workflow."""
    return decompile_apk(apk_path)


def recompile_apk(output_dir: str, reconstructed_apk_name: str = "patched_output.apk") -> bool:
    """Rebuild the modified directory back into an APK file using apktool."""
    if not output_dir or not os.path.exists(output_dir):
        console.print(f"[bold red]✗ Directory not found or invalid: {output_dir}[/]")
        return False

    console.print(Panel(f"[cyan]Rebuilding APK from '{output_dir}'...[/]", border_style="magenta"))

    try:
        build_cmd = ["apktool", "b", output_dir, "-o", reconstructed_apk_name]
        subprocess.run(build_cmd, check=True, capture_output=True, text=True)
        console.print(f"[bold green]✓ APK recompiled successfully: {reconstructed_apk_name}[/]")
        console.print(
            "[yellow][!] Note: The recompiled APK must be signed (e.g., using uber-apk-signer or jarsigner) before installation on a physical device.[/]")
        return True
    except FileNotFoundError:
        console.print("[bold red]✗ 'apktool' not found in system PATH.[/]")
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() if e.stderr else f"Exit code {e.returncode}"
        console.print(f"[bold red]✗ Recompilation failed: {err_msg}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Recompilation failed: {e}[/]")

    return False