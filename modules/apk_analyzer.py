"""
Aadi — APK Static Analyzer Module (Optimized & Expanded)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import zipfile
import os
import re
import hashlib
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

DANGEROUS_PERMS = {
    "android.permission.READ_CONTACTS": "HIGH",
    "android.permission.WRITE_CONTACTS": "HIGH",
    "android.permission.READ_SMS": "HIGH",
    "android.permission.SEND_SMS": "HIGH",
    "android.permission.RECEIVE_SMS": "HIGH",
    "android.permission.READ_CALL_LOG": "HIGH",
    "android.permission.WRITE_CALL_LOG": "HIGH",
    "android.permission.RECORD_AUDIO": "HIGH",
    "android.permission.CAMERA": "MEDIUM",
    "android.permission.ACCESS_FINE_LOCATION": "HIGH",
    "android.permission.ACCESS_COARSE_LOCATION": "MEDIUM",
    "android.permission.READ_EXTERNAL_STORAGE": "MEDIUM",
    "android.permission.WRITE_EXTERNAL_STORAGE": "MEDIUM",
    "android.permission.PROCESS_OUTGOING_CALLS": "HIGH",
    "android.permission.INTERNET": "LOW",
    "android.permission.CHANGE_WIFI_STATE": "MEDIUM",
    "android.permission.BLUETOOTH": "LOW",
    "android.permission.NFC": "LOW",
    "android.permission.GET_ACCOUNTS": "MEDIUM",
    "android.permission.USE_CREDENTIALS": "HIGH",
    "android.permission.READ_PHONE_STATE": "HIGH",
    "android.permission.CALL_PHONE": "HIGH",
    "android.permission.RECEIVE_BOOT_COMPLETED": "MEDIUM",
    "android.permission.SYSTEM_ALERT_WINDOW": "HIGH",
    "android.permission.INSTALL_PACKAGES": "CRITICAL",
    "android.permission.DELETE_PACKAGES": "CRITICAL",
    "android.permission.BIND_DEVICE_ADMIN": "CRITICAL",
    "android.permission.MOUNT_UNMOUNT_FILESYSTEMS": "HIGH",
    "android.permission.MASTER_CLEAR": "CRITICAL",
}

SECRET_PATTERNS = [
    (r"(?i)(api_?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-]{16,})", "API Key"),
    (r"(?i)(secret|password|passwd|pwd)\s*[=:]\s*['\"]?(\S{8,})", "Secret/Password"),
    (r"(?i)(access_?token|auth_?token)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})", "Auth Token"),
    (r"(?i)(aws_?access_?key_?id)\s*[=:]\s*['\"]?(AKIA[0-9A-Z]{16})", "AWS Access Key"),
    (r"(?i)(aws_?secret)\s*[=:]\s*['\"]?([a-zA-Z0-9/+=]{40})", "AWS Secret"),
    (r"(?i)(BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY)", "Private Key"),
    (r"(?i)(client_?id|client_?secret)\s*[=:]\s*['\"]?(\S{8,})", "OAuth Credential"),
    (r"(?i)(firebase[a-zA-Z_]*)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})", "Firebase Config"),
    (r"(?i)google_maps_key\s*[=:]\s*['\"]?(AIza[0-9A-Za-z\-_]{35})", "Google Maps Key"),
    (r"(?i)(jdbc:[a-z]+://\S+)", "Database URL"),
    (r"https?://(?:\S+:)?\S+@[\w\.\-]+", "URL with Credentials"),
]


def _file_hash(path: str) -> dict:
    """Compute MD5, SHA1, and SHA256 hashes of the APK file."""
    result = {}
    try:
        for algo in ["md5", "sha1", "sha256"]:
            h = hashlib.new(algo)
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            result[algo.upper()] = h.hexdigned() if hasattr(h, 'hexdigned') else h.hexdigest()
    except Exception as e:
        console.print(f"[yellow]⚠ Error computing hashes: {e}[/]")
    return result


def analyze_apk(apk_path: str) -> dict:
    """Perform static analysis on the target APK file."""
    findings = {
        "path": apk_path,
        "hashes": {},
        "manifest": {},
        "permissions": [],
        "dangerous_permissions": [],
        "exported_components": {"activities": [], "services": [], "receivers": [], "providers": []},
        "secrets": [],
        "urls": [],
        "ips": [],
        "libs": [],
        "obfuscated": False,
        "backup_enabled": False,
        "debuggable": False,
        "network_security_config": False,
        "vulnerabilities": [],
    }

    if not os.path.isfile(apk_path):
        console.print(f"[bold red]✗ File not found: {apk_path}[/]")
        return findings

    console.print(Panel(f"[bold cyan]Analyzing APK:[/] {apk_path}", border_style="magenta"))

    with console.status("[cyan]Computing file hashes...[/]"):
        findings["hashes"] = _file_hash(apk_path)

    try:
        with zipfile.ZipFile(apk_path, "r") as zf:
            namelist = zf.namelist()
            console.print(f"[dim]APK contains [bold]{len(namelist)}[/] entries.[/]")

            # Check for native libraries (.so files)
            libs = [name for name in namelist if name.startswith("lib/")]
            findings["libs"] = list(set([lib.split('/')[1] for lib in libs if len(lib.split('/')) > 1]))

            if findings["libs"]:
                console.print(f"[green]✓ Native Libraries detected:[/] {', '.join(findings['libs'])}")

            # Check if AndroidManifest.xml exists (Note: It is binary XML inside APK)
            if "AndroidManifest.xml" in namelist:
                console.print("[green]✓ AndroidManifest.xml found in archive.[/]")
            else:
                console.print(
                    "[yellow]⚠ AndroidManifest.xml not found directly in root (might be packaged differently).[/]")

    except zipfile.BadZipFile:
        console.print("[bold red]✗ Not a valid APK (ZIP) file.[/]")
        return findings
    except Exception as e:
        console.print(f"[bold red]✗ Error processing APK zip structure: {e}[/]")
        return findings

    console.print("[green]✓ Static analysis framework ready.[/]")
    return findings