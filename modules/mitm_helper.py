"""
Aadi — One-Click MITM Proxy & Certificate Installer
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


def install_system_cert(device_id: str, cert_path: str):
    """Push Burp/Mitmproxy cert to Android system trust store (/system/etc/security/cacerts/)."""
    if not os.path.exists(cert_path):
        console.print(f"[bold red]✗ Certificate file not found:[/] {cert_path}")
        return

    console.print(
        Panel("[yellow]⚠ Note: Device must be rooted and remounted as read-write (`adb root; adb remount`).[/]",
              border_style="yellow"))

    if not Confirm.ask("[cyan]Proceed with system certificate installation?[/]", default=True):
        return

    try:
        # ADB root & remount
        subprocess.run(["adb", "-s", device_id, "root"], capture_output=True)
        subprocess.run(["adb", "-s", device_id, "remount"], capture_output=True)

        # Hash certificate name required by Android (openssl x509 -subject_hash_old -in cert.pem)
        res = subprocess.run(["openssl", "x509", "-inform", "PEM", "-subject_hash_old", "-in", cert_path],
                             capture_output=True, text=True)
        cert_hash = res.stdout.strip().split("\n")[0]
        target_name = f"{cert_hash}.0"

        console.print(f"[cyan][*] Calculated Android cert hash filename:[/] {target_name}")

        # Push to temp then move to cacerts
        subprocess.run(["adb", "-s", device_id, "push", cert_path, f"/sdcard/{target_name}"], check=True)
        subprocess.run(
            ["adb", "-s", device_id, "shell", f"mv /sdcard/{target_name} /system/etc/security/cacerts/{target_name}"],
            check=True)
        subprocess.run(["adb", "-s", device_id, "shell", f"chmod 644 /system/etc/security/cacerts/{target_name}"],
                       check=True)

        console.print(f"[bold green]✓ Certificate successfully installed to system store as {target_name}![/]")
        console.print("[yellow][*] Please restart your target device or application for changes to take effect.[/]")

    except Exception as e:
        console.print(f"[bold red]✗ Failed to install system certificate:[/] {e}")


def configure_proxy(device_id: str, proxy_host: str, proxy_port: str):
    """Configure global HTTP proxy on target Android device."""
    proxy_str = f"{proxy_host}:{proxy_port}"
    try:
        subprocess.run(["adb", "-s", device_id, "shell", "settings", "put", "global", "http_proxy", proxy_str],
                       check=True)
        console.print(f"[bold green]✓ Global proxy successfully set to {proxy_str}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to set proxy:[/] {e}")


def clear_proxy(device_id: str):
    """Remove global HTTP proxy configuration."""
    try:
        subprocess.run(["adb", "-s", device_id, "shell", "settings", "put", "global", "http_proxy", ":0"], check=True)
        console.print("[bold green]✓ Global proxy cleared successfully.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to clear proxy:[/] {e}")