"""
main.py
--------
Entry point for the Keyboard Input Monitoring Lab.

This is an EDUCATIONAL project for an isolated security-training
environment (e.g. an OWASP-style lab). It demonstrates, in a safe and
transparent way, how focus-scoped keyboard-input monitoring works.

It deliberately does NOT:
  - install any OS-level keyboard hook or accessibility API listener
  - run in the background, add itself to startup, or use any
    persistence/stealth mechanism
  - monitor any window other than its own
  - target, detect, or interact with web browsers in any way
  - inspect network traffic, cookies, sessions, or saved credentials
  - store real passwords or authentication data of any kind

Run with:  python main.py
(See README.md for virtual-environment setup instructions.)
"""

from gui.app import KeyboardMonitoringLabApp


def main():
    app = KeyboardMonitoringLabApp()
    app.mainloop()


if __name__ == "__main__":
    main()
