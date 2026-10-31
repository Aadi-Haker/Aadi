"""
Aadi — AI-Powered Vulnerability Triage & LLM Exploit Suggester (Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import requests
import json
from typing import Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


def analyze_vulnerabilities_with_ai(
        manifest_data: str,
        ollama_url: str = "http://localhost:11434/api/generate",
        model_name: str = "llama3",
        timeout_sec: int = 120
) -> Optional[str]:
    """Send manifest or static scan data to local LLM (Ollama) for AI security triage with robust error handling."""
    if not manifest_data or not manifest_data.strip():
        console.print("[bold red]✗ Error: Manifest data is empty or invalid.[/]")
        return None

    # Limit payload length to prevent model context overload if extremely large
    max_chars = 12000
    if len(manifest_data) > max_chars:
        console.print("[yellow]⚠ Manifest data is very large; trimming to fit model context window.[/]")
        manifest_data = manifest_data[:max_chars] + "\n[... truncated ...]"

    console.print(
        Panel(f"[cyan]Querying Local AI Model ({model_name}) for Vulnerability Triage...[/]", border_style="magenta"))

    prompt = (
        "You are an expert Android Security and Penetration Testing assistant. "
        "Analyze the following Android app manifest/components for security misconfigurations, "
        "vulnerabilities (e.g., exported components, weak permissions, cleartext traffic), "
        "and suggest precise exploitation vectors:\n\n"
        f"{manifest_data}"
    )

    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2  # Lower temperature for deterministic security analysis
            }
        }

        res = requests.post(ollama_url, json=payload, timeout=timeout_sec)

        if res.status_code == 200:
            data = res.json()
            analysis = data.get("response", "No response text found from model.")
            console.print(Panel(analysis, title="[bold green]AI Security Analysis Report[/]", border_style="green"))
            return analysis
        else:
            console.print(f"[bold red]✗ AI Server error: Status code {res.status_code} - {res.text}[/]")
            return None

    except requests.exceptions.Timeout:
        console.print(
            f"[bold red]✗ Request timed out after {timeout_sec} seconds. The model might be busy or processing a large payload.[/]")
    except requests.exceptions.ConnectionError:
        console.print(
            f"[bold red]✗ Failed to connect to Ollama at {ollama_url}. Make sure Ollama is running (`ollama serve`).[/]")
    except requests.exceptions.RequestException as re_err:
        console.print(f"[bold red]✗ HTTP Request failed: {re_err}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Unexpected error during AI triage: {e}[/]")

    return None