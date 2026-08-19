"""
tests/test_redactor.py
------------------------
Unit tests for the redaction logic in monitor/redactor.py.

These tests are the automated proof behind the lab's central safety
claim: no matter what is typed into the password field, the raw value
never survives past redact_password().
"""

import unittest
from monitor.redactor import (
    redact_password,
    display_username,
    format_key_label,
    PASSWORD_PLACEHOLDER,
    TEST_INPUT_PLACEHOLDER,
)


class TestRedactPassword(unittest.TestCase):
    def test_returns_fixed_placeholder(self):
        self.assertEqual(redact_password("hunter2"), PASSWORD_PLACEHOLDER)

    def test_never_leaks_raw_value_regardless_of_content(self):
        sensitive_samples = [
            "CorrectHorseBatteryStaple",
            "P@ssw0rd!123",
            "",
            "a" * 500,
            "😀🔒emoji-pass",
        ]
        for raw in sensitive_samples:
            result = redact_password(raw)
            self.assertEqual(result, PASSWORD_PLACEHOLDER)
            # The raw text must not appear anywhere in the output.
            if raw:
                self.assertNotIn(raw, result)

    def test_result_does_not_reveal_length(self):
        short_result = redact_password("a")
        long_result = redact_password("a" * 100)
        self.assertEqual(short_result, long_result)
        self.assertNotIn(str(len("a" * 100)), long_result)


class TestDisplayUsername(unittest.TestCase):
    def test_returns_fixed_placeholder(self):
        self.assertEqual(display_username("real_user_123"), TEST_INPUT_PLACEHOLDER)

    def test_raw_username_not_echoed(self):
        raw = "someone@example.com"
        result = display_username(raw)
        self.assertNotIn(raw, result)


class TestFormatKeyLabel(unittest.TestCase):
    def test_printable_character_passthrough(self):
        self.assertEqual(format_key_label("a"), "a")
        self.assertEqual(format_key_label("Z"), "Z")

    def test_special_keys_are_relabeled(self):
        self.assertEqual(format_key_label("space"), "Space")
        self.assertEqual(format_key_label("BackSpace"), "Backspace")
        self.assertEqual(format_key_label("Return"), "Enter")
        self.assertEqual(format_key_label("Shift_L"), "Shift")

    def test_empty_or_none_input(self):
        self.assertEqual(format_key_label(""), "?")
        self.assertEqual(format_key_label(None), "?")

    def test_unknown_multi_char_symbol_passthrough(self):
        self.assertEqual(format_key_label("F5"), "F5")


if __name__ == "__main__":
    unittest.main()
