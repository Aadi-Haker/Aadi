"""
Aadi — APK Static Analyzer Module
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
    "android.permission.READ_CONTACTS":          "HIGH",
    "android.permission.WRITE_CONTACTS":         "HIGH",
    "android.permission.READ_SMS":               "HIGH",
    "android.permission.SEND_SMS":               "HIGH",
    "android.permission.RECEIVE_SMS":            "HIGH",
    "android.permission.READ_CALL_LOG":          "HIGH",
    "android.permission.WRITE_CALL_LOG":         "HIGH",
    "android.permission.RECORD_AUDIO":           "HIGH",
    "android.permission.CAMERA":                 "MEDIUM",
    "android.permission.ACCESS_FINE_LOCATION":   "HIGH",
    "android.permission.ACCESS_COARSE_LOCATION": "MEDIUM",
    "android.permission.READ_EXTERNAL_STORAGE":  "MEDIUM",
    "android.permission.WRITE_EXTERNAL_STORAGE": "MEDIUM",
    "android.permission.PROCESS_OUTGOING_CALLS": "HIGH",
    "android.permission.INTERNET":               "LOW",
    "android.permission.CHANGE_WIFI_STATE":      "MEDIUM",
    "android.permission.BLUETOOTH":              "LOW",
    "android.permission.NFC":                    "LOW",
    "android.permission.GET_ACCOUNTS":           "MEDIUM",
    "android.permission.USE_CREDENTIALS":        "HIGH",
    "android.permission.READ_PHONE_STATE":       "HIGH",
    "android.permission.CALL_PHONE":             "HIGH",
    "android.permission.RECEIVE_BOOT_COMPLETED": "MEDIUM",
    "android.permission.SYSTEM_ALERT_WINDOW":    "HIGH",
    "android.permission.INSTALL_PACKAGES":       "CRITICAL",
    "android.permission.DELETE_PACKAGES":        "CRITICAL",
    "android.permission.BIND_DEVICE_ADMIN":      "CRITICAL",
    "android.permission.MOUNT_UNMOUNT_FILESYSTEMS": "HIGH",
    "android.permission.MASTER_CLEAR":           "CRITICAL",
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
    result = {}
    for algo in ["md5", "sha1", "sha256"]:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        result[algo.upper()] = h.hexdigest()
    return result

def analyze_apk(apk_path: str) -> dict:
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
        console.print(f"[red]✗ File not found: {apk_path}[/]")
        return findings

    console.print(Panel(f"[bold cyan]Analyzing:[/] {apk_path}", border_style="magenta"))

    with console.status("[cyan]Computing hashes...[/]"):
        findings["hashes"] = _file_hash(apk_path)

    try:
        zf = zipfile.ZipFile(apk_path, "r")
    except zipfile.BadZipFile:
        console.print("[red]✗ Not a valid APK (ZIP) file.[/]")
        return findings

    namelist = zf.namelist()
    console.print(f"[dim]APK contains [bold]{len(namelist)}[/] entries.[/]")
    zf.close()
    console.print("[green]✓ Static analysis framework ready.[/]")
    return findings