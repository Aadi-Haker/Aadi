"""
Aadi — SQLite Session Database Module (Optimized, Robust & Secured)
Author: Aaditya Kumar Pandey | Instagram: @aadi_97621
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "aadi_sessions.db")


def init_db() -> None:
    """Initialize the SQLite database and tables securely."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_name TEXT,
                    timestamp TEXT,
                    data TEXT
                )
            """)
            conn.commit()
    except Exception as e:
        print(f"[-] Database initialization error: {e}")


def save_session_to_db(target_name: str, session_data: Dict[str, Any]) -> int:
    """Save current session data into SQLite database."""
    init_db()
    session_id = -1
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_json = json.dumps(session_data, default=str)
            cursor.execute(
                "INSERT INTO sessions (target_name, timestamp, data) VALUES (?, ?, ?)",
                (target_name, timestamp, data_json)
            )
            conn.commit()
            session_id = cursor.lastrowid
    except Exception as e:
        print(f"[-] Error saving session to DB: {e}")
    return session_id


def load_latest_session() -> Dict[str, Any]:
    """Load the most recent session from database."""
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM sessions ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row and row[0]:
                return json.loads(row[0])
    except Exception as e:
        print(f"[-] Error loading latest session: {e}")
    return {"findings": [], "permissions": [], "secrets": [], "urls": []}


def load_session_by_id(session_id: int) -> Optional[Dict[str, Any]]:
    """Load a specific session by its ID from the database."""
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM sessions WHERE id = ?", (session_id,))
            row = cursor.fetchone()
            if row and row[0]:
                return json.loads(row[0])
    except Exception as e:
        print(f"[-] Error loading session {session_id}: {e}")
    return None


def list_all_saved_sessions() -> List[Tuple[int, str, str]]:
    """List all previous scan sessions stored in DB."""
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, target_name, timestamp FROM sessions ORDER BY id DESC")
            return cursor.fetchall()
    except Exception as e:
        print(f"[-] Error listing sessions: {e}")
        return []


def handle_session_history() -> None:
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