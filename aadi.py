#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          Aadi — Advanced Android Pentesting Tool                 ║
║          Author : Aaditya Kumar Pandey                           ║
║          Contact: Instagram @aadi_97621                          ║
║          For authorized penetration testing use only             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import sys
import os
import time
import json
import random
import shutil
import subprocess
import re

# ── Rich UI ────────────────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
except ImportError:
    print("[!] 'rich' not installed. Run: pip install rich")
    sys.exit(1)

# ── Modules ────────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from modules import adb_manager, apk_analyzer, network_scanner
from modules import vulnerability_scanner, exploit_engine, payload_generator, report_generator

console = Console()

VERSION     = "2.0.0"
AUTHOR      = "Aaditya Kumar Pandey"
INSTAGRAM   = "@aadi_97621"
TOOL_NAME   = "AADI"
YEAR        = "2026"


# ═══════════════════════════════════════════════════════════════════════════════
#  BANNER & ANIMATION
# ═══════════════════════════════════════════════════════════════════════════════

BANNER_ART = r"""
    ___    ___    ____  ____
   /   |  /   |  / __ \/  _/
  / /| | / /| | / / / // /  
 / ___ |/ ___ |/ /_/ // /   
/_/  |_/_/  |_/_____/___/   
  
"""

BANNER_LINES_GRADIENT = [
    "magenta", "bright_magenta", "purple", "deep_pink3", "orchid", "violet"
]

def get_banner_status():
    """Gather live status info for the banner."""
    try:
        devices = adb_manager.list_devices()
        device_count = len(devices)
        status_color = "green" if device_count > 0 else "red"
        device_text = f"[{status_color}]{device_count} Connected[/]"

        # Check for wireless connections
        wireless_count = 0
        for device in devices:
            if ":" in device.get("serial", ""):
                wireless_count += 1

        if wireless_count > 0:
            device_text += f" [magenta]({wireless_count} WiFi)[/]"
    except:
        device_text = "[yellow]ADB Not Found[/]"

    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")

    return (
        f"📅 [bold white]{now}[/]  |  "
        f"📱 [bold cyan]Devices:[/] {device_text}  |  "
        f"🚀 [bold green]v{VERSION}[/]"
    )

def animate_glitch_banner():
    """Display a matrix/glitch reveal for the banner."""
    from rich.markup import escape
    lines = BANNER_ART.strip("\n").split("\n")
    
    # Glitch phase
    chars = "01$#!@%^&*()_+=-[]{}|;:,.<>?/"
    for _ in range(12):
        glitch_lines = []
        for line in lines:
            glitch_line = "".join(random.choice(chars) if c != " " else " " for c in line)
            color = random.choice(BANNER_LINES_GRADIENT)
            # Escape the glitch line to prevent MarkupError
            glitch_lines.append(f"[bold {color}]{escape(glitch_line)}[/]")
        
        console.clear()
        for gl in glitch_lines:
            console.print(Align.center(gl))
        time.sleep(0.06)

    # Settling phase (line by line reveal)
    console.clear()
    for i, line in enumerate(lines):
        color = BANNER_LINES_GRADIENT[i % len(BANNER_LINES_GRADIENT)]
        console.print(Align.center(f"[bold {color}]{line}[/]"))
        time.sleep(0.05)

def print_banner():
    """Print the animated Aadi banner with live status."""
    animate_glitch_banner()

    # Tagline
    tagline = Text("◈ ADVANCED ANDROID PENTESTING FRAMEWORK ◈", style="bold italic bright_magenta")
    console.print(Align.center(tagline))
    console.print()

    # Status Panel
    status_text = get_banner_status()
    console.print(Align.center(Panel(
        status_text,
        border_style="magenta",
        box=box.HORIZONTALS,
        padding=(0, 2),
        title="[bold magenta]System Status[/]",
        title_align="left"
    )))
    console.print()


def auto_reconnect_wifi():
    """Automatically try to reconnect to saved WiFi devices on startup."""
    wifi_file = os.path.join(os.path.dirname(__file__), "wifi_devices.json")

    if not os.path.exists(wifi_file):
        return False

    try:
        import json
        with open(wifi_file, "r") as f:
            wifi_data = json.load(f)
    except Exception as e:
        console.print(f"[yellow]Error reading WiFi devices: {e}[/]")
        return False

    if not wifi_data:
        return False

    # Check if any devices are already connected
    try:
        current_devices = adb_manager.list_devices()
        current_serials = [dev.get("serial", "") for dev in current_devices]
    except:
        current_serials = []

    console.print("[cyan]🔄 Attempting auto-reconnection to saved WiFi devices...[/]")

    connected_any = False
    connected_devices = []
    already_connected = []

    for device_id, config in wifi_data.items():
        ip = config.get('ip')
        port = config.get('port', 5555)

        if ip:
            # Check if already connected
            if any(ip in serial for serial in current_serials):
                console.print(f"[dim]{ip}:{port} already connected [green]✓[/]")
                connected_any = True
                already_connected.append(device_id)
                config['last_connected'] = time.strftime("%Y-%m-%d %H:%M:%S")
                continue

            console.print(f"[dim]Trying {ip}:{port}...[/]", end="")
            result = adb_manager.connect_wifi(ip, port)
            if result:
                console.print(" [green]✓ Connected[/]")
                connected_any = True
                connected_devices.append(device_id)
                # Update last connected time
                config['last_connected'] = time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                console.print(" [red]✗ Failed[/]")

    # Update the file with new connection times
    try:
        with open(wifi_file, "w") as f:
            json.dump(wifi_data, f, indent=2)
    except Exception:
        pass

    if connected_any:
        if already_connected:
            console.print(f"[green]✓ {len(already_connected)} device(s) already connected, {len(connected_devices)} reconnected[/]")
        else:
            console.print(f"[green]✓ Successfully reconnected to {len(connected_devices)} WiFi device(s)[/]")
        all_connected = already_connected + connected_devices
        console.print(f"[dim]Connected: {', '.join(all_connected)}[/]")
        return True
    else:
        console.print("[yellow]⚠ Could not auto-reconnect. Device may be offline or network changed.[/]")
        console.print("[yellow]Connect via USB and use 'Auto ADB WiFi Connect' to update device info.[/]")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════════

MENU_OPTIONS = [
    ("1",  "📱", "Device Manager",          "List & manage connected Android devices"),
    ("2",  "🔎", "APK Static Analyzer",     "Decompile & audit an APK file"),
    ("3",  "🌐", "Network Scanner",         "Port scan, WiFi info, host discovery"),
    ("4",  "🚨", "Vulnerability Scanner",   "CVE mapping, root check, insecure storage"),
    ("5",  "💥", "Exploit Engine",          "Launch activities, deep links, shell dropper"),
    ("6",  "🎯", "Payload Generator",       "APK payloads, reverse shells, obfuscation"),
    ("7",  "📋", "Report Generator",        "Generate HTML/JSON security report"),
    ("8",  "📡", "Wireless Setup Wizard",   "Setup wireless ADB connection (cable-free)"),
    ("9",  "⚡", "Auto ADB WiFi Connect",   "Automatically switch USB ADB to WiFi mode"),
    ("10", "📸", "Screenshot Capture",      "Capture device screenshot via ADB"),
    ("11", "📦", "Package Manager",         "Enumerate installed packages"),
    ("12", "🐛", "Logcat Analyzer",         "Capture & analyze logcat for secrets"),
    ("13", "🔐", "SSL Pinning Check",       "Detect SSL pinning in target app"),
    ("14", "📂", "File Transfer",           "Pull/push files from/to device"),
    ("15", "💻", "Interactive ADB Shell",   "Drop into live ADB shell"),
    ("16", "🧰", "Remote Control",          "Remote screen, file explorer, camera and device control tools"),
    ("17", "🔄", "Quick WiFi Connect",      "Connect to previously saved WiFi devices"),
    ("18", "⚙️", "WiFi Settings",          "Configure WiFi auto-reconnect settings"),
    ("19", "❔", "About",                   "About AADI"),
    ("0",  "🚪", "Exit",                    "Exit AADI"),
]

