"""
Aadi — AI-Powered Vulnerability Triage & LLM Exploit Suggester
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import requests
import json
from rich.console import Console
from rich.panel import Panel

console = Console()


def analyze_vulnerabilities_with_ai(manifest_data: str, ollama_url: str = "http://localhost:11434/api/generate"):
    """Send manifest or static scan data to local LLM (Ollama) for AI security triage."""
    console.print(Panel("[cyan]Querying Local AI Model for Vulnerability Triage...[/]", border_style="magenta"))
    prompt = f"Analyze the following Android app manifest/components for security vulnerabilities and suggest exploitation vectors:\n\n{manifest_data}"

    try:
        payload = {"model": "llama3", "prompt": prompt, "stream": False}
        res = requests.post(ollama_url, json=payload, timeout=30)
        if res.status_code == 200:
            analysis = res.json().get("response", "No response from model.")
            console.print(Panel(analysis, title="[bold green]AI Security Analysis Report[/]", border_style="green"))
        else:
            console.print(f"[bold red]✗ AI Server error: {res.status_code}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to connect to AI backend (Ollama): {e}[/]")