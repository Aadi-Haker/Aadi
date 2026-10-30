"""
AADI — Authentication & Master Password Security Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
import json
import hashlib
import getpass
from rich.console import Console
from rich.panel import Panel

console = Console()

# File to store the hashed master password securely within the module directory
AUTH_FILE = os.path.join(os.path.dirname(__file__), ".auth_cache.json")


def _hash_password(password: str) -> str:
    """Generate a secure SHA-256 hash of the master password."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_or_setup_auth() -> bool:
    """
    Checks if a master password is already set.
    If not, guides the user to create a new one.
    If set, prompts the user to enter the password to authenticate.
    Returns True if authentication succeeds, False otherwise.
    """
    # Check if auth file exists
    if not os.path.exists(AUTH_FILE):
        console.print(Panel(
            "[bold cyan]🔐 AADI Security Setup — First Time Configuration[/]\n\n"
            "[white]No master password found. Please set a strong master password\n"
            "to protect your AADI penetration testing framework.[/]",
            border_style="cyan"
        ))

        while True:
            pwd1 = getpass.getpass("Enter new master password: ")
            pwd2 = getpass.getpass("Confirm master password: ")

            if not pwd1:
                console.print("[red]Password cannot be empty. Try again.[/]")
                continue

            if pwd1 != pwd2:
                console.print("[bold red]✗ Passwords do not match. Try again.[/]")
                continue

            # Save hashed password
            data = {"password_hash": _hash_password(pwd1)}
            try:
                with open(AUTH_FILE, "w") as f:
                    json.dump(data, f)
                console.print("[bold green]✔ Master password successfully configured![/]\n")
                return True
            except Exception as e:
                console.print(f"[bold red]✗ Failed to save password file:[/] {e}")
                return False
    else:
        # Prompt for existing password
        console.print(Panel(
            "[bold cyan]🔒 AADI Secure Authentication[/]\n\n"
            "[dim]Please enter your master password to unlock the framework.[/]",
            border_style="cyan"
        ))

        # Allow 3 attempts
        attempts = 3
        while attempts > 0:
            pwd = getpass.getpass("Enter master password: ")

            try:
                with open(AUTH_FILE, "r") as f:
                    data = json.load(f)

                if _hash_password(pwd) == data.get("password_hash"):
                    console.print("[bold green]✔ Authentication successful! Access granted.[/]\n")
                    return True
                else:
                    attempts -= 1
                    console.print(f"[bold red]✗ Incorrect password. Attempts remaining: {attempts}[/]")
            except Exception as e:
                console.print(f"[bold red]✗ Error reading auth file:[/] {e}")
                return False

        console.print("[bold red]✗ Maximum authentication attempts exceeded. Exiting...[/]")
        return False