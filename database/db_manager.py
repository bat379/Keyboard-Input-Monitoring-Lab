"""
database/db_manager.py
-----------------------
SECURITY CONCEPT: Local-only, minimal-data storage.

Real-world credential-stealing malware typically exfiltrates captured data
to a remote server. This lab deliberately does the opposite:

  1. All data is written to a SQLite file that lives on the *local disk only*
     (no network sockets are ever opened by this module).
  2. Only synthetic/test data is stored — the schema has no column capable
     of holding a real password, because the password value is redacted
     *before* it ever reaches this module (see monitor/redactor.py).
  3. A one-click "Clear Test Data" operation exists so a trainee can wipe
     the lab's local database at any time (real spyware hides this
     capability from its victim; a training tool exposes it front-and-
     center).

This module is intentionally "dumb": it does not know anything about
keyboard hooking. It only persists rows it is given.
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

# The DB lives next to this file inside the project folder, not in some
# hidden/system directory. Educational tools should be easy to inspect
# and easy to delete -- the opposite of stealthy malware behavior.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab_data.sqlite3")


class DatabaseManager:
    """Handles all persistence for the Keyboard Input Monitoring Lab."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_schema()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self):
        """
        Creates the tables if they don't already exist.

        Note the schema itself enforces the "no real secrets" design goal:
        there is no column named `password` or similar that stores raw
        text tied to a login attempt -- only a boolean `redacted` flag and
        a fixed placeholder string are ever written for password data.
        """
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS keystrokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    key_label TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    username_display TEXT NOT NULL,
                    password_redacted INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
                """
            )

    # ---------------------------------------------------------------
    # Session lifecycle
    # ---------------------------------------------------------------
    def start_session(self) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO sessions (start_time) VALUES (?)",
                (datetime.now().isoformat(timespec="seconds"),),
            )
            return cur.lastrowid

    def end_session(self, session_id: int):
        with self._connect() as conn:
            conn.execute(
                "UPDATE sessions SET end_time = ? WHERE id = ?",
                (datetime.now().isoformat(timespec="seconds"), session_id),
            )

    # ---------------------------------------------------------------
    # Keystroke logging (Monitor tab / Safe Test Mode username field only)
    # ---------------------------------------------------------------
    def log_keystroke(self, session_id: int, key_label: str):
        """
        Stores a single labeled key event, e.g. "a", "Space", "Backspace".

        Only ever called for keystrokes typed into the lab's OWN test
        widgets while they hold input focus (see monitor/key_event_handler.py).
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO keystrokes (session_id, key_label, timestamp) VALUES (?, ?, ?)",
                (session_id, key_label, datetime.now().isoformat(timespec="seconds")),
            )

    # ---------------------------------------------------------------
    # Simulated login attempts (Safe Test Mode)
    # ---------------------------------------------------------------
    def log_login_attempt(self, session_id: int, username_display: str, password_redacted: bool = True):
        """
        Stores an educational record of a *simulated* login submission.

        `username_display` is expected to already be a safe placeholder
        (e.g. "[TEST INPUT]") produced by monitor/redactor.py -- this
        method does not perform redaction itself, it just persists what
        it's given, so redaction must happen upstream, close to capture.
        """
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO login_attempts (session_id, timestamp, username_display, password_redacted)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session_id,
                    datetime.now().isoformat(timespec="seconds"),
                    username_display,
                    1 if password_redacted else 0,
                ),
            )

    # ---------------------------------------------------------------
    # Dashboard statistics
    # ---------------------------------------------------------------
    def get_stats(self) -> dict:
        with self._connect() as conn:
            keystroke_count = conn.execute("SELECT COUNT(*) AS c FROM keystrokes").fetchone()["c"]
            session_count = conn.execute("SELECT COUNT(*) AS c FROM sessions").fetchone()["c"]
            login_count = conn.execute("SELECT COUNT(*) AS c FROM login_attempts").fetchone()["c"]
            redacted_count = conn.execute(
                "SELECT COUNT(*) AS c FROM login_attempts WHERE password_redacted = 1"
            ).fetchone()["c"]
        return {
            "keystrokes": keystroke_count,
            "sessions": session_count,
            "login_attempts": login_count,
            "passwords_redacted": redacted_count,
        }

    def get_recent_keystrokes(self, limit: int = 200):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT key_label, timestamp FROM keystrokes ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_recent_login_attempts(self, limit: int = 100):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT username_display, password_redacted, timestamp
                FROM login_attempts ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    # ---------------------------------------------------------------
    # Clear Test Data
    # ---------------------------------------------------------------
    def clear_all_data(self):
        """
        Wipes every table. Exposed directly in the GUI as a big, obvious
        button -- a deliberate contrast with real spyware, which hides
        its stored data from the user rather than offering to erase it.
        """
        with self._connect() as conn:
            conn.execute("DELETE FROM keystrokes")
            conn.execute("DELETE FROM login_attempts")
            conn.execute("DELETE FROM sessions")
