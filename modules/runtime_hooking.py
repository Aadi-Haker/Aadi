"""
Aadi — Automated Frida Hooking Engine
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# बिल्ट-इन बाईपास स्क्रिप्ट्स (Built-in JS payloads for runtime hooks)
FRIDA_SCRIPTS = {
    "ssl_pinning": """
Java.perform(function() {
    console.log("[*] Script loaded: Universal SSL Pinning Bypass");
    try {
        var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TrustManagerImpl.verifyChain.implementation = function(untrustedChain, trustAnchorCertificates, host, clientAuth, ocspData, tlsSctData) {
            console.log("[+] Bypassed TrustManagerImpl.verifyChain for: " + host);
            return untrustedChain;
        };
    } catch(err) { console.log("[-] TrustManagerImpl hook failed: " + err.message); }

    try {
        var CertificatePinner = Java.use('okhttp3.CertificatePinner');
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(hostname, peerCertificates) {
            console.log("[+] Bypassed OkHttp3 CertificatePinner for: " + hostname);
            return;
        };
    } catch(err) { console.log("[-] OkHttp3 hook failed: " + err.message); }
});
""",
    "root_detection": """
Java.perform(function() {
    console.log("[*] Script loaded: Root Detection Bypass");
    var File = Java.use('java.io.File');
    File.exists.implementation = function() {
        var filename = this.getAbsolutePath();
        if (filename.indexOf("su") != -1 || filename.indexOf("magisk") != -1) {
            console.log("[+] Bypassed root check for file: " + filename);
            return false;
        }
        return this.exists();
    };
});
""",
    "class_dump": """
Java.perform(function() {
    console.log("[*] Script loaded: Class Enumerator");
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            console.log("[Class] " + className);
        },
        onComplete: function() {
            console.log("[+] Class enumeration complete.");
        }
    });
});
"""
}

def _check_frida_cli() -> bool:
    """Check if frida-tools is installed."""
    try:
        subprocess.run(["frida", "--version"], capture_output=True, timeout=3)
        return True
    except FileNotFoundError:
        return False

def run_frida_hook(device_id: str, package: str, hook_type: str = "ssl_pinning"):
    """Automatically spawn/attach app and run Frida hooking script."""
    if not _check_frida_cli():
        console.print("[bold red]✗ Frida CLI tools not found![/] Run: [cyan]pip install frida-tools[/]")
        return False

    script_code = FRIDA_SCRIPTS.get(hook_type)
    if not script_code:
        console.print(f"[bold red]✗ Unknown hook type:[/] {hook_type}")
        return False

    # स्क्रिप्ट को अस्थायी फाइल के रूप में सेव करना
    script_path = f"/tmp/aadi_hook_{hook_type}.js"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_code)

    console.print(Panel(
        f"[bold cyan]Launching Automated Frida Hook[/]\n"
        f"  Target Device: {device_id}\n"
        f"  Target Package: {package}\n"
        f"  Hook Type: {hook_type}\n"
        f"  Temp Script: {script_path}",
        border_style="magenta"
    ))

    # कमांड तैयार करना: frida -U -f <package> -l <script> --no-pause
    cmd = ["frida", "-U", "-f", package, "-l", script_path, "--no-pause"]
    if device_id and ":" in device_id: # अगर वायरलेस ADB है
        cmd = ["frida", "-H", device_id, "-f", package, "-l", script_path, "--no-pause"]

    console.print("[yellow][*] Spawning app and injecting script... Press Ctrl+C to stop.[/]")
    try:
        # इसे इंटरैक्टिव रूप से चलाना ताकि यूजर लाइव आउटपुट देख सके
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[green]✓ Frida hook session terminated.[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Frida execution error:[/] {e}")

    # सफाई
    if os.path.exists(script_path):
        os.remove(script_path)
    return True

def frida_menu(device_id: str):
    """Interactive menu for automated Frida hooks."""
    while True:
        console.print()
        t = Table(title="[bold magenta]⚡ Automated Frida Hooking Engine[/]", box=box.DOUBLE_EDGE, border_style="magenta")
        t.add_column("Option", style="cyan", width=6)
        t.add_column("Hook Action", style="white")
        t.add_column("Description", style="dim")

        t.add_row("[1]", "Universal SSL Pinning Bypass", "Bypass OkHttp3 & Conscrypt certificate pinning")
        t.add_row("[2]", "Root Detection Bypass", "Hook File.exists() to hide su/magisk binaries")
        t.add_row("[3]", "Dump Loaded Classes", "Enumerate and log all active Java classes in real-time")
        t.add_row("[0]", "Back", "Return to main menu")
        console.print(t)

        from rich.prompt import Prompt
        choice = Prompt.ask("[cyan]Select Frida Hook ▶[/]", choices=["0", "1", "2", "3"], default="0")
        if choice == "0":
            break

        pkg = Prompt.ask("[cyan]Enter target package name (e.g. com.example.app)[/]")
        if not pkg:
            continue

        hook_map = {"1": "ssl_pinning", "2": "root_detection", "3": "class_dump"}
        run_frida_hook(device_id, pkg, hook_map.get(choice))