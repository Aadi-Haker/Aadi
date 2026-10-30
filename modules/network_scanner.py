"""
AADI — Network Scanner Module (Enhanced & Cross-Version Robust)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import subprocess
import re
import socket
import shutil
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

console = Console()

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5555: "ADB",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt2", 27017: "MongoDB", 9200: "Elasticsearch",
    4444: "Metasploit", 1099: "RMI", 8161: "ActiveMQ",
}


def _run_adb(args: list, device_id: str = None):
    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except Exception:
        return ""


def get_device_ip(*args, **kwargs):
    """Get device IP robustly across modern Android versions (safe with any arguments)."""
    device_id = args[0] if args and isinstance(args[0], str) else kwargs.get('device_id', None)

    # Method 1: Check ip addr show wlan0 or general ip addr
    out = _run_adb(["shell", "ip -4 addr show"], device_id)
    match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/\d+.*?(?:wlan0|eth0|ap0)", out)
    if match:
        ip = match.group(1)
        console.print(f"[green]Device IP Found:[/] {ip}")
        return ip

    # Fallback to general inet grep
    matches = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)/\d+", out)
    for ip in matches:
        if not ip.startswith("127."):
            console.print(f"[green]Device IP Found:[/] {ip}")
            return ip

    # Method 2: ip route
    out_route = _run_adb(["shell", "ip route"], device_id)
    match_route = re.search(r"src\s+(\d+\.\d+\.\d+\.\d+)", out_route)
    if match_route:
        ip = match_route.group(1)
        console.print(f"[green]Device IP Found:[/] {ip}")
        return ip

    console.print("[yellow]Could not automatically fetch device IP via ADB.[/]")
    return None


def get_wifi_info(*args, **kwargs):
    """Retrieve WiFi connection details safely."""
    device_id = args[0] if args and isinstance(args[0], str) else kwargs.get('device_id', None)
    info = {}
    wpa = _run_adb(["shell", "wpa_cli status"], device_id)
    dumpsys = _run_adb(["shell", "dumpsys wifi | grep -E 'SSID|BSSID|freq|rssi|ip_address'"], device_id)

    for line in (wpa + "\n" + dumpsys).splitlines():
        if "=" in line:
            kv = line.strip().split("=", 1)
        elif ":" in line:
            kv = line.strip().split(":", 1)
        else:
            continue

        if len(kv) == 2:
            k, v = kv[0].strip().lower(), kv[1].strip()
            if "ssid" in k and "bssid" not in k:
                info["SSID"] = v.strip('"')
            elif "bssid" in k:
                info["BSSID"] = v
            elif "freq" in k:
                info["Frequency"] = v + " MHz"
            elif "rssi" in k or "signal" in k:
                info["Signal"] = v + " dBm"
            elif "ip_address" in k or (k == "ip_address"):
                info["IP"] = v
            elif "security" in k or "key_mgmt" in k:
                info["Security"] = v

    table = Table(title="[bold magenta]📶 WiFi Info[/]", box=box.SIMPLE, border_style="cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    for k, v in info.items():
        table.add_row(k, v)
    console.print(table)
    return info


def _scan_port(host: str, port: int, timeout: float = 0.8) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def port_scan(target: str = None, ports: list = None, timeout: float = 0.8, max_workers: int = 100):
    """Fast multithreaded port scanner."""
    if not target:
        target = Prompt.ask("[cyan]Enter target IP or hostname to scan[/]", default="127.0.0.1")

    if ports is None:
        ports = list(COMMON_PORTS.keys())

    console.print(Panel(f"[bold cyan]Port Scanning:[/] {target}  ({len(ports)} ports)", border_style="magenta"))
    open_ports = []

    with console.status(f"[cyan]Scanning {len(ports)} ports on {target}...[/]"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(_scan_port, target, p, timeout): p for p in ports}
            for fut in concurrent.futures.as_completed(futures):
                port = futures[fut]
                if fut.result():
                    open_ports.append(port)

    open_ports.sort()
    table = Table(title=f"[bold green]Open Ports on {target}[/]", box=box.SIMPLE_HEAVY,
                  border_style="green", header_style="bold green")
    table.add_column("Port", style="cyan", width=8)
    table.add_column("Service", style="white")
    table.add_column("Risk", style="red")

    risky = {21, 23, 3389, 5900, 4444, 1099, 5555}
    for p in open_ports:
        svc = COMMON_PORTS.get(p, "Unknown")
        risk = "[bold red]HIGH[/]" if p in risky else (
            "[yellow]MEDIUM[/]" if p in {80, 8080, 27017, 6379} else "[green]LOW[/]")
        table.add_row(str(p), svc, risk)

    if open_ports:
        console.print(table)
    else:
        console.print("[yellow]No open ports found in the scanned range.[/]")

    if 5555 in open_ports:
        console.print(Panel(
            "[bold red]⚠  ADB port 5555 is OPEN![/]\n"
            f"The device may be exploitable via: [bold yellow]adb connect {target}:5555[/]",
            border_style="red"))

    return open_ports


def discover_devices(*args, **kwargs):
    """Wrapper function to discover active hosts/devices or run port scan safely."""
    console.rule("[bold magenta]🔍 Network & Host Discovery[/]")
    subnet = Prompt.ask("[cyan]Enter target subnet or IP for scan[/]", default="192.168.1.1/24")

    if shutil.which("nmap"):
        console.print(f"[green][*] Running nmap host discovery on {subnet}...[/]")
        try:
            subprocess.run(["nmap", "-sn", subnet])
        except KeyboardInterrupt:
            console.print("\n[yellow]Scan interrupted.[/]")
    else:
        port_scan()


def mitm_setup_guide(*args, **kwargs):
    """Print a guide for setting up MitM with mitmproxy."""
    guide = """
[bold magenta]── MitM Proxy Setup Guide ──────────────────────────────────[/]

[bold cyan]1. Install mitmproxy:[/]
   pip install mitmproxy

[bold cyan]2. Start transparent proxy:[/]
   mitmproxy --mode transparent --showhost

[bold cyan]3. On device (ADB shell, requires root or WiFi proxy):[/]
   adb shell settings put global http_proxy <your-ip>:8080

[bold cyan]4. Install mitmproxy CA cert on device:[/]
   Browse to http://mitm.it from the device

[bold cyan]5. For SSL Pinning bypass, use Frida + objection:[/]
   objection -g <package_name> explore
   android sslpinning disable

[bold cyan]6. Capture traffic:[/]
   mitmweb --mode transparent
    """
    console.print(Panel(guide, title="[bold]MitM Setup Guide[/]", border_style="cyan"))


def network_scanner_menu(*args, **kwargs):
    """Main menu wrapper for network scanner module."""
    while True:
        console.rule("[bold cyan]Network & Device Scanner Menu[/]")
        console.print("[1] Discover Active Hosts / Port Scan")
        console.print("[2] Get Connected Device IP")
        console.print("[3] Get WiFi Connection Info")
        console.print("[4] MitM Setup Guide")
        console.print("[0] Back to Main Menu")

        choice = Prompt.ask("[cyan]Select option[/]", choices=["1", "2", "3", "4", "0"], default="1")

        if choice == "1":
            discover_devices()
        elif choice == "2":
            get_device_ip()
        elif choice == "3":
            get_wifi_info()
        elif choice == "4":
            mitm_setup_guide()
        elif choice == "0":
            break