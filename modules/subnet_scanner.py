"""
Aadi — Subnet ADB Scanner & Auto-Connect Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import socket
import subprocess
import threading
from queue import Queue
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box

console = Console()
print_lock = threading.Lock()


def _get_local_subnet() -> str:
    """Try to guess local subnet base (e.g. '192.168.1') from active interfaces."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        parts = local_ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}"
    except Exception:
        return "192.168.1"


def scan_adb_port(ip: str, port: int = 5555, timeout: float = 0.5) -> bool:
    """Check if ADB port is open on a specific IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception:
        return False


def subnet_scanner_worker(subnet: str, port: int, active_hosts: list):
    """Worker thread to scan IP addresses."""
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        if scan_adb_port(ip, port, timeout=0.3):
            with print_lock:
                active_hosts.append(ip)
                console.print(f"  [bold green][+] Found ADB Device:[/] {ip}:{port}")


def scan_network_for_adb(subnet_base: str = None, port: int = 5555) -> list:
    """Multithreaded subnet scanner for open ADB ports."""
    if not subnet_base:
        subnet_base = _get_local_subnet()

    console.print(Panel(
        f"[bold cyan]Scanning Subnet:[/] {subnet_base}.1/24\n"
        f"Target Port: [bold yellow]{port}[/] (Wireless ADB)",
        border_style="magenta",
        title="[bold]Subnet ADB Discovery[/]"
    ))

    active_hosts = []
    threads = []

    for i in range(1, 255):
        t = threading.Thread(target=subnet_scanner_worker, args=(subnet_base, port, active_hosts))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return active_hosts


def handle_subnet_adb_scan():
    """Interactive handler for subnet ADB scanning & connection."""
    console.rule("[bold magenta]🌐 Subnet ADB Scanner & Auto-Connect[/]")

    default_subnet = _get_local_subnet()
    subnet = Prompt.ask("[cyan]Enter subnet base (e.g. 192.168.1)[/]", default=default_subnet)
    port = IntPrompt.ask("[cyan]Enter ADB port[/]", default=5555)

    console.print("\n[yellow][*] Scanning network. Please wait...[/]\n")
    found_ips = scan_network_for_adb(subnet, port)

    if not found_ips:
        console.print("\n[bold red][-] No active wireless ADB devices found on this subnet.[/]")
        return

    console.print(f"\n[bold green]✓ Scan complete! Found {len(found_ips)} active host(s).[/]\n")

    t = Table(title="[bold cyan]Discovered ADB Targets[/]", box=box.SIMPLE_HEAVY, border_style="cyan")
    t.add_column("#", style="cyan", width=4)
    t.add_column("IP Address", style="bold white")
    t.add_column("Port", style="yellow")
    t.add_column("Status", style="green")

    for idx, ip in enumerate(found_ips, 1):
        t.add_row(str(idx), ip, str(port), "Port 5555 Open (Ready)")

    console.print(t)

    if Confirm.ask("[cyan]Would you like to connect to one of these devices now?[/]", default=True):
        choice = IntPrompt.ask(f"[cyan]Enter device number (1-{len(found_ips)})[/]", default=1)
        if 1 <= choice <= len(found_ips):
            target_ip = found_ips[choice - 1]
            console.print(f"[cyan]Connecting to {target_ip}:{port}...[/]")

            res = subprocess.run(["adb", "connect", f"{target_ip}:{port}"], capture_output=True, text=True)
            if "connected" in res.stdout.lower():
                console.print(f"[bold green]✓ Successfully connected to {target_ip}:{port} wirelessly![/]")
            else:
                console.print(f"[red]Connection output: {res.stdout.strip()}[/]")
        else:
            console.print("[red]Invalid selection.[/]")