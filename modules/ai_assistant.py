"""
Aadi — AI Vulnerability Triage & Remediation Assistant Module (Optimized & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import json
import difflib
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt

console = Console()

# ── Attack Chaining Rules ──────────────────────────────────────────────────────
ATTACK_CHAIN_RULES = [
    {
        "triggers": ["Exported Activity", "Insecure Data Storage"],
        "chain_name": "Privilege Escalation via Exported Component & Stolen Session",
        "description": "An attacker can invoke the exported activity directly using ADB/Intents, bypassing UI authentication, and extract sensitive session tokens from world-readable SharedPreferences/Databases.",
        "impact": "CRITICAL"
    },
    {
        "triggers": ["Backup Enabled", "Hardcoded Secrets"],
        "chain_name": "Full App Compromise via ADB Backup & Hardcoded Keys",
        "description": "Because allowBackup=true, an attacker can pull the app's unencrypted backup archive via 'adb backup', then extract hardcoded API keys or database credentials to impersonate users.",
        "impact": "HIGH"
    },
    {
        "triggers": ["Task Hijacking", "Exported Activity"],
        "chain_name": "StrandHogg Phishing / Activity Spoofing",
        "description": "Using a non-default taskAffinity, a malicious app can overlay a fake login screen on top of the target's exported activities when launched.",
        "impact": "HIGH"
    }
]

REMEDIATIONS_DB = {
    "Debuggable Application": (
        "// AndroidManifest.xml FIX:\n"
        "<application\n"
        "    android:debuggable=\"false\"\n"
        "    android:allowBackup=\"false\">\n"
        "</application>"
    ),
    "Exported Components": (
        "// AndroidManifest.xml FIX:\n"
        "<activity\n"
        "    android:name=\".TargetActivity\"\n"
        "    android:exported=\"false\">\n"
        "</activity>"
    ),
    "Insecure Data Storage": (
        "// Secure SharedPreferences storage implementation (Kotlin/Java):\n"
        "EncryptedSharedPreferences.create(\n"
        "    context,\n"
        "    \"secure_prefs_filename\",\n"
        "    masterKey,\n"
        "    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,\n"
        "    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM\n"
        ")"
    ),
    "Backup Enabled": (
        "// AndroidManifest.xml FIX:\n"
        "<application\n"
        "    android:allowBackup=\"false\">\n"
        "</application>"
    )
}


def triage_findings(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze findings and perform smart re-scoring and triage."""
    console.print(Panel("[bold cyan]🤖 AI Triage Engine analyzing findings...[/]", border_style="cyan"))

    triaged_results = {
        "critical_count": 0,
        "high_count": 0,
        "actionable_insights": [],
        "attack_chains": []
    }

    if not findings or not isinstance(findings, list):
        return triaged_results

    finding_names = [str(f.get("name", "")) for f in findings if isinstance(f, dict)]

    # Evaluate Attack Chains
    for rule in ATTACK_CHAIN_RULES:
        if all(trigger in finding_names for trigger in rule["triggers"]):
            triaged_results["attack_chains"].append(rule)

    # Smart Scoring & Insights
    for f in findings:
        if not isinstance(f, dict):
            continue
        sev = str(f.get("severity", "INFO")).upper()
        if sev == "CRITICAL":
            triaged_results["critical_count"] += 1
        elif sev == "HIGH":
            triaged_results["high_count"] += 1

    return triaged_results


def display_triage_report(findings: List[Dict[str, Any]]) -> None:
    """Display AI triage analysis and potential attack chains in a rich UI format."""
    if not findings:
        console.print("[yellow]No findings in session to triage. Run an APK analysis or Vulnerability scan first.[/]")
        return

    result = triage_findings(findings)

    console.print(Panel(
        f"[bold green]✓ Triage Complete[/]\n"
        f"  Critical Findings: [bold red]{result['critical_count']}[/]\n"
        f"  High Findings:     [bold yellow]{result['high_count']}[/]\n"
        f"  Potential Attack Chains Discovered: [bold magenta]{len(result['attack_chains'])}[/]",
        title="[bold]AI Security Triage Summary[/]",
        border_style="magenta"
    ))

    # Display Attack Chains if any
    if result["attack_chains"]:
        t = Table(title="[bold red]🔗 Automated Exploit Chaining Analysis[/]",
                  box=box.DOUBLE_EDGE, border_style="red", header_style="bold red")
        t.add_column("Attack Chain", style="cyan", width=25)
        t.add_column("Impact", style="red", width=12)
        t.add_column("Description & Exploit Path", style="white")

        for chain in result["attack_chains"]:
            t.add_row(
                chain["chain_name"],
                f"[bold red]{chain['impact']}[/]",
                chain["description"]
            )
        console.print(t)
    else:
        console.print("[green]✓ No multi-vector exploit chains identified from current findings.[/]")


def generate_custom_remediation(vuln_name: str) -> str:
    """Generate developer-ready code fixes for specific vulnerabilities with smart fuzzy matching."""
    if not vuln_name or not vuln_name.strip():
        console.print("[red]✗ Vulnerability name cannot be empty.[/]")
        return ""

    vuln_keys = list(REMEDIATIONS_DB.keys())

    # Exact match check
    fix = REMEDIATIONS_DB.get(vuln_name)
    matched_name = vuln_name

    # If exact match fails, use fuzzy matching to find closest valid vulnerability
    if not fix:
        matches = difflib.get_close_matches(vuln_name, vuln_keys, n=1, cutoff=0.3)
        if matches:
            matched_name = matches[0]
            fix = REMEDIATIONS_DB.get(matched_name)
            console.print(
                f"[yellow]ℹ Exact match not found for '{vuln_name}'. Showing closest match: '{matched_name}'[/]")

    if not fix:
        fix = "// General Recommendation:\nApply principle of least privilege, strict input validation, and proper cryptographic standards."
        matched_name = vuln_name

    console.print(Panel(fix, title=f"[bold green]🛡 Code Remediation for: {matched_name}[/]", border_style="green"))
    return fix


def ai_assistant_menu(session_data: Optional[Dict[str, Any]] = None) -> None:
    """Interactive AI Assistant Menu."""
    if session_data is None:
        session_data = {"findings": []}

    options = [
        ("1", "🧠", "Run AI Triage & Exploit Chaining", "Analyze session findings for multi-vector attacks"),
        ("2", "🛡", "Generate Custom Code Remediation", "Get developer-ready secure code snippets"),
        ("0", "↩️", "Back", "Return to main menu"),
    ]

    while True:
        console.print()
        t = Table(title="\n[bold magenta]🤖 AI Triage & Remediation Assistant[/]\n",
                  box=box.DOUBLE_EDGE, border_style="magenta", header_style="bold cyan")
        t.add_column("#", style="cyan", width=3)
        t.add_column("", style="", width=3)
        t.add_column("Feature", style="white", min_width=25)
        t.add_column("Description", style="dim")

        for num, icon, name, desc in options:
            t.add_row(num, icon, name, desc)

        console.print(t)

        choice = Prompt.ask("\n[bold cyan]AI Assistant ▶[/]", choices=[num for num, *_ in options], show_choices=False)

        if choice == "0":
            return
        elif choice == "1":
            findings = session_data.get("findings", [])
            display_triage_report(findings)
        elif choice == "2":
            vuln = Prompt.ask("[cyan]Enter vulnerability name (e.g. Exported Components, Debuggable Application)[/]")
            generate_custom_remediation(vuln)