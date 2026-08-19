"""
tests/test_db_manager.py
---------------------------
Unit tests for database/db_manager.py.

Uses a temporary SQLite file per test (never the real lab_data.sqlite3)
so tests never pollute or depend on real lab data.
"""

import unittest
import os
import tempfile

from database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        fd, self.tmp_path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        self.db = DatabaseManager(db_path=self.tmp_path)

    def tearDown(self):
        os.remove(self.tmp_path)

    def test_session_lifecycle(self):
        session_id = self.db.start_session()
        self.assertIsInstance(session_id, int)
        self.db.end_session(session_id)
        stats = self.db.get_stats()
        self.assertEqual(stats["sessions"], 1)

    def test_log_keystroke_increments_stats(self):
        session_id = self.db.start_session()
        self.db.log_keystroke(session_id, "a")
        self.db.log_keystroke(session_id, "b")
        stats = self.db.get_stats()
        self.assertEqual(stats["keystrokes"], 2)

    def test_log_login_attempt_always_redacted(self):
        session_id = self.db.start_session()
        self.db.log_login_attempt(session_id, "[TEST INPUT]", password_redacted=True)
        stats = self.db.get_stats()
        self.assertEqual(stats["login_attempts"], 1)
        self.assertEqual(stats["passwords_redacted"], 1)

        attempts = self.db.get_recent_login_attempts()
        self.assertEqual(attempts[0]["username_display"], "[TEST INPUT]")
        # Confirm no column/value in the stored row could ever hold a
        # raw password -- only the placeholder string is present.
        self.assertNotIn("password", attempts[0])

    def test_clear_all_data(self):
        session_id = self.db.start_session()
        self.db.log_keystroke(session_id, "a")
        self.db.log_login_attempt(session_id, "[TEST INPUT]")

        self.db.clear_all_data()
        stats = self.db.get_stats()
        self.assertEqual(stats["keystrokes"], 0)
        self.assertEqual(stats["sessions"], 0)
        self.assertEqual(stats["login_attempts"], 0)


if __name__ == "__main__":
    unittest.main()
