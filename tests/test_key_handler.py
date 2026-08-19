"""
tests/test_key_handler.py
----------------------------
Unit tests for monitor/key_event_handler.py.

Verifies two safety-critical behaviors:
  1. No events are ever produced while monitoring is stopped (default
     state on launch), even if something calls the handler.
  2. Once started, events are correctly labeled and flagged, and
     stopping immediately halts further processing.
"""

import unittest
from monitor.key_event_handler import KeyEventHandler


class FakeTkEvent:
    """Minimal stand-in for a Tkinter key event, avoids needing a real GUI."""

    def __init__(self, keysym):
        self.keysym = keysym


class TestKeyEventHandler(unittest.TestCase):
    def setUp(self):
        self.handler = KeyEventHandler()

    def test_inactive_by_default(self):
        self.assertFalse(self.handler.is_active)

    def test_no_events_processed_before_start(self):
        event = FakeTkEvent("a")
        result = self.handler.process(event)
        self.assertIsNone(result)

    def test_events_processed_after_start(self):
        self.handler.start()
        result = self.handler.process(FakeTkEvent("a"))
        self.assertIsNotNone(result)
        self.assertEqual(result.key_label, "a")
        self.assertTrue(result.is_printable)

    def test_special_key_labeling(self):
        self.handler.start()
        result = self.handler.process(FakeTkEvent("BackSpace"))
        self.assertEqual(result.key_label, "Backspace")
        self.assertFalse(result.is_printable)

    def test_stop_halts_processing_immediately(self):
        self.handler.start()
        self.assertIsNotNone(self.handler.process(FakeTkEvent("a")))

        self.handler.stop()
        self.assertIsNone(self.handler.process(FakeTkEvent("b")))
        self.assertFalse(self.handler.is_active)

    def test_restart_resumes_processing(self):
        self.handler.start()
        self.handler.stop()
        self.handler.start()
        result = self.handler.process(FakeTkEvent("x"))
        self.assertIsNotNone(result)
        self.assertEqual(result.key_label, "x")

    def test_process_keysym_convenience_method(self):
        self.handler.start()
        result = self.handler.process_keysym("Return")
        self.assertEqual(result.key_label, "Enter")

    def test_process_keysym_inactive(self):
        result = self.handler.process_keysym("a")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
