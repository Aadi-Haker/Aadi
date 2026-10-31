"""
Aadi — Automated Frida Hooking Engine (Optimized, Cross-Platform & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import os
import time
import tempfile
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

# बिल्ट-इन बाईपास स्क्रिप्ट्स (Built-in JS payloads for runtime hooks)
FRIDA_SCRIPTS: Dict[str, str] = {
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
    """Check if frida-tools is installed in the system PATH."""
    try:
        res = subprocess.run(["frida", "--version"], capture_output=True, text=True, timeout=3)
        return res.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False


def run_frida_hook(device_id: Optional[str], package: str, hook_type: str = "ssl_pinning") -> bool:
    """Automatically spawn/attach app and run Frida hooking script using cross-platform temp file."""
    if not _check_frida_cli():
        console.print("[bold red]✗ Frida CLI tools not found![/] Run: [cyan]pip install frida-tools[/]")
        return False

    if not package or not package.strip():
        console.print("[bold red]✗ Target package name cannot be empty.[/]")
        return False

    script_code = FRIDA_SCRIPTS.get(hook_type)
    if not script_code:
        console.print(f"[bold red]✗ Unknown hook type:[/] {hook_type}")
        return False

    script_path: Optional[str] = None
    try:
        # Cross-platform secure temporary file creation
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as tmp_file:
            tmp_file.write(script_code)
            script_path = tmp_file.name

        console.print(Panel(
            f"[bold cyan]Launching Automated Frida Hook[/]\n"
            f"  Target Device: {device_id or 'Default / Connected'}\n"
            f"  Target Package: {package}\n"
            f"  Hook Type: {hook_type}\n"
            f"  Temp Script: {script_path}",
            border_style="magenta"
        ))

        # कमांड तैयार करना: frida -U -f <package> -l <script> --no-pause
        if device_id and ":" in device_id:  # अगर वायरलेस ADB है (IP:Port)
            cmd = ["frida", "-H", device_id, "-f", package, "-l", script_path, "--no-pause"]
        elif device_id:
            cmd = ["frida", "-S", device_id, "-f", package, "-l", script_path, "--no-pause"]
        else:
            cmd = ["frida", "-U", "-f", package, "-l", script_path, "--no-pause"]

        console.print("[yellow][*] Spawning app and injecting script... Press Ctrl+C to stop.[/]")

        subprocess.run(cmd)
        console.print("\n[green]✓ Frida hook session completed.[/]")
        return True

    except KeyboardInterrupt:
        console.print("\n[green]✓ Frida hook session terminated by user.[/]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Frida process exited with error code {e.returncode}.[/]")
        return False
    except Exception as e:
        console.print(f"[bold red]✗ Frida execution error: {e}[/]")
        return False
    finally:
        # सुरक्षित सफाई (Cleanup)
        if script_path and os.path.exists(script_path):
            try:
                os.remove(script_path)
            except Exception:
                pass


def frida_menu(device_id: Optional[str]) -> None:
    """Interactive menu for automated Frida hooks."""
    while True:
        console.print()
        t = Table(title="[bold magenta]⚡ Automated Frida Hooking Engine[/]", box=box.DOUBLE_EDGE,
                  border_style="magenta")
        t.add_column("Option", style="cyan", width=6)
        t.add_column("Hook Action", style="white")
        t.add_column("Description", style="dim")

        t.add_row("[1]", "Universal SSL Pinning Bypass", "Bypass OkHttp3 & Conscrypt certificate pinning")
        t.add_row("[2]", "Root Detection Bypass", "Hook File.exists() to hide su/magisk binaries")
        t.add_row("[3]", "Dump Loaded Classes", "Enumerate and log all active Java classes in real-time")
        t.add_row("[0]", "Back", "Return to main menu")
        console.print(t)

        choice = Prompt.ask("[cyan]Select Frida Hook ▶[/]", choices=["0", "1", "2", "3"], default="0")
        if choice == "0":
            break

        pkg = Prompt.ask("[cyan]Enter target package name (e.g. com.example.app)[/]")
        if not pkg or not pkg.strip():
            console.print("[red]✗ Package name cannot be empty.[/]")
            continue

        hook_map = {"1": "ssl_pinning", "2": "root_detection", "3": "class_dump"}
        run_frida_hook(device_id, pkg.strip(), hook_map.get(choice))