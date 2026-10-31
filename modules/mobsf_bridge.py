"""
Aadi — MobSF REST API Bridge Module (Optimized, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import requests
import os
import json
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel

console = Console()


def upload_and_scan_mobsf(apk_path: str, mobsf_url: str = "http://localhost:8000", api_key: str = "") -> bool:
    """Upload APK to MobSF, trigger scan, and fetch vulnerability summary with robust error handling."""
    if not apk_path or not os.path.isfile(apk_path):
        console.print(f"[bold red]✗ APK file not found or invalid path:[/] {apk_path}")
        return False

    headers = {"Authorization": api_key} if api_key else {}
    upload_url = f"{mobsf_url.rstrip('/')}/api/v1/upload"

    console.print(Panel(
        f"[cyan]Target APK:[/] {os.path.basename(apk_path)}\n"
        f"[cyan]MobSF Server:[/] {mobsf_url}",
        title="[bold cyan]🛡️ AADI MobSF Security Bridge[/]",
        border_style="magenta"
    ))

    try:
        # 1. Upload APK
        console.print("[cyan][*] Uploading APK to MobSF...[/]")
        with open(apk_path, "rb") as f:
            files = {"file": (os.path.basename(apk_path), f)}
            response = requests.post(upload_url, headers=headers, files=files, timeout=60)

        if response.status_code == 200:
            res_json = response.json()
            file_hash = res_json.get("hash")
            app_name = res_json.get("file_name")
            scan_type = res_json.get("scan_type", "apk")

            if not file_hash:
                console.print("[bold red]✗ Upload succeeded but failed to retrieve file hash from MobSF.[/]")
                return False

            console.print(f"[bold green]✓ Upload successful! Hash:[/] [cyan]{file_hash}[/]")

            # 2. Trigger Scan
            console.print("[yellow][*] Triggering static analysis scan on MobSF (this may take a moment)...[/]")
            scan_url = f"{mobsf_url.rstrip('/')}/api/v1/scan"
            scan_data = {"file_name": app_name, "hash": file_hash, "scan_type": scan_type}

            scan_res = requests.post(scan_url, headers=headers, data=scan_data, timeout=120)

            if scan_res.status_code == 200:
                console.print("[bold green]✓ MobSF scan completed successfully![/]")

                # 3. Optional: Fetch JSON Report Summary
                try:
                    report_url = f"{mobsf_url.rstrip('/')}/api/v1/report_json"
                    report_res = requests.post(report_url, headers=headers, data={"hash": file_hash}, timeout=30)
                    if report_res.status_code == 200:
                        report_data = report_res.json()
                        app_score = report_data.get("security_score", "N/A")
                        high_sev = len(report_data.get("high", []))

                        console.print(Panel(
                            f"[white]App Name:[/] [bold]{report_data.get('app_name', app_name)}[/]\n"
                            f"[white]Security Score:[/] [bold yellow]{app_score}/100[/]\n"
                            f"[white]High Severity Issues:[/] [bold red]{high_sev}[/]",
                            title="[bold green]📊 Scan Summary Report[/]",
                            border_style="green"
                        ))
                except Exception:
                    pass

                console.print(f"[dim]Full report available on MobSF web UI at: {mobsf_url}/view/{file_hash}[/]")
                return True
            else:
                err_text = scan_res.text[:300] if scan_res.text else "No response body"
                console.print(f"[bold red]✗ Scan failed with status {scan_res.status_code}:[/] {err_text}")
                return False
        else:
            err_text = response.text[:300] if response.text else "No response body"
            console.print(f"[bold red]✗ Upload failed with status {response.status_code}:[/] {err_text}")
            return False

    except requests.exceptions.ConnectionError:
        console.print(f"[bold red]✗ Connection error: Could not reach MobSF server at {mobsf_url}. Is it running?[/]")
        return False
    except requests.exceptions.Timeout:
        console.print("[bold red]✗ Request timed out while communicating with MobSF server.[/]")
        return False
    except Exception as e:
        console.print(f"[bold red]✗ An unexpected error occurred:[/] {e}")
        return False