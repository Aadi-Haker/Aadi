"""
Aadi — Advanced Intent & Deep-Link Fuzzer (Enhanced, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import time
from typing import List, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def _run_adb(args: List[str], device_id: Optional[str] = None, timeout: int = 3) -> Tuple[str, str, int]:
    """Helper function to run adb commands with timeout and error handling."""
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "Process timed out", -2
    except Exception as e:
        return "", str(e), -1


def fuzz_exported_activities(device_id: str, package_name: str, activity_list: List[str]) -> None:
    """Fuzz exported activities using advanced intent actions and input validation payloads."""
    if not activity_list:
        console.print("[yellow]⚠ No exported activities provided for fuzzing.[/]")
        return

    if not package_name:
        console.print("[red]✗ Target package name cannot be empty.[/]")
        return

    console.print(Panel(
        f"[cyan]Starting Advanced Intent Fuzzing[/]\n"
        f"[white]Target Package:[/] [bold magenta]{package_name}[/]\n"
        f"[white]Target Activities:[/] [bold yellow]{len(activity_list)} found[/]",
        title="[bold cyan]⚡ AADI Intent Fuzzer Engine[/]",
        border_style="magenta"
    ))

    # Standard and malicious fuzz actions
    payload_actions = [
        "android.intent.action.VIEW",
        "android.intent.action.MAIN",
        "android.intent.action.EDIT",
        "android.intent.action.SEND",
        "com.malicious.action.TEST"
    ]

    # Input validation / fuzz payloads for intent extras (Fixed syntax bug: "A" * 1000)
    fuzz_payloads = [
        ("test_string", "' OR 1=1 -- "),                  # SQL Injection probe
        ("payload", "<script>alert(1)</script>"),       # XSS / Code injection probe
        ("data", "A" * 1000),                           # Buffer overflow / Large input probe (Fixed)
        ("url", "file:///etc/passwd"),                  # Path traversal URI probe
        ("debug", "true"),                              # Boolean debug flag toggle
        ("account_id", "-1"),                           # Integer boundary test
    ]

    results_table = Table(title="[bold red]🎯 Intent Fuzzing Results[/]", box=box.DOUBLE_EDGE, border_style="red",
                          header_style="bold red")
    results_table.add_column("Activity", style="cyan", width=25)
    results_table.add_column("Action", style="yellow", width=22)
    results_table.add_column("Payload Extra", style="white", width=20)
    results_table.add_column("Status / Response", style="green", width=20)

    total_tests = 0
    vulnerable_hits = 0

    for act in activity_list:
        component = f"{package_name}/{act}" if not act.startswith(".") else f"{package_name}{act}"

        for actn in payload_actions:
            # Test 1: Clean launch without extras
            total_tests += 1
            out, err, rc = _run_adb(["shell", "am", "start", "-a", actn, "-n", component], device_id)

            status = "[green]✓ OK[/]"
            if rc != 0 or "Error" in err or "Exception" in err:
                status = "[bold red]⚠ CRASH/ERR[/]"
                vulnerable_hits += 1

            results_table.add_row(act, actn, "None (Base)", status)

            # Test 2: Fuzz with malicious/edge-case extra arguments
            for key, val in fuzz_payloads:
                total_tests += 1
                cmd_args = ["shell", "am", "start", "-a", actn, "-n", component, "--es", key, str(val)]
                out, err, rc = _run_adb(cmd_args, device_id)

                payload_status = "[green]✓ Handled[/]"
                if rc != 0 or "Error" in err or "Exception" in err or "SecurityException" in out:
                    payload_status = "[bold yellow]⚠ EXCEPTION[/]"
                    vulnerable_hits += 1

                val_preview = str(val)[:10] + "..." if len(str(val)) > 10 else str(val)
                results_table.add_row(act, actn, f"{key}={val_preview}", payload_status)
                time.sleep(0.05)  # Prevent flooding adb daemon too rapidly

    console.print(results_table)

    console.print(Panel(
        f"[bold green]✓ Intent Fuzzing Completed Successfully![/]\n"
        f"  Total Combinations Tested: [bold cyan]{total_tests}[/]\n"
        f"  Potential Exceptions/Errors Logged: [bold red]{vulnerable_hits}[/]",
        title="[bold]Fuzzing Summary Report[/]",
        border_style="green"
    ))