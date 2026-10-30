"""
Aadi — Authentication Module (3-Attempt Cinematic Hacker Voice Edition)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import sys
import time
import os
import json
import pyttsx3
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "auth_config.json")


def speak_voice(text: str, rate_offset: int = -50):
    """
    Optimized Text-to-Speech engine configured to sound heavy, slow,
    and cinematic like a hacker terminal, with proper pronunciation pacing.
    """
    try:
        engine = pyttsx3.init()

        # आवाज की स्पीड को धीमा करें ताकि वह साफ और भारी (Cinematic) सुनाई दे
        current_rate = engine.getProperty('rate')
        engine.setProperty('rate', 130 if current_rate > 150 else current_rate + rate_offset)

        # वॉल्यूम को पूरा तेज रखें
        engine.setProperty('volume', 1.0)

        # एक बेहतरीन अंग्रेजी पुरुष/हैकर्स जैसी आवाज (Voice ID) खोजने की कोशिश
        voices = engine.getProperty('voices')
        for voice in voices:
            voice_desc = voice.name.lower()
            if "english" in voice_desc or "male" in voice_desc or "en-" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(text)
        engine.runAndWait()

        # क्रैश होने से बचाने के लिए इंजन को सुरक्षित रूप से बंद करें
        try:
            engine.stop()
        except:
            pass

    except Exception:
        # अगर सिस्टम में ऑडियो ड्राइवर या स्पीच उपलब्ध न हो, तो चुपचाप आगे बढ़ जाएं
        pass


def get_or_set_password() -> str:
    """Check if password is saved; if not, prompt user to set a new one."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("password", "Aadi@97621")
        except:
            pass

    # अगर पहली बार टूल चल रहा है और पासवर्ड सेट नहीं है
    console.print(
        Panel("[bold yellow]First Time Setup:[/] Please set a security passkey for AADI.", border_style="yellow"))
    new_pass = Prompt.ask("[cyan]Set Master Password[/]", password=True)
    confirm_pass = Prompt.ask("[cyan]Confirm Master Password[/]", password=True)

    if new_pass != confirm_pass:
        console.print("[red]Passwords do not match! Exiting.[/]")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"password": new_pass}, f)
        console.print("[green]✓ Password saved successfully![/]\n")
    except Exception as e:
        console.print(f"[red]Could not save password: {e}[/]")

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
            speak_voice("Access Granted. Welcome back, Sir.", rate_offset=-50)

            console.print("\n[bold green]⚡ ACCESS GRANTED[/]", justify="center")
            time.sleep(0.4)

            console.print("[bold cyan]╔════════════════════════════════════╗[/]", justify="center")
            console.print("[bold magenta]║       WELCOME BACK, SIR... 👻      ║[/]", justify="center")
            console.print("[bold cyan]╚════════════════════════════════════╝[/]", justify="center")
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
                sys.exit(1)  # तीनों प्रयास खत्म होने पर टूल हमेशा के लिए बंद

    return False