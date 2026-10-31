"""
Aadi — Subnet ADB Scanner & Auto-Connect Module (Optimized, Thread-Safe & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import socket
import subprocess
import threading
import concurrent.futures
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box

console = Console()
print_lock = threading.Lock()


def _get_local_subnet() -> str:
    """Try to guess local subnet base (e.g. '192.168.1') from active interfaces securely."""
    s: Optional[socket.socket] = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        parts = local_ip.split(".")
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}"
    except Exception:
        pass
    finally:
        if s:
            try:
                s.close()
            except Exception:
                pass
    return "192.168.1"


def scan_adb_port(ip: str, port: int = 5555, timeout: float = 0.3) -> bool:
    """Check if ADB port is open on a specific IP securely."""
    s: Optional[socket.socket] = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        return result == 0
    except Exception:
        return False
    finally:
        if s:
            try:
                s.close()
            except Exception:
                pass


def scan_network_for_adb(subnet_base: Optional[str] = None, port: int = 5555, max_workers: int = 50) -> List[str]:
    """Multithreaded subnet scanner for open ADB ports using ThreadPoolExecutor."""
    if not subnet_base or not subnet_base.strip():
        subnet_base = _get_local_subnet()

    console.print(Panel(
        f"[bold cyan]Scanning Subnet:[/] {subnet_base}.1/24\n"
        f"Target Port: [bold yellow]{port}[/] (Wireless ADB)",
        border_style="magenta",
        title="[bold]Subnet ADB Discovery[/]"
    ))

    active_hosts: List[str] = []

    def _worker(ip_addr: str) -> None:
        if scan_adb_port(ip_addr, port, timeout=0.3):
            with print_lock:
                active_hosts.append(ip_addr)
                console.print(f"  [bold green][+] Found ADB Device:[/] {ip_addr}:{port}")

    # Generate all IP addresses in the /24 subnet (1 to 254)
    ip_list = [f"{subnet_base}.{i}" for i in range(1, 255)]

    with console.status(f"[cyan]Scanning {len(ip_list)} hosts on port {port}...[/]"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(_worker, ip_list)

    return sorted(active_hosts)


def handle_subnet_adb_scan() -> None:
    """Interactive handler for subnet ADB scanning & connection."""
    console.rule("[bold magenta]🌐 Subnet ADB Scanner & Auto-Connect[/]")

    default_subnet = _get_local_subnet()
    subnet = Prompt.ask("[cyan]Enter subnet base (e.g. 192.168.1)[/]", default=default_subnet)
    port = IntPrompt.ask("[cyan]Enter ADB port[/]", default=5555)

    if not (1 <= port <= 65535):
        console.print("[bold red]✗ Invalid port number.[/]")
        return

    console.print("\n[yellow][*] Scanning network. Please wait...[/]\n")
    found_ips = scan_network_for_adb(subnet.strip(), port)

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
        t.add_row(str(idx), ip, str(port), f"Port {port} Open (Ready)")

    console.print(t)

    if Confirm.ask("[cyan]Would you like to connect to one of these devices now?[/]", default=True):
        choice = IntPrompt.ask(f"[cyan]Enter device number (1-{len(found_ips)})[/]", default=1)
        if 1 <= choice <= len(found_ips):
            target_ip = found_ips[choice - 1]
            console.print(f"[cyan]Connecting to {target_ip}:{port}...[/]")

            try:
                res = subprocess.run(["adb", "connect", f"{target_ip}:{port}"], capture_output=True, text=True, timeout=10)
                output_str = res.stdout.strip()
                if "connected" in output_str.lower() or "already connected" in output_str.lower():
                    console.print(f"[bold green]✓ Successfully connected to {target_ip}:{port} wirelessly![/]")
                else:
                    console.print(f"[red]Connection output: {output_str}[/]")
            except subprocess.TimeoutExpired:
                console.print("[bold red]✗ ADB connection request timed out.[/]")
            except FileNotFoundError:
                console.print("[bold red]✗ 'adb' command not found in system PATH.[/]")
            except Exception as e:
                console.print(f"[bold red]✗ Connection error: {e}[/]")
        else:
            console.print("[red]Invalid selection.[/]")