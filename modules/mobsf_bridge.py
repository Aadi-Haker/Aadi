"""
Aadi — MobSF REST API Bridge Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import requests
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def upload_and_scan_mobsf(apk_path: str, mobsf_url: str = "http://localhost:8000", api_key: str = ""):
    """Upload APK to MobSF and retrieve security assessment."""
    if not os.path.exists(apk_path):
        console.print(f"[bold red]✗ APK file not found:[/] {apk_path}")
        return

    headers = {"Authorization": api_key} if api_key else {}
    upload_url = f"{mobsf_url}/api/v1/upload"

    console.print(Panel(f"[cyan]Uploading {os.path.basename(apk_path)} to MobSF at {mobsf_url}...[/]", border_style="magenta"))

    try:
        with open(apk_path, "rb") as f:
            files = {"file": (os.path.basename(apk_path), f)}
            response = requests.post(upload_url, headers=headers, files=files)

        if response.status_code == 200:
            res_json = response.json()
            file_hash = res_json.get("hash")
            app_name = res_json.get("file_name")
            console.print(f"[bold green]✓ Upload successful! Hash: {file_hash}[/]")

            # Trigger scan
            console.print("[yellow][*] Triggering static analysis scan on MobSF...[/]")
            scan_url = f"{mobsf_url}/api/v1/scan"
            scan_data = {"file_name": app_name, "hash": file_hash, "scan_type": "apk"}
            scan_res = requests.post(scan_url, headers=headers, data=scan_data)

            if scan_res.status_code == 200:
                console.print("[bold green]✓ MobSF scan completed successfully! Check MobSF web UI for full report.[/]")
            else:
                console.print(f"[bold red]✗ Scan failed:[/] {scan_res.text}")
        else:
            console.print(f"[bold red]✗ Upload failed with status {response.status_code}:[/] {response.text}")
    except Exception as e:
        console.print(f"[bold red]✗ Connection error to MobSF server:[/] {e}")