REMOTE_CONTROL_OPTIONS = [
    ("1", "🖥️", "Open Remote Screen", "Open Android screen with scrcpy (audio options)"),
    ("2", "📁", "File Explorer",      "Browse device files"),
    ("3", "📷", "Remote Camera",      "Open remote camera tools"),
    ("4", "📸", "Take Screenshot",    "Capture device screenshot"),
    ("5", "🎥", "Screen Record",      "Record device screen"),
    ("6", "🎵", "Audio Setup Guide",  "Setup instructions for audio streaming"),
    ("7", "📡", "WiFi Device Info",   "Show wireless connection details"),
    ("8", "📊", "Network Monitor",   "Monitor device network traffic"),
    ("9", "🔧", "Device Controls",    "Power, volume, brightness controls"),
    ("10", "📱", "App Manager",       "Install/uninstall apps wirelessly"),
    ("11", "🌐", "WiFi Analyzer",     "Analyze WiFi networks around device"),
    ("0", "↩️", "Back",               "Return to main menu"),
]


def print_main_menu():
    t = Table(
        title=f"\n[bold magenta]👻  {TOOL_NAME}  —  Main Menu[/]\n",
        box=box.DOUBLE_EDGE,
        border_style="magenta",
        header_style="bold cyan",
        show_lines=True,
        min_width=70,
    )
    t.add_column("  #  ",   style="bold cyan",   width=5,  no_wrap=True)
    t.add_column("  ",      style="",             width=4,  no_wrap=True, justify="center")
    t.add_column("Module",  style="bold white",   min_width=24)
    t.add_column("Description", style="dim",      min_width=34)

    for num, icon, name, desc in MENU_OPTIONS:
        style = "on #1a0030" if num == "0" else ""
        t.add_row(f"[bold cyan] {num} [/]", icon, name, desc, style=style)

    console.print(t)


def print_remote_control_menu():
    t = Table(
        title=f"\n[bold magenta]🎛️  {TOOL_NAME}  —  Remote Control[/]\n",
        box=box.DOUBLE_EDGE,
        border_style="magenta",
        header_style="bold cyan",
        show_lines=True,
        min_width=70,
    )
    t.add_column("  #  ",   style="bold cyan",   width=5,  no_wrap=True)
    t.add_column("  ",      style="",             width=3,  no_wrap=True)
    t.add_column("Module",  style="bold white",   min_width=24)
    t.add_column("Description", style="dim",      min_width=38)

    for num, icon, name, desc in REMOTE_CONTROL_OPTIONS:
        style = "on #1a0030" if num == "0" else ""
        t.add_row(f"[bold cyan] {num} [/]", icon, name, desc, style=style)

    console.print(t)


# ═══════════════════════════════════════════════════════════════════════════════
#  DEVICE SELECTION HELPER
# ═══════════════════════════════════════════════════════════════════════════════

def select_device() -> str:
    """Select a connected device; return its serial."""
    devices = adb_manager.list_devices()
    if not devices:
        return None
    if len(devices) == 1:
        dev = devices[0]["serial"]
        console.print(f"[green]Auto-selected device:[/] {dev}")
        return dev
    serial = Prompt.ask("[cyan]Enter device serial[/]")
    return serial


# ═══════════════════════════════════════════════════════════════════════════════
#  MODULE HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def handle_device_manager():
    console.rule("[bold magenta]📱 Device Manager[/]")
    adb_manager.check_adb()
    device_id = select_device()
    if not device_id:
        return
    adb_manager.device_info(device_id)


def handle_apk_analyzer():
    console.rule("[bold magenta]🔎 APK Static Analyzer[/]")
    apk_path = Prompt.ask("[cyan]APK file path[/]")
    findings  = apk_analyzer.analyze_apk(apk_path)
    if Confirm.ask("[cyan]Save findings to report?[/]", default=True):
        _save_to_session(findings, "apk_analysis")
        console.print("[green]✓ Added to session report.[/]")


def handle_network_scanner():
    console.rule("[bold magenta]🌐 Network Scanner[/]")
    choice = Prompt.ask("[cyan]Scan mode[/]", choices=["device", "host", "wifi", "discover", "mitm"], default="device")

    if choice == "device":
        device_id = select_device()
        if not device_id:
            return
        ip = network_scanner.get_device_ip(device_id)
        if ip:
            console.print(f"[green]Device IP:[/] {ip}")
            network_scanner.port_scan(ip)
        else:
            console.print("[red]Could not determine device IP.[/]")

    elif choice == "host":
        target = Prompt.ask("[cyan]Target IP/hostname[/]")
        port_range = Prompt.ask("[cyan]Port range (comma-list or 'all')[/]", default="common")
        if port_range == "all":
            ports = list(range(1, 65536))
        elif port_range == "common":
            ports = None
        else:
            ports = [int(p.strip()) for p in port_range.split(",") if p.strip().isdigit()]
        network_scanner.port_scan(target, ports)

    elif choice == "wifi":
        device_id = select_device()
        if device_id:
            network_scanner.get_wifi_info(device_id)

    elif choice == "discover":
        subnet = Prompt.ask("[cyan]Subnet (e.g. 192.168.1)[/]")
        network_scanner.discover_devices(subnet)

    elif choice == "mitm":
        network_scanner.mitm_setup_guide()


