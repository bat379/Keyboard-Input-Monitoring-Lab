"""
gui/login_form.py
-------------------
SECURITY CONCEPT: Safe Test Mode.

This is a MOCK login form. It does not authenticate against any real
system, does not send data anywhere, and exists purely so a trainee can
see, end-to-end, what an "educational event" looks like when a
monitored form is submitted:

    Username field: [TEST INPUT]
    Password field: [REDACTED]

The password Entry widget uses `show="*"` (standard masking) AND, more
importantly, the raw value the trainee typed is passed through
`redact_password()` and discarded immediately on submit -- it is never
logged to the on-screen event log, never written to the database, and
never stored in any attribute of this class beyond the local variable
inside `_on_submit`.
"""

import customtkinter as ctk
from monitor.redactor import redact_password, display_username


class LoginFormFrame(ctk.CTkFrame):
    def __init__(self, master, on_submit_event, **kwargs):
        """
        on_submit_event: callback(username_display: str, password_redacted: str)
            Called after redaction has already happened -- this frame
            never hands raw credentials to its caller.
        """
        super().__init__(master, **kwargs)
        self.on_submit_event = on_submit_event

        ctk.CTkLabel(
            self, text="Safe Test Mode -- Mock Login Form",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(
            self,
            text=(
                "This form is NOT connected to any real account or service.\n"
                "Type any placeholder values -- nothing you enter here is a\n"
                "real credential, and the password is never stored or shown."
            ),
            justify="left",
            text_color=("gray20", "gray70"),
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkLabel(self, text="Username:").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="test_user")
        self.username_entry.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        ctk.CTkLabel(self, text="Password:").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        # show="*" masks the field visually -- but the REAL protection is
        # that we never read this value for anything other than
        # immediately redacting it in _on_submit below.
        self.password_entry = ctk.CTkEntry(self, placeholder_text="test_password", show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

        submit_btn = ctk.CTkButton(self, text="Submit (Simulated Login)", command=self._on_submit)
        submit_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(15, 10))

        self.grid_columnconfigure(1, weight=1)

    def _on_submit(self):
        raw_username = self.username_entry.get()
        raw_password = self.password_entry.get()

        # Redaction happens IMMEDIATELY, at the point of capture.
        # From this line onward, `raw_password` is never touched again.
        username_display = display_username(raw_username)
        password_display = redact_password(raw_password)

        # Clear the fields right away so the masked/raw values don't
        # linger in the widget any longer than necessary.
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

        self.on_submit_event(username_display, password_display)
