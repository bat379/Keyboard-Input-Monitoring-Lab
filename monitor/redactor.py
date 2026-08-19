"""
monitor/redactor.py
--------------------
SECURITY CONCEPT: Redact-at-the-source.

A core lesson of this lab: sensitive data should never be allowed to
reach storage or logging code in the first place. Redaction happens
immediately, in the same layer that reads the raw input, *before*
anything is written to the GUI log, the database, or a return value
that could be persisted.

This module contains no I/O -- it is pure logic, which also makes it
trivially unit-testable (see tests/test_redactor.py).
"""

PASSWORD_PLACEHOLDER = "[REDACTED]"
TEST_INPUT_PLACEHOLDER = "[TEST INPUT]"


def redact_password(_raw_password: str) -> str:
    """
    Takes a raw password string typed into the mock login form and
    returns a fixed placeholder -- the actual characters and even the
    *length* of the password are discarded, not just hidden from the UI.

    Deliberately, the parameter is never referenced beyond this line,
    and the function never returns, logs, or stores any derivative of it
    (not a hash, not a length, not a character count) — a proper
    real-world implementation should avoid leaking even metadata about
    a secret.
    """
    return PASSWORD_PLACEHOLDER


def display_username(_raw_username: str) -> str:
    """
    Even though a "username" is lower sensitivity than a password, this
    lab treats ALL mock login-form input as synthetic test data and
    never displays or stores the literal value the trainee typed --
    reinforcing the "collect the minimum necessary data" principle.
    """
    return TEST_INPUT_PLACEHOLDER


def format_key_label(key_symbol: str) -> str:
    """
    Normalizes a raw Tkinter key symbol into a short, readable label for
    the on-screen keystroke log, e.g.:

        "space"     -> "Space"
        "BackSpace" -> "Backspace"
        "a"         -> "a"

    This keeps the Monitor tab's log a legible teaching aid rather than
    a raw event dump.
    """
    if key_symbol is None or key_symbol == "":
        return "?"

    special_labels = {
        "space": "Space",
        "BackSpace": "Backspace",
        "Return": "Enter",
        "Tab": "Tab",
        "Shift_L": "Shift",
        "Shift_R": "Shift",
        "Control_L": "Ctrl",
        "Control_R": "Ctrl",
        "Alt_L": "Alt",
        "Alt_R": "Alt",
        "Caps_Lock": "CapsLock",
        "Escape": "Esc",
        "Delete": "Delete",
    }
    if key_symbol in special_labels:
        return special_labels[key_symbol]

    # Single printable character keys are shown as-is (this is TEST data
    # the trainee typed into the lab's own practice box -- never a
    # real password, since the password field never reaches this path).
    if len(key_symbol) == 1:
        return key_symbol

    return key_symbol
