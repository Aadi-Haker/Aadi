"""
Aadi — Authentication Module (3-Attempt Cinematic Hacker Voice Edition - Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import sys
import time
import os
import json
import pyttsx3
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "auth_config.json")


def speak_voice(text: str, rate_offset: int = -50) -> None:
    """
    Optimized Text-to-Speech engine configured to sound heavy, slow,
    and cinematic like a hacker terminal, with proper pronunciation pacing.
    """
    try:
        engine = pyttsx3.init()
        if not engine:
            return

        current_rate = engine.getProperty('rate')
        engine.setProperty('rate', 130 if current_rate > 150 else current_rate + rate_offset)

        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        for voice in voices:
            voice_desc = voice.name.lower()
            if "english" in voice_desc or "male" in voice_desc or "en-" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(text)
        engine.runAndWait()

        try:
            engine.stop()
        except Exception:
            pass

    except Exception:
        pass


def get_or_set_password() -> str:
    """Check if password is saved securely; if not, prompt user to set a new one."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                saved_pass = data.get("password")
                if saved_pass:
                    return saved_pass
        except json.JSONDecodeError:
            console.print("[yellow]⚠ Auth config file corrupted. Re-setting master password.[/]")
        except Exception as e:
            console.print(f"[yellow]⚠ Error reading auth config: {e}[/]")

    # अगर पहली बार टूल चल रहा है या फाइल करप्ट है
    console.print(
        Panel("[bold yellow]First Time Setup:[/] Please set a security passkey for AADI.", border_style="yellow"))

    while True:
        new_pass = Prompt.ask("[cyan]Set Master Password[/]", password=True)
        confirm_pass = Prompt.ask("[cyan]Confirm Master Password[/]", password=True)

        if new_pass == confirm_pass and len(new_pass) > 0:
            break
        console.print("[red]Passwords do not match or empty! Try again.[/]")

    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"password": new_pass}, f, indent=2)
        console.print("[green]✓ Password saved successfully![/]\n")
    except Exception as e:
        console.print(f"[red]Could not save password: {e}[/]")
        sys.exit(1)

    return new_pass


def verify_or_setup_auth() -> bool:
    """
    Password authentication with 3-attempt limit, cinematic voice alerts,
    and automatic self-destruction/lockout on maximum failures.
    """
    MASTER_PASSWORD = get_or_set_password()
    max_attempts = 3

    console.print(Panel(
        "[bold cyan]🔐 AADI Security Gateway — Authentication Required[/]\n"
        "[dim]Warning: 3 failed attempts will trigger absolute session lockdown.[/]",
        border_style="magenta", padding=(0, 2)
    ))

    for attempt in range(1, max_attempts + 1):
        remaining = max_attempts - attempt
        entered_password = Prompt.ask(f"[cyan]Enter Security Passkey (Attempt {attempt}/{max_attempts})[/]",
                                      password=True)

        if entered_password == MASTER_PASSWORD:
            # सही पासवर्ड डालने पर
            speak_voice("Access Granted. Welcome back, Sir Aadi.", rate_offset=-50)

            console.print("\n[bold green]⚡ ACCESS GRANTED[/]", justify="center")
            time.sleep(0.4)

            console.print("[bold cyan]   ╔════════════════════════════════════╗[/]", justify="center")
            console.print("[bold magenta]║    WELCOME BACK, SIR... Aadi 👻    ║[/]", justify="center")
            console.print("[bold cyan]   ╚════════════════════════════════════╝[/]", justify="center")
            time.sleep(0.8)
            return True
        else:
            if remaining > 0:
                # गलत पासवर्ड, लेकिन अभी मौके बाकी हैं
                speak_voice("Wrong password. Try again.", rate_offset=-40)
                console.print(f"\n[bold yellow]✖ Wrong password! {remaining} attempt(s) remaining.[/]",
                              justify="center")
                time.sleep(0.5)
            else:
                # 3 बार गलत पासवर्ड डालने पर आखिरी बार ब्लॉक करना
                speak_voice("Access Denied. Intrusion detected. Terminating tool.", rate_offset=-40)

                console.print("\n[bold red]✖ ACCESS DENIED — MAXIMUM ATTEMPTS EXCEEDED![/]", justify="center")
                console.print("[dim red]Intrusion lockout engaged. Purging memory and self-destructing...[/]",
                              justify="center")

                with console.status("[bold red]Locking down AADI framework...", spinner="earth"):
                    time.sleep(2.0)

                console.print("[bold red][-] Tool session destroyed. Goodbye.[/]")
                sys.exit(1)

    return False