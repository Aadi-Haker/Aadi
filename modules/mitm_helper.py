"""
Aadi — One-Click MITM Proxy & Certificate Installer (Optimized, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import shutil
import subprocess
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


def _run_adb(args: List[str], device_id: Optional[str] = None, capture: bool = True) -> Tuple[str, str, int]:
    """Helper function to execute ADB commands safely with timeout and error handling."""
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        res = subprocess.run(cmd, capture_output=capture, text=True, timeout=15)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Process timed out", -2
    except Exception as e:
        return "", str(e), -1


def install_system_cert(device_id: str, cert_path: str) -> bool:
    """Push Burp/Mitmproxy cert to Android system trust store (/system/etc/security/cacerts/)."""
    if not device_id:
        console.print("[bold red]✗ No device selected. Please connect a device first.[/]")
        return False

    if not cert_path or not os.path.exists(cert_path):
        console.print(f"[bold red]✗ Certificate file not found or invalid path:[/] {cert_path}")
        return False

    # Check for OpenSSL dependency
    if not shutil.which("openssl"):
        console.print("[bold red]✗ 'openssl' is not installed on your host machine.[/]")
        console.print("[dim]Install it via: sudo apt install openssl (Linux) or brew install openssl (Mac)[/]")
        return False

    console.print(Panel(
        "[bold yellow]⚠ System Certificate Installation Notice[/]\n"
        "[white]1. Target device must be rooted (Magisk recommended).\n"
        "2. Modern Android versions may require Magisk modules (e.g., 'Move Certificates') "
        "if the /system partition is read-only (dm-verity).[/]",
        title="[bold cyan]🔒 MITM Trust Store Installer[/]",
        border_style="yellow"
    ))

    if not Confirm.ask("[cyan]Do you wish to proceed with system certificate installation?[/]", default=True):
        console.print("[yellow][-] Installation cancelled by user.[/]")
        return False

    try:
        console.print("[cyan][*] Requesting ADB root access and remount...[/]")
        _run_adb(["root"], device_id)
        _, _, remount_rc = _run_adb(["remount"], device_id)

        if remount_rc != 0:
            console.print("[yellow]⚠ Standard 'adb remount' failed. /system partition may be protected.[/]")
            console.print("[dim]Tip: Ensure Magisk is active or use a custom overlayfs/recovery.[/]")

        # Calculate certificate hash required by Android (subject_hash_old)
        console.print("[cyan][*] Calculating Android certificate hash filename...[/]")
        openssl_cmd = ["openssl", "x509", "-inform", "PEM", "-subject_hash_old", "-in", cert_path]
        res = subprocess.run(openssl_cmd, capture_output=True, text=True)

        if res.returncode != 0 or not res.stdout.strip():
            err_msg = res.stderr.strip() if res.stderr else "Unknown OpenSSL error"
            console.print(f"[bold red]✗ Failed to calculate certificate hash using OpenSSL:[/] {err_msg}")
            return False

        cert_hash = res.stdout.strip().split("\n")[0]
        target_name = f"{cert_hash}.0"
        console.print(f"[green]✓ Calculated hash filename:[/] [bold cyan]{target_name}[/]")

        # Push to temporary sdcard location then move to system cacerts
        console.print("[cyan][*] Pushing certificate to device storage...[/]")
        _, _, push_rc = _run_adb(["push", cert_path, f"/sdcard/{target_name}"], device_id)
        if push_rc != 0:
            console.print("[bold red]✗ Failed to push certificate to device sdcard.[/]")
            return False

        console.print("[cyan][*] Moving certificate into system trust store...[/]")
        move_cmd = ["shell", f"mv /sdcard/{target_name} /system/etc/security/cacerts/{target_name}"]
        _, move_err, move_rc = _run_adb(move_cmd, device_id)

        if move_rc != 0:
            console.print(f"[bold red]✗ Failed to move certificate to /system/etc/security/cacerts/:[/] {move_err}")
            # Cleanup temp file on failure
            _run_adb(["shell", f"rm -f /sdcard/{target_name}"], device_id)
            return False

        # Set strict permissions (chmod 644)
        chmod_cmd = ["shell", f"chmod 644 /system/etc/security/cacerts/{target_name}"]
        _run_adb(chmod_cmd, device_id)

        console.print(Panel(
            f"[bold green]✓ Certificate successfully installed as:[/] /system/etc/security/cacerts/{target_name}\n"
            "[yellow][*] Please reboot your target device or restart target applications for changes to take effect.[/]",
            border_style="green"
        ))
        return True

    except Exception as e:
        console.print(f"[bold red]✗ An unexpected error occurred during installation:[/] {e}")
        return False


def configure_proxy(device_id: str, proxy_host: str, proxy_port: str) -> bool:
    """Configure global HTTP proxy on target Android device."""
    if not device_id:
        console.print("[bold red]✗ No device selected.[/]")
        return False

    if not proxy_host or not proxy_port:
        console.print("[bold red]✗ Proxy host and port cannot be empty.[/]")
        return False

    proxy_str = f"{proxy_host}:{proxy_port}"
    console.print(f"[cyan]Setting global proxy to {proxy_str} on device {device_id}...[/]")

    _, err, rc = _run_adb(["shell", "settings", "put", "global", "http_proxy", proxy_str], device_id)
    if rc == 0:
        console.print(f"[bold green]✓ Global proxy successfully set to:[/] [bold cyan]{proxy_str}[/]")
        return True
    else:
        console.print(f"[bold red]✗ Failed to configure proxy:[/] {err}")
        return False


def clear_proxy(device_id: str) -> bool:
    """Remove global HTTP proxy configuration."""
    if not device_id:
        console.print("[bold red]✗ No device selected.[/]")
        return False

    console.print("[cyan]Clearing global HTTP proxy settings...[/]")
    _, err, rc = _run_adb(["shell", "settings", "put", "global", "http_proxy", ":0"], device_id)

    if rc == 0:
        console.print("[bold green]✓ Global proxy cleared successfully.[/]")
        return True
    else:
        console.print(f"[bold red]✗ Failed to clear proxy:[/] {err}")
        return False