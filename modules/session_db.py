"""
Aadi — SQLite Session Database Module
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "aadi_sessions.db")


def init_db():
    """Initialize the SQLite database and tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sessions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       target_name
                       TEXT,
                       timestamp
                       TEXT,
                       data
                       TEXT
                   )
                   """)
    conn.commit()
    conn.close()


def save_session_to_db(target_name: str, session_data: dict) -> int:
    """Save current session data into SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_json = json.dumps(session_data)
    cursor.execute(
        "INSERT INTO sessions (target_name, timestamp, data) VALUES (?, ?, ?)",
        (target_name, timestamp, data_json)
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id


def load_latest_session() -> dict:
    """Load the most recent session from database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM sessions ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return {"findings": [], "permissions": [], "secrets": [], "urls": []}


def list_all_saved_sessions():
    """List all previous scan sessions stored in DB."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, target_name, timestamp FROM sessions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def handle_session_history():
    """Interactive handler to view or load previous sessions."""
    from rich.console import Console
    from rich.table import Table
    from rich import box
    from rich.prompt import Prompt, IntPrompt

    console = Console()
    console.rule("[bold magenta]📂 Session History & Database[/]")

    sessions = list_all_saved_sessions()
    if not sessions:
        console.print("[yellow]No saved sessions found in database yet.[/]")
        return

    t = Table(title="[bold cyan]Saved Audit Sessions[/]", box=box.ROUNDED, border_style="cyan")
    t.add_column("ID", style="cyan", width=4)
    t.add_column("Target Name", style="bold white")
    t.add_column("Timestamp", style="yellow")

    for s_id, target, ts in sessions:
        t.add_row(str(s_id), target, ts)

    console.print(t)
    console.print("[dim]Sessions are automatically saved after APK analysis or vulnerability scans.[/]")