def handle_vulnerability_scanner():
    console.rule("[bold magenta]🚨 Vulnerability Scanner[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg = Prompt.ask("[cyan]Target package (leave blank for device-level only)[/]", default="")
    report = vulnerability_scanner.full_vulnerability_scan(device_id, pkg or None)
    _save_to_session(report, "vulnerability_scan")


def handle_exploit_engine():
    console.rule("[bold magenta]💥 Exploit Engine[/]")
    device_id = select_device()
    if not device_id:
        return

    exploit_engine.exploit_menu(device_id)
    choice = Prompt.ask("[red]Select exploit[/]", choices=[str(i) for i in range(10)])

    if choice == "1":
        pkg  = Prompt.ask("[cyan]Package name[/]")
        act  = Prompt.ask("[cyan]Activity class[/]")
        exploit_engine.launch_exported_activity(device_id, pkg, act)

    elif choice == "2":
        pkg    = Prompt.ask("[cyan]Package name[/]")
        action = Prompt.ask("[cyan]Intent action[/]")
        exploit_engine.trigger_broadcast_receiver(device_id, pkg, action)

    elif choice == "3":
        uri = Prompt.ask("[cyan]Content provider URI (content://...)[/]")
        exploit_engine.extract_content_provider(device_id, uri)

    elif choice == "4":
        pkg    = Prompt.ask("[cyan]Package name[/]")
        scheme = Prompt.ask("[cyan]Deep link scheme (e.g. myapp)[/]")
        exploit_engine.deep_link_fuzzer(device_id, pkg, scheme)

    elif choice == "5":
        pkg = Prompt.ask("[cyan]Package name[/]")
        exploit_engine.frida_injection_guide(pkg)

    elif choice == "6":
        lhost = Prompt.ask("[cyan]LHOST[/]")
        lport = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        exploit_engine.shell_payload_dropper(device_id, lhost, lport)

    elif choice == "7":
        pkg  = Prompt.ask("[cyan]Package name[/]")
        db   = Prompt.ask("[cyan]Database filename[/]")
        exploit_engine.extract_database(device_id, pkg, db)

    elif choice == "8":
        exploit_engine.bypass_lock_screen(device_id)

    elif choice == "9":
        exploit_engine.enable_developer_options(device_id)


def handle_payload_generator():
    console.rule("[bold magenta]🎯 Payload Generator[/]")
    payload_generator.payload_menu()
    choice = Prompt.ask("[red]Select payload type[/]", choices=["1", "2", "3", "4", "5", "0"])

    if choice == "1":
        lhost  = Prompt.ask("[cyan]LHOST[/]")
        lport  = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        ptype  = Prompt.ask("[cyan]Payload type[/]",
                             choices=["reverse_tcp", "reverse_https", "reverse_http", "shell_tcp"],
                             default="reverse_tcp")
        output = Prompt.ask("[cyan]Output file[/]", default="payload.apk")
        payload_generator.generate_msfvenom_apk(lhost, lport, ptype, output)

    elif choice == "2":
        action = Prompt.ask("[cyan]Intent action[/]")
        comp   = Prompt.ask("[cyan]Component (pkg/class or blank)[/]", default="")
        data   = Prompt.ask("[cyan]Data URI (or blank)[/]", default="")
        payload_generator.generate_intent_payload(action, comp or None, data or None)

    elif choice == "3":
        lhost = Prompt.ask("[cyan]LHOST[/]")
        lport = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        payload_generator.generate_reverse_shell_commands(lhost, lport)

    elif choice == "4":
        lhost  = Prompt.ask("[cyan]LHOST[/]")
        lport  = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        output = Prompt.ask("[cyan]Script filename[/]", default="adb_payload.sh")
        payload_generator.generate_adb_payload_script(None, lhost, lport, output)

    elif choice == "5":
        raw   = Prompt.ask("[cyan]Payload to obfuscate[/]")
        method = Prompt.ask("[cyan]Obfuscation method[/]", choices=["base64", "hex"], default="base64")
        payload_generator.obfuscate_payload(raw, method)


def handle_report_generator():
    console.rule("[bold magenta]📋 Report Generator[/]")
    target = Prompt.ask("[cyan]Target description (app/device name)[/]", default="Unknown Target")

    # Build report from session
    data = _get_session()
    data["target"] = target

    fmt = Prompt.ask("[cyan]Report format[/]", choices=["html", "json", "both", "table"], default="html")

    if fmt in ("html", "both"):
        out = Prompt.ask("[cyan]HTML output filename[/]", default="aadi_report.html")
        report_generator.generate_html_report(data, out)

    if fmt in ("json", "both"):
        out = Prompt.ask("[cyan]JSON output filename[/]", default="aadi_report.json")
        report_generator.generate_json_report(data, out)

    if fmt == "table":
        report_generator.print_summary_table(data)


def handle_adb_wifi():
    console.rule("[bold magenta]📡 ADB WiFi Connect[/]")
    device_id = select_device()
    if not device_id:
        return
    port = IntPrompt.ask("[cyan]Port[/]", default=5555)
    ip, p = adb_manager.enable_adb_wifi(device_id, port)
    if ip:
        console.print(f"[bold green]✓ WiFi ADB enabled on:[/] {ip}:{p}")
        console.print(f"[cyan]To connect wirelessly later:[/] adb connect {ip}:{p}")


def wireless_connection_wizard():
    """Guide user through setting up wireless ADB connection."""
    console.rule("[bold magenta]📡 Wireless Connection Wizard[/]")

    wizard = Panel(
        "[bold cyan]📡 Wireless ADB Setup Guide[/]\n\n"
        "[bold white]Step 1: Initial USB Connection[/]\n"
        "[dim]• Connect your Android device via USB cable (one-time setup)[/]\n"
        "[dim]• Enable USB Debugging in Developer Options[/]\n"
        "[dim]• Ensure both devices are on the same WiFi network[/]\n\n"
        "[bold white]Step 2: Enable WiFi ADB[/]\n"
        "[dim]• Run: adb tcpip 5555[/]\n"
        "[dim]• This switches ADB from USB to WiFi mode[/]\n\n"
        "[bold white]Step 3: Connect Wirelessly[/]\n"
        "[dim]• Get device IP: adb shell ip addr show wlan0[/]\n"
        "[dim]• Connect: adb connect <device_ip>:5555[/]\n\n"
        "[bold white]Step 4: Remove Cable[/]\n"
        "[dim]• Once connected via WiFi, you can remove the USB cable[/]\n"
        "[dim]• Device will stay connected as long as on same network[/]\n\n"
        "[bold yellow]💡 Tips:[/]\n"
        "[dim]• Reboot required to revert to USB mode[/]\n"
        "[dim]• Some ROMs may require re-enabling after reboot[/]\n"
        "[dim]• Use 'Auto ADB WiFi Connect' for automated setup[/]",
        title="[bold]Wireless Setup Wizard[/]",
        border_style="cyan",
        padding=(0, 2)
    )
    console.print(wizard)

    if Confirm.ask("[cyan]Would you like to run automatic WiFi setup now?[/]", default=True):
        console.print("[cyan]Please connect your device via USB first (one-time requirement)...[/]")
        time.sleep(2)
        handle_auto_adb_wifi()


def handle_adb_wifi():
    console.rule("[bold magenta]📡 ADB WiFi Connect[/]")
    device_id = select_device()
    if not device_id:
        return
    port = IntPrompt.ask("[cyan]Port[/]", default=5555)
    ip, p = adb_manager.enable_adb_wifi(device_id, port)
    if ip:
        console.print(f"[bold green]✓ WiFi ADB enabled on:[/] {ip}:{p}")
        console.print(f"[cyan]To connect wirelessly later:[/] adb connect {ip}:{p}")


def handle_auto_adb_wifi():
    console.rule("[bold magenta]⚡ Auto ADB WiFi Connect[/]")
    device_id = select_device()
    if not device_id:
        return
    adb_manager.auto_adb_wifi_connect(device_id, 5555)


def handle_screenshot():
    console.rule("[bold magenta]📸 Screenshot Capture[/]")
    device_id = select_device()
    if not device_id:
        return
    path = adb_manager.take_screenshot(device_id)
    if path:
        console.print(f"[bold green]✓ Screenshot saved:[/] {path}")


def handle_package_manager():
    console.rule("[bold magenta]📦 Package Manager[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg_type = Prompt.ask("[cyan]Package filter[/]",
                           choices=["all", "system", "third_party", "disabled"],
                           default="third_party")
    adb_manager.list_packages(device_id, pkg_type)


def handle_logcat():
    console.rule("[bold magenta]🐛 Logcat Analyzer[/]")
    device_id = select_device()
    if not device_id:
        return
    lines = IntPrompt.ask("[cyan]Lines to capture[/]", default=300)
    adb_manager.capture_logcat(device_id, lines)


def handle_ssl_check():
    console.rule("[bold magenta]🔐 SSL Pinning Check[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg = Prompt.ask("[cyan]Package name[/]")
    network_scanner.check_ssl_pinning(device_id, pkg)


def handle_file_transfer():
    console.rule("[bold magenta]📂 File Transfer[/]")
    device_id = select_device()
    if not device_id:
        return
    direction = Prompt.ask("[cyan]Direction[/]", choices=["pull", "push"])
    if direction == "pull":
        remote = Prompt.ask("[cyan]Remote path (on device)[/]")
        local  = Prompt.ask("[cyan]Local destination[/]", default=".")
        adb_manager.pull_file(device_id, remote, local)
    else:
        local  = Prompt.ask("[cyan]Local file path[/]")
        remote = Prompt.ask("[cyan]Remote destination (on device)[/]")
        adb_manager.push_file(device_id, local, remote)


def handle_adb_shell():
    console.rule("[bold magenta]💻 Interactive ADB Shell[/]")
    device_id = select_device()
    if not device_id:
        return
    adb_manager.interactive_shell(device_id)


def check_scrcpy() -> bool:
    """Check whether scrcpy is available on PATH."""
    if shutil.which("scrcpy"):
        return True
    console.print("[bold red]scrcpy not found.[/] Install it with: [bold cyan]sudo apt install scrcpy[/]")
    return False


def open_remote_screen(device_id: str, audio_mode: str = "laptop") -> bool:
    """Launch scrcpy for the selected Android device with audio options."""
    cmd = [
        "scrcpy",
        "-s", device_id,
        "--window-title", "Remote Screen",
        "--max-size", "900",
    ]

    # Audio mode configuration
    if audio_mode == "device":
        cmd.append("--no-audio")
        console.print("[cyan]Audio mode: Device only (no audio forwarding)[/]")
    elif audio_mode == "laptop":
        # Default behavior - audio forwarded to laptop
        console.print("[cyan]Audio mode: Laptop only (audio forwarded)[/]")
    elif audio_mode == "both":
        # For both mode, we disable audio forwarding so device plays audio
        # and provide guidance for getting audio on laptop too
        cmd.append("--no-audio")
        console.print("[cyan]Audio mode: Both - Device audio + Laptop audio streaming[/]")
        console.print("[yellow]Device will play audio locally. For laptop audio, use one of these methods:[/]")
        console.print("[dim]1. Install SoundWire (Android) + SoundWire Server (PC)[/]")
        console.print("[dim]2. Use AudioRelay app for audio streaming[/]")
        console.print("[dim]3. Connect device audio to laptop via audio cable[/]")
        console.print("[yellow]Audio streaming apps allow you to hear audio on both devices simultaneously.[/]")
    else:
        console.print("[yellow]Audio mode: Laptop only (default)[/]")

    try:
        subprocess.Popen(cmd)
        console.print("[bold green]Remote Screen launched.[/]")
        return True
    except FileNotFoundError:
        console.print("[bold red]scrcpy not found.[/] Install it with: [bold cyan]sudo apt install scrcpy[/]")
    except OSError as exc:
        console.print(f"[bold red]Failed to launch Remote Screen:[/] {exc}")
    return False


def show_wifi_device_info():
    """Display detailed WiFi connection information for the device."""
    console.rule("[bold magenta]📡 WiFi Device Info[/]")
    device_id = select_device()
    if not device_id:
        return

    # Check if device is connected via WiFi
    is_wireless = ":" in device_id
    connection_type = "[green]WiFi[/]" if is_wireless else "[yellow]USB[/]"
    console.print(f"[cyan]Connection Type:[/] {connection_type}")
    console.print(f"[cyan]Device ID:[/] {device_id}")

    if is_wireless:
        ip, port = device_id.split(":")
        console.print(f"[cyan]IP Address:[/] {ip}")
        console.print(f"[cyan]Port:[/] {port}")

        # Get additional network info
        try:
            wifi_info_out, _ = adb_manager.run_adb(["shell", "dumpsys", "wifi"], device_id)
            if wifi_info_info := adb_manager._extract_device_ip(wifi_info_out):
                console.print(f"[cyan]WiFi IP:[/] {wifi_info_info}")

            # Get signal strength
            signal_out, _ = adb_manager.run_adb(["shell", "dumpsys", "wifi"], device_id)
            if "rssi" in signal_out.lower():
                console.print("[cyan]Signal Strength:[/] Available in detailed dumpsys output")

        except Exception as e:
            console.print(f"[yellow]Could not get detailed WiFi info: {e}[/]")

    # Get device battery and status
    battery_out, _ = adb_manager.run_adb(["shell", "dumpsys", "battery"], device_id)
    if battery_out:
        console.print("[cyan]Battery Status:[/] Available")

    console.print(f"[green]✓ Device is accessible wirelessly for all remote control features[/]")


def monitor_network_traffic():
    """Monitor network traffic on the device."""
    console.rule("[bold magenta]📊 Network Monitor[/]")
    device_id = select_device()
    if not device_id:
        return

    console.print("[cyan]Starting network traffic monitoring...[/]")
    console.print("[yellow]Press Ctrl+C to stop monitoring[/]")

    try:
        # Start monitoring network connections
        while True:
            console.clear()
            console.print(f"[bold magenta]📊 Network Traffic Monitor - {device_id}[/]\n")

            # Get current network connections
            netstat_out, _ = adb_manager.run_adb(["shell", "netstat"], device_id)
            if netstat_out:
                console.print("[bold cyan]Active Network Connections:[/]")
                console.print(netstat_out[:500])  # Limit output

            # Get network stats
            net_stats_out, _ = adb_manager.run_adb(["shell", "cat", "/proc/net/dev"], device_id)
            if net_stats_out:
                console.print("\n[bold cyan]Network Interface Statistics:[/]")
                console.print(net_stats_out)

            # Get WiFi info
            wifi_out, _ = adb_manager.run_adb(["shell", "dumpsys", "wifi"], device_id)
            if wifi_out and "SSID" in wifi_out:
                console.print("[bold cyan]Connected WiFi Network:[/]")
                import re
                ssid_match = re.search(r'SSID: ([^\s,]+)', wifi_out)
                if ssid_match:
                    console.print(f"  Network: {ssid_match.group(1)}")

            time.sleep(3)

    except KeyboardInterrupt:
        console.print("\n[yellow]Network monitoring stopped.[/]")
    except Exception as e:
        console.print(f"[red]Error during network monitoring: {e}[/]")


def device_controls():
    """Wireless device control - power, volume, brightness."""
    console.rule("[bold magenta]🔧 Device Controls[/]")
    device_id = select_device()
    if not device_id:
        return

    control_options = [
        ("1", "🔊", "Volume Up", "Increase volume"),
        ("2", "🔉", "Volume Down", "Decrease volume"),
        ("3", "🔇", "Mute", "Mute device"),
        ("4", "📱", "Power", "Power button press"),
        ("5", "🏠", "Home", "Home button press"),
        ("6", "⬅️", "Back", "Back button press"),
        ("7", "☀️", "Brightness Up", "Increase brightness"),
        ("8", "🌑", "Brightness Down", "Decrease brightness"),
        ("9", "🔓", "Screen Unlock", "Attempt to unlock screen"),
        ("0", "↩️", "Back", "Return to remote control menu"),
    ]

    while True:
        console.print()
        t = Table(title=f"\n[bold magenta]🔧 Device Controls - {device_id}[/]\n",
                  box=box.DOUBLE_EDGE, border_style="magenta", header_style="bold cyan")
        t.add_column("#", style="cyan", width=3)
        t.add_column("", style="", width=3)
        t.add_column("Control", style="white", min_width=20)
        t.add_column("Description", style="dim")

        for num, icon, name, desc in control_options:
            t.add_row(num, icon, name, desc)

        console.print(t)

        choice = Prompt.ask("\n[bold cyan]Device Control ▶[/]",
                           choices=[num for num, *_ in control_options], show_choices=False)

        if choice == "0":
            return

        if choice == "1":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_VOLUME_UP"], device_id)
            console.print("[green]Volume increased[/]")
        elif choice == "2":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_VOLUME_DOWN"], device_id)
            console.print("[green]Volume decreased[/]")
        elif choice == "3":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_MUTE"], device_id)
            console.print("[green]Device muted[/]")
        elif choice == "4":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_POWER"], device_id)
            console.print("[green]Power button pressed[/]")
        elif choice == "5":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_HOME"], device_id)
            console.print("[green]Home button pressed[/]")
        elif choice == "6":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_BACK"], device_id)
            console.print("[green]Back button pressed[/]")
        elif choice == "7":
            adb_manager.run_adb(["shell", "cmd", "window", "change-screencolor", "brightness", "0.8"], device_id)
            console.print("[green]Brightness increased[/]")
        elif choice == "8":
            adb_manager.run_adb(["shell", "cmd", "window", "change-screencolor", "brightness", "0.3"], device_id)
            console.print("[green]Brightness decreased[/]")
        elif choice == "9":
            adb_manager.run_adb(["shell", "input", "keyevent", "KEYCODE_MENU"], device_id)
            console.print("[green]Menu button pressed (may help unlock)[/]")


def wireless_app_manager():
    """Install/uninstall apps wirelessly."""
    console.rule("[bold magenta]📱 Wireless App Manager[/]")
    device_id = select_device()
    if not device_id:
        return

    app_options = [
        ("1", "📥", "Install APK", "Install APK file from local machine"),
        ("2", "🗑️", "Uninstall App", "Uninstalled installed app"),
        ("3", "📋", "List Apps", "List installed applications"),
        ("4", "🔄", "Update App", "Update app from APK file"),
        ("0", "↩️", "Back", "Return to remote control menu"),
    ]

    while True:
        console.print()
        t = Table(title=f"\n[bold magenta]📱 Wireless App Manager - {device_id}[/]\n",
                  box=box.DOUBLE_EDGE, border_style="magenta", header_style="bold cyan")
        t.add_column("#", style="cyan", width=3)
        t.add_column("", style="", width=3)
        t.add_column("Action", style="white", min_width=20)
        t.add_column("Description", style="dim")

        for num, icon, name, desc in app_options:
            t.add_row(num, icon, name, desc)

        console.print(t)

        choice = Prompt.ask("\n[bold cyan]App Manager ▶[/]",
                           choices=[num for num, *_ in app_options], show_choices=False)

        if choice == "0":
            return

        if choice == "1":
            apk_path = Prompt.ask("[cyan]APK file path[/]")
            if os.path.exists(apk_path):
                console.print(f"[cyan]Installing {apk_path}...[/]")
                adb_manager.run_adb(["install", apk_path], device_id)
                console.print("[green]Installation command sent[/]")
            else:
                console.print("[red]File not found[/]")

        elif choice == "2":
            package_name = Prompt.ask("[cyan]Package name[/]")
            console.print(f"[cyan]Uninstalling {package_name}...[/]")
            adb_manager.run_adb(["uninstall", package_name], device_id)
            console.print("[green]Uninstallation command sent[/]")

        elif choice == "3":
            pkg_type = Prompt.ask("[cyan]Package filter[/]",
                                choices=["all", "third_party"], default="third_party")
            adb_manager.list_packages(device_id, pkg_type)

        elif choice == "4":
            apk_path = Prompt.ask("[cyan]APK file path[/]")
            if os.path.exists(apk_path):
                console.print(f"[cyan]Updating with {apk_path}...[/]")
                adb_manager.run_adb(["install", "-r", apk_path], device_id)
                console.print("[green]Update command sent[/]")
            else:
                console.print("[red]File not found[/]")


def wifi_analyzer():
    """Analyze WiFi networks around the device."""
    console.rule("[bold magenta]🌐 WiFi Analyzer[/]")
    device_id = select_device()
    if not device_id:
        return

    console.print("[cyan]Scanning WiFi networks...[/]")

    # Get WiFi scan results
    scan_out, _ = adb_manager.run_adb(["shell", "cmd", "wifi", "list-scan-results"], device_id)

    if scan_out:
        console.print("[bold green]Available WiFi Networks:[/]")
        console.print(scan_out)
    else:
        console.print("[yellow]Could not get WiFi scan results. Trying alternative method...[/]")
        # Alternative method
        alt_out, _ = adb_manager.run_adb(["shell", "dumpsys", "wifi"], device_id)
        if alt_out:
            console.print("[bold cyan]WiFi Information:[/]")
            # Extract relevant info
            if "SSID" in alt_out:
                ssids = re.findall(r'SSID: ([^\s,]+)', alt_out)
                if ssids:
                    console.print("[cyan]Nearby Networks:[/]")
                    for ssid in set(ssids[:10]):  # Show unique SSIDs
                        console.print(f"  • {ssid}")

    # Get current connection info
    current_out, _ = adb_manager.run_adb(["shell", "dumpsys", "wifi"], device_id)
    if current_out:
        ssid_match = re.search(r'SSID: ([^\s,]+)', current_out)
        if ssid_match:
            console.print(f"\n[green]Currently Connected:[/] {ssid_match.group(1)}")

        # Get signal strength
        rssi_match = re.search(r'rssi=(-?\d+)', current_out)
        if rssi_match:
            rssi = int(rssi_match.group(1))
            signal_quality = "Excellent" if rssi > -50 else "Good" if rssi > -60 else "Fair" if rssi > -70 else "Poor"
            console.print(f"[cyan]Signal Strength:[/] {rssi} dBm ({signal_quality})")

        # Get link speed
        speed_match = re.search(r'link_speed=(\d+)', current_out)
        if speed_match:
            console.print(f"[cyan]Link Speed:[/] {speed_match.group(1)} Mbps")

    console.print(f"\n[green]✓ WiFi analysis complete for {device_id}[/]")


def show_audio_setup_guide():
    """Display detailed audio streaming setup instructions."""
    guide = Panel(
        "[bold cyan]🎵 Audio Streaming Setup Guide[/]\n\n"
        "[bold white]Option 1: SoundWire[/]\n"
        "[dim]1. Install SoundWire on Android from Play Store[/]\n"
        "[dim]2. Install SoundWire Server on your PC from soundwire.org[/]\n"
        "[dim]3. Connect both devices to same WiFi network[/]\n"
        "[dim]4. Run SoundWire Server on PC, enter IP in Android app[/]\n\n"
        "[bold white]Option 2: AudioRelay[/]\n"
        "[dim]1. Install AudioRelay on Android[/]\n"
        "[dim]2. Install AudioRelay Server on PC[/]\n"
        "[dim]3. Connect via WiFi and configure audio routing[/]\n\n"
        "[bold white]Option 3: Audio Cable[/]\n"
        "[dim]1. Connect 3.5mm audio cable from device to laptop line-in[/]\n"
        "[dim]2. Configure laptop to record from line-in input[/]\n\n"
        "[bold yellow]Tip: Use 'device' audio mode in Aadi + audio streaming app for best results![/]",
        title="[bold]Audio Setup Guide[/]",
        border_style="cyan",
        padding=(0, 2)
    )
    console.print(guide)


def handle_remote_control():
    while True:
        console.print()
        print_remote_control_menu()
        valid_choices = [num for num, *_ in REMOTE_CONTROL_OPTIONS]
        choice = Prompt.ask("\n[bold cyan]Remote Control ▶[/]", choices=valid_choices, show_choices=False)

        if choice == "0":
            return

        if choice == "1":
            if not check_scrcpy():
                continue
            device_id = select_device()
            if not device_id:
                continue
            audio_mode = Prompt.ask(
                "[cyan]Select audio mode[/]",
                choices=["laptop", "device", "both"],
                default="laptop"
            )
            open_remote_screen(device_id, audio_mode)
            continue

        if choice == "2":
            console.print("[yellow]File Explorer - Coming soon![/]")
            continue

        if choice == "3":
            console.print("[yellow]Remote Camera - Coming soon![/]")
            continue

        if choice == "4":
            handle_screenshot()
            continue

        if choice == "5":
            console.print("[yellow]Screen Record - Coming soon![/]")
            continue

        if choice == "6":
            show_audio_setup_guide()
            continue

        if choice == "7":
            show_wifi_device_info()
            continue

        if choice == "8":
            monitor_network_traffic()
            continue

        if choice == "9":
            device_controls()
            continue

        if choice == "10":
            wireless_app_manager()
            continue

        if choice == "11":
            wifi_analyzer()
            continue

        console.print("[yellow]This feature is not ready yet.[/]")


def handle_about():
    about = Panel(
        f"\n"
        f"  [bold magenta]👻  {TOOL_NAME} v{VERSION}[/]\n\n"
        f"  [bold cyan]Advanced Android Penetration Testing Framework[/]\n\n"
        f"  [white]A comprehensive tool for ethical hackers and security professionals.\n"
        f"  Covers static APK analysis, dynamic runtime analysis via ADB,\n"
        f"  network scanning, vulnerability mapping, exploit assistance,\n"
        f"  payload generation, and professional report generation.[/]\n\n"
        f"  [bold magenta]Author   :[/] [white]{AUTHOR}[/]\n"
        f"  [bold magenta]Instagram:[/] [cyan]{INSTAGRAM}[/]\n"
        f"  [bold magenta]Built by :[/] [white]Aaditya Kumar Pandey / Aadi[/]\n"
        f"  [bold magenta]Year     :[/] [white]{YEAR}[/]\n\n"
        f"  [bold red]⚠  For authorized penetration testing use only.[/]\n"
        f"  [dim]Unauthorized use is illegal and unethical.[/]\n",
        title="[bold]About Aadi[/]",
        border_style="magenta",
        padding=(0, 4),
    )
    console.print(about)


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STORE (in-memory findings accumulator)
# ═══════════════════════════════════════════════════════════════════════════════

_SESSION = {"findings": [], "permissions": [], "secrets": [], "urls": []}
_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "aadi_config.json")


def load_config():
    """Load tool configuration."""
    default_config = {
        "auto_reconnect_wifi": True,
        "wifi_timeout": 30,
        "preserve_wifi_on_device": True
    }

    if os.path.exists(_CONFIG_FILE):
        try:
            with open(_CONFIG_FILE, "r") as f:
                config = json.load(f)
                default_config.update(config)
        except Exception:
            pass

    return default_config


def save_config(config):
    """Save tool configuration."""
    try:
        with open(_CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        console.print(f"[yellow]Could not save config: {e}[/]")


def _save_to_session(data: dict, source: str):
    """Merge findings from a module into the session store."""
    if isinstance(data, dict):
        for vuln in data.get("vulnerabilities", []):
            _SESSION["findings"].append(vuln)
        for vuln in data.get("cves", []):
            _SESSION["findings"].append({
                "name": vuln.get("cve", "CVE"),
                "severity": vuln.get("severity", "MEDIUM"),
                "detail": vuln.get("detail", ""),
                "cve": vuln.get("cve"),
            })
        _SESSION["permissions"].extend(data.get("dangerous_permissions", []))
        _SESSION["secrets"].extend(data.get("secrets", []))
        _SESSION["urls"].extend(data.get("urls", []))


def _get_session() -> dict:
    return _SESSION.copy()


def quick_wifi_connect():
    """Quick connect to previously saved WiFi devices."""
    wifi_file = os.path.join(os.path.dirname(__file__), "wifi_devices.json")

    if not os.path.exists(wifi_file):
        console.print("[yellow]No saved WiFi devices found.[/]")
        console.print("[dim]Use 'Auto ADB WiFi Connect' to save devices for quick reconnect.[/]")
        return

    try:
        import json
        with open(wifi_file, "r") as f:
            wifi_data = json.load(f)
    except Exception as e:
        console.print(f"[red]Error reading WiFi devices file: {e}[/]")
        return

    if not wifi_data:
        console.print("[yellow]No saved WiFi devices.[/]")
        return

    console.print("[bold cyan]Saved WiFi Devices:[/]")
    device_list = list(wifi_data.keys())
    for i, device_id in enumerate(device_list, 1):
        config = wifi_data[device_id]
        console.print(f"  [cyan]{i}.[/] {device_id} [dim](Last: {config.get('last_connected', 'Unknown')})[/]")

    if Confirm.ask("[cyan]Connect to a saved device?[/]", default=False):
        choice = IntPrompt.ask("[cyan]Enter device number[/]", default=1)
        if 1 <= choice <= len(device_list):
            device_id = device_list[choice - 1]
            config = wifi_data[device_id]
            console.print(f"[cyan]Connecting to:[/] {config['ip']}:{config['port']}")
            result = adb_manager.connect_wifi(config['ip'], config['port'])
            if result:
                console.print("[green]✓ Connected successfully![/]")
            else:
                console.print("[red]✗ Connection failed. Device may be offline or network changed.[/]")
        else:
            console.print("[red]Invalid selection.[/]")
    else:
        if Confirm.ask("[cyan]Would you like to clear saved devices?[/]", default=False):
            os.remove(wifi_file)
            console.print("[green]✓ Saved WiFi devices cleared.[/]")


def handle_wifi_settings():
    """Configure WiFi auto-reconnect settings."""
    console.rule("[bold magenta]⚙️ WiFi Settings[/]")

    config = load_config()

    console.print(Panel(
        f"[bold cyan]Current WiFi Settings:[/]\n\n"
        f"[white]Auto-reconnect on startup:[/] {'[green]Enabled[/]' if config.get('auto_reconnect_wifi', True) else '[red]Disabled[/]'}\n"
        f"[white]WiFi connection timeout:[/] {config.get('wifi_timeout', 30)} seconds\n"
        f"[white]Preserve WiFi on device:[/] {'[green]Enabled[/]' if config.get('preserve_wifi_on_device', True) else '[red]Disabled[/]'}\n\n"
        f"[dim]These settings control how Aadi handles WiFi connections across VM restarts.[/]",
        title="[bold]WiFi Configuration[/]",
        border_style="cyan",
        padding=(0, 2)
    ))

    choice = Prompt.ask(
        "[cyan]What would you like to change?[/]",
        choices=["auto_reconnect", "timeout", "preserve", "back"],
        default="back"
    )

    if choice == "auto_reconnect":
        config["auto_reconnect_wifi"] = not config.get("auto_reconnect_wifi", True)
        status = "enabled" if config["auto_reconnect_wifi"] else "disabled"
        console.print(f"[green]✓ Auto-reconnect {status}[/]")
        save_config(config)

    elif choice == "timeout":
        new_timeout = IntPrompt.ask("[cyan]Enter new timeout (seconds)[/]", default=config.get('wifi_timeout', 30))
        config["wifi_timeout"] = new_timeout
        console.print(f"[green]✓ WiFi timeout set to {new_timeout} seconds[/]")
        save_config(config)

    elif choice == "preserve":
        config["preserve_wifi_on_device"] = not config.get("preserve_wifi_on_device", True)
        status = "enabled" if config["preserve_wifi_on_device"] else "disabled"
        console.print(f"[green]✓ WiFi preservation {status}[/]")
        save_config(config)



# ═══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════════════════════

HANDLER_MAP = {
    "1":  handle_device_manager,
    "2":  handle_apk_analyzer,
    "3":  handle_network_scanner,
    "4":  handle_vulnerability_scanner,
    "5":  handle_exploit_engine,
    "6":  handle_payload_generator,
    "7":  handle_report_generator,
    "8":  wireless_connection_wizard,
    "9":  handle_auto_adb_wifi,
    "10": handle_screenshot,
    "11": handle_package_manager,
    "12": handle_logcat,
    "13": handle_ssl_check,
    "14": handle_file_transfer,
    "15": handle_adb_shell,
    "16": handle_remote_control,
    "17": quick_wifi_connect,
    "18": handle_wifi_settings,
    "19": handle_about,
}


def interactive_mode():
    print_banner()
    console.print(Panel(
        "[bold red]⚠  LEGAL DISCLAIMER[/]\n\n"
        "[white]AADI is designed for authorized security testing ONLY.\n"
        "Use of this tool against systems you do not own or have explicit written\n"
        "permission to test is [bold red]ILLEGAL[/] and may result in criminal prosecution.\n"
        "The author assumes no liability for misuse.[/]",
        border_style="red", padding=(0, 2)))

    if not Confirm.ask("\n[bold red]I confirm I have authorization to test the target system[/]", default=False):
        console.print("[yellow]Exiting. Obtain proper authorization before testing.[/]")
        sys.exit(0)

    # Auto-reconnect to WiFi devices on startup (if enabled in config)
    config = load_config()
    if config.get("auto_reconnect_wifi", True):
        console.print()
        auto_reconnect_wifi()
        console.print()

    while True:
        console.print()
        print_main_menu()
        valid_choices = [num for num, *_ in MENU_OPTIONS]
        choice = Prompt.ask("\n[bold cyan]Aadi ▶[/]", choices=valid_choices, show_choices=False)

        if choice == "0":
            console.print("\n[bold magenta]👻 Exiting AADI. Stay ethical.[/]\n")
            sys.exit(0)

        handler = HANDLER_MAP.get(choice)
        if handler:
            try:
                console.print()
                handler()
            except KeyboardInterrupt:
                console.print("\n[yellow]↩ Returned to main menu.[/]")
            except Exception as e:
                console.print(f"\n[bold red]✗ Error:[/] {e}")
        else:
            console.print("[red]Invalid option.[/]")

        console.print()
        Prompt.ask("[dim]Press ENTER to continue[/]", default="")


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI MODE  (argparse)
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aadi",
        description=f"👻 Aadi v{VERSION} — Advanced Android Pentesting Tool by {AUTHOR}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 aadi.py --interactive
  python3 aadi.py --apk app.apk --report html
  python3 aadi.py --device ABC123 --vuln-scan --pkg com.example.app
  python3 aadi.py --device ABC123 --port-scan
  python3 aadi.py --payload reverse_tcp --lhost 10.0.0.1 --lport 4444
  python3 aadi.py --device ABC123 --exploit deep-link --pkg com.example --scheme myapp
  python3 aadi.py --devices
        """
    )

    p.add_argument("--interactive", "-i",  action="store_true",    help="Launch interactive menu mode")
    p.add_argument("--version",     "-v",  action="store_true",    help="Show version")

    # Device
    dg = p.add_argument_group("Device")
    dg.add_argument("--devices",           action="store_true",    help="List connected devices")
    dg.add_argument("--device", "-d",      metavar="SERIAL",       help="Target device serial number")
    dg.add_argument("--info",              action="store_true",    help="Show device info")
    dg.add_argument("--shell",             metavar="CMD",          help="Run ADB shell command")
    dg.add_argument("--adb-shell",         action="store_true",    help="Drop into interactive ADB shell")
    dg.add_argument("--adb-wifi",          action="store_true",    help="Enable ADB over WiFi")
    dg.add_argument("--screenshot",        action="store_true",    help="Capture device screenshot")
    dg.add_argument("--logcat",            metavar="N", type=int,  help="Capture N lines of logcat", nargs="?", const=200)
    dg.add_argument("--packages",          choices=["all","system","third_party","disabled"],
                                                                   help="List installed packages")
    dg.add_argument("--pull",              metavar="REMOTE",       help="Pull file from device")
    dg.add_argument("--push",             nargs=2, metavar=("LOCAL","REMOTE"), help="Push file to device")

    # APK Analysis
    ag = p.add_argument_group("APK Analysis")
    ag.add_argument("--apk",              metavar="FILE",          help="APK file to analyze")

    # Network
    ng = p.add_argument_group("Network")
    ng.add_argument("--port-scan",        action="store_true",    help="Port scan device IP")
    ng.add_argument("--target",           metavar="IP",           help="Explicit scan target IP")
    ng.add_argument("--ports",            metavar="PORTS",        help="Comma-separated ports or 'all'")
    ng.add_argument("--wifi-info",        action="store_true",    help="Show WiFi info")
    ng.add_argument("--discover",         metavar="SUBNET",       help="Discover hosts on subnet")
    ng.add_argument("--ssl-pinning",      metavar="PKG",          help="Check SSL pinning for package")
    ng.add_argument("--mitm-guide",       action="store_true",    help="Show MitM setup guide")

    # Vulnerability
    vg = p.add_argument_group("Vulnerability")
    vg.add_argument("--vuln-scan",        action="store_true",    help="Run full vulnerability scan")
    vg.add_argument("--pkg",             metavar="PKG",           help="Target package name")
    vg.add_argument("--cve-check",       action="store_true",     help="Check Android CVEs for device")
    vg.add_argument("--root-check",      action="store_true",     help="Check if device is rooted")

    # Exploit
    eg = p.add_argument_group("Exploit")
    eg.add_argument("--exploit",          metavar="MODULE",
                    choices=["activity","broadcast","provider","deep-link","frida","shell-drop","db-extract","lock-bypass","dev-options"],
                    help="Exploit module to run")
    eg.add_argument("--activity",         metavar="CLASS",        help="Activity class for --exploit activity")
    eg.add_argument("--action",           metavar="ACTION",       help="Intent action")
    eg.add_argument("--uri",              metavar="URI",          help="URI for content provider / deep link")
    eg.add_argument("--scheme",           metavar="SCHEME",       help="Deep link scheme")
    eg.add_argument("--lhost",            metavar="IP",           help="Listener host")
    eg.add_argument("--lport",            metavar="PORT", type=int, default=4444, help="Listener port")
    eg.add_argument("--db-name",          metavar="DB",           help="Database filename to extract")

    # Payload
    pg = p.add_argument_group("Payload")
    pg.add_argument("--payload",          metavar="TYPE",
                    choices=["reverse_tcp","reverse_https","reverse_http","shell_tcp",
                             "intent","reverse-shells","adb-script","obfuscate"],
                    help="Generate a payload")
    pg.add_argument("--payload-out",      metavar="FILE",         help="Output file for payload")
    pg.add_argument("--obfuscate-method", choices=["base64","hex"], default="base64",
                    help="Obfuscation method")
    pg.add_argument("--raw-payload",      metavar="CMD",          help="Payload string to obfuscate")

    # Report
    rg = p.add_argument_group("Report")
    rg.add_argument("--report",           choices=["html","json","both","table"],
                    help="Generate report after scan")
    rg.add_argument("--report-out",       metavar="FILE",         help="Report output filename")
    rg.add_argument("--target-name",      metavar="NAME",         help="Target name for report", default="Unknown Target")

    return p


def cli_mode(args):
    """Run CLI operations based on parsed arguments."""
    print_banner()

    device_id = args.device
    apk_data = {}

    # Version
    if args.version:
        console.print(f"[bold magenta]{TOOL_NAME}[/] v[bold cyan]{VERSION}[/] by [bold]{AUTHOR}[/]")
        return

    # Devices
    if args.devices:
        adb_manager.check_adb()
        adb_manager.list_devices()

    # Device info
    if args.info and device_id:
        adb_manager.device_info(device_id)

    # Shell command
    if args.shell and device_id:
        adb_manager.shell_cmd(device_id, args.shell)

    # Interactive ADB shell
    if args.adb_shell and device_id:
        adb_manager.interactive_shell(device_id)

    # ADB WiFi
    if args.adb_wifi and device_id:
        adb_manager.enable_adb_wifi(device_id, args.lport)

    # Screenshot
    if args.screenshot and device_id:
        adb_manager.take_screenshot(device_id)

    # Logcat
    if args.logcat is not None and device_id:
        adb_manager.capture_logcat(device_id, args.logcat)

    # Packages
    if args.packages and device_id:
        adb_manager.list_packages(device_id, args.packages)

    # Pull file
    if args.pull and device_id:
        adb_manager.pull_file(device_id, args.pull)

    # Push file
    if args.push and device_id:
        adb_manager.push_file(device_id, args.push[0], args.push[1])

    # APK Analysis
    if args.apk:
        apk_data = apk_analyzer.analyze_apk(args.apk)
        _save_to_session(apk_data, "apk")

    # Network
    if args.port_scan:
        target = args.target
        if not target and device_id:
            target = network_scanner.get_device_ip(device_id)
        if target:
            ports = None
            if args.ports == "all":
                ports = list(range(1, 65536))
            elif args.ports:
                ports = [int(p) for p in args.ports.split(",") if p.strip().isdigit()]
            network_scanner.port_scan(target, ports)
        else:
            console.print("[red]Provide --target or --device for port scan.[/]")

    if args.wifi_info and device_id:
        network_scanner.get_wifi_info(device_id)

    if args.discover:
        network_scanner.discover_devices(args.discover)

    if args.ssl_pinning and device_id:
        network_scanner.check_ssl_pinning(device_id, args.ssl_pinning)

    if args.mitm_guide:
        network_scanner.mitm_setup_guide()

    # Vulnerability
    if args.vuln_scan and device_id:
        report = vulnerability_scanner.full_vulnerability_scan(device_id, args.pkg)
        _save_to_session(report, "vuln")

    if args.cve_check and device_id:
        findings = vulnerability_scanner.check_android_version_cves(device_id)
        _save_to_session({"cves": findings}, "cve")

    if args.root_check and device_id:
        vulnerability_scanner.check_root_status(device_id)

    # Exploit
    if args.exploit and device_id:
        ex = args.exploit
        if ex == "activity":
            exploit_engine.launch_exported_activity(device_id, args.pkg, args.activity)
        elif ex == "broadcast":
            exploit_engine.trigger_broadcast_receiver(device_id, args.pkg, args.action)
        elif ex == "provider":
            exploit_engine.extract_content_provider(device_id, args.uri)
        elif ex == "deep-link":
            exploit_engine.deep_link_fuzzer(device_id, args.pkg, args.scheme)
        elif ex == "frida":
            exploit_engine.frida_injection_guide(args.pkg)
        elif ex == "shell-drop":
            exploit_engine.shell_payload_dropper(device_id, args.lhost, args.lport)
        elif ex == "db-extract":
            exploit_engine.extract_database(device_id, args.pkg, args.db_name)
        elif ex == "lock-bypass":
            exploit_engine.bypass_lock_screen(device_id)
        elif ex == "dev-options":
            exploit_engine.enable_developer_options(device_id)

    # Payload
    if args.payload:
        out = args.payload_out
        if args.payload in ("reverse_tcp","reverse_https","reverse_http","shell_tcp"):
            payload_generator.generate_msfvenom_apk(args.lhost, args.lport, args.payload, out or "payload.apk")
        elif args.payload == "intent":
            payload_generator.generate_intent_payload(args.action, args.pkg, args.uri)
        elif args.payload == "reverse-shells":
            payload_generator.generate_reverse_shell_commands(args.lhost, args.lport)
        elif args.payload == "adb-script":
            payload_generator.generate_adb_payload_script(device_id, args.lhost, args.lport, out or "adb_payload.sh")
        elif args.payload == "obfuscate":
            payload_generator.obfuscate_payload(args.raw_payload or "", args.obfuscate_method)

    # Report
    if args.report:
        data = _get_session()
        data["target"] = args.target_name
        if apk_data:
            data.update(apk_data)
        if args.report in ("html", "both"):
            out = args.report_out or "AADI_report.html"
            report_generator.generate_html_report(data, out)
        if args.report in ("json", "both"):
            out = args.report_out or "AADI_report.json"
            report_generator.generate_json_report(data, out)
        if args.report == "table":
            report_generator.print_summary_table(data)


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = build_parser()

    if len(sys.argv) == 1:
        # No args → interactive
        interactive_mode()
        return

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        cli_mode(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold magenta]👻 AADI interrupted. Stay ethical.[/]\n")
        sys.exit(0)