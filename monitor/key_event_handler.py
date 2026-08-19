"""
monitor/key_event_handler.py
------------------------------
SECURITY CONCEPT: Focus-scoped capture vs. global hooking.

Real keyloggers typically use OS-level hooks (e.g. Windows
`SetWindowsHookEx(WH_KEYBOARD_LL)`, X11 `XGrabKeyboard`, or libraries
like `pynput`/`keyboard` in "listen globally" mode) to receive *every*
keystroke on the machine, regardless of which application is focused.

This lab deliberately avoids all of that. It binds ONLY to Tkinter
widgets that belong to this application's own window
(`widget.bind("<KeyPress>", handler)`), which means:

  * The OS only ever delivers key events to this handler when one of
    THIS application's widgets currently has input focus.
  * Switching focus to another program (a browser, a text editor,
    a password manager, etc.) means this handler receives NOTHING --
    there is no cross-application visibility at all.
  * No OS-level hook, driver, accessibility API, or global listener is
    installed anywhere in this codebase.

This class is UI-framework-light on purpose: it takes a raw Tkinter
event object and turns it into a small, structured result, so the
capture logic itself can be unit-tested without spinning up a GUI.
"""

from dataclasses import dataclass
from monitor.redactor import format_key_label


@dataclass
class KeyEventResult:
    key_label: str
    is_printable: bool


class KeyEventHandler:
    """
    Processes individual Tkinter <KeyPress> events from widgets that
    belong to this application only.

    Usage:
        handler = KeyEventHandler()
        widget.bind("<KeyPress>", lambda e: on_key(handler.process(e)))
    """

    def __init__(self):
        self._active = False

    def start(self):
        """Enable processing (called on 'Start Monitoring')."""
        self._active = True

    def stop(self):
        """Disable processing (called on 'Stop Monitoring')."""
        self._active = False

    @property
    def is_active(self) -> bool:
        return self._active

    def process(self, tk_event) -> "KeyEventResult | None":
        """
        Converts a Tkinter key event into a KeyEventResult.

        Returns None if monitoring is currently stopped -- this is the
        single choke point that guarantees NOTHING is captured while
        the trainee has pressed "Stop Monitoring", even if a widget
        binding is technically still wired up.
        """
        if not self._active:
            return None

        key_symbol = getattr(tk_event, "keysym", "") or ""
        label = format_key_label(key_symbol)
        is_printable = len(key_symbol) == 1

        return KeyEventResult(key_label=label, is_printable=is_printable)

    def process_keysym(self, keysym: str) -> "KeyEventResult | None":
        """
        Convenience method used by unit tests so we don't need a real
        Tkinter event object to exercise the logic above.
        """
        if not self._active:
            return None
        label = format_key_label(keysym)
        return KeyEventResult(key_label=label, is_printable=len(keysym) == 1)
