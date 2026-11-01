"""
Aadi — APK Signer Module
Author: Aaditya Kumar Pandey
"""

import os
import subprocess
import shutil
from rich.console import Console

console = Console()


def sign_apk(apk_path: str, keystore_path: str = None, alias: str = "aadi_key") -> bool:
    """Sign an unsigned APK file using jarsigner or apksigner with a debug/custom keystore."""
    if not os.path.exists(apk_path):
        console.print(f"[bold red][-] APK file not found: {apk_path}[/]")
        return False

    # Check for apksigner or jarsigner availability
    has_apksigner = shutil.which("apksigner") is not None
    has_jarsigner = shutil.which("jarsigner") is not None

    if not has_apksigner and not has_jarsigner:
        console.print("[bold red][-] Neither 'apksigner' nor 'jarsigner' found on system PATH.[/]")
        return False

    # If no keystore provided, check or generate a default debug keystore
    if not keystore_path or not os.path.exists(keystore_path):
        keystore_path = os.path.expanduser("~/.android/debug.keystore")
        if not os.path.exists(keystore_path):
            console.print("[yellow][*] Generating default debug keystore...[/]")
            os.makedirs(os.path.dirname(keystore_path), exist_ok=True)
            try:
                subprocess.run([
                    "keytool", "-genkey", "-v", "-keystore", keystore_path,
                    "-storepass", "android", "-keypass", "android", "-alias", alias,
                    "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
                    "-dname", "CN=Android, O=Android, C=US"
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                console.print(f"[bold red][-] Failed to generate keystore: {e}[/]")
                return False

    console.print(f"[cyan][*] Signing APK: {apk_path}[/]")

    try:
        if has_apksigner:
            cmd = ["apksigner", "sign", "--ks", keystore_path, "--ks-pass", "pass:android", apk_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[bold green][+] APK successfully signed using apksigner![/]")
                return True
            else:
                console.print(f"[red][-] apksigner failed: {result.stderr}[/]")

        if has_jarsigner:
            cmd = ["jarsigner", "-verbose", "-keystore", keystore_path, "-storepass", "android", apk_path, alias]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[bold green][+] APK successfully signed using jarsigner![/]")
                return True
            else:
                console.print(f"[red][-] jarsigner failed: {result.stderr}[/]")
    except Exception as e:
        console.print(f"[bold red][-] Error during APK signing process: {e}[/]")

    return False