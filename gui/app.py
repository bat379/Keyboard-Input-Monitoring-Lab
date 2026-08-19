"""
gui/app.py
-----------
Top-level application window for the Keyboard Input Monitoring Lab.

SECURITY CONCEPT: Explicit, visible control state.

Real spyware runs silently and gives its operator (not its victim)
control. This lab inverts that: the trainee sitting at the keyboard is
the one with the Start/Stop buttons, the status indicator, and full
visibility into everything captured -- and monitoring is OFF by default
every time the app launches.
"""

import customtkinter as ctk

from database.db_manager import DatabaseManager
from monitor.key_event_handler import KeyEventHandler
from gui.login_form import LoginFormFrame
from gui.dashboard import DashboardFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class KeyboardMonitoringLabApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Keyboard Input Monitoring Lab (Educational)")
        self.geometry("880x640")
        self.minsize(760, 560)

        self.db = DatabaseManager()
        self.key_handler = KeyEventHandler()
        self.current_session_id = None

        self._build_layout()

        # SECURITY NOTE: monitoring is OFF at startup. Nothing is
        # captured until the trainee explicitly clicks "Start Monitoring".
        self._set_monitoring_ui_state(active=False)

    # ------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------
    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top control bar -------------------------------------------------
        control_bar = ctk.CTkFrame(self, corner_radius=0)
        control_bar.grid(row=0, column=0, sticky="ew")
        control_bar.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            control_bar, text="Keyboard Input Monitoring Lab",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.start_btn = ctk.CTkButton(
            control_bar, text="Start Monitoring", fg_color="#2fa572",
            hover_color="#248a5f", command=self._start_monitoring, width=150,
        )
        self.start_btn.grid(row=0, column=3, padx=(5, 5), pady=12)

        self.stop_btn = ctk.CTkButton(
            control_bar, text="Stop Monitoring", fg_color="#c0392b",
            hover_color="#a13024", command=self._stop_monitoring, width=150,
        )
        self.stop_btn.grid(row=0, column=4, padx=(5, 15), pady=12)

        self.status_label = ctk.CTkLabel(control_bar, text="STOPPED", text_color="gray")
        self.status_label.grid(row=0, column=1, padx=(0, 15))

        # --- Tabs --------------------------------------------------------------
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        self.tab_monitor = self.tabview.add("Monitor")
        self.tab_safe_mode = self.tabview.add("Safe Test Mode")
        self.tab_dashboard = self.tabview.add("Dashboard")

        self._build_monitor_tab()
        self._build_safe_mode_tab()
        self._build_dashboard_tab()

        # --- Bottom bar: Clear Test Data ---------------------------------------
        bottom_bar = ctk.CTkFrame(self, corner_radius=0)
        bottom_bar.grid(row=2, column=0, sticky="ew")
        clear_btn = ctk.CTkButton(
            bottom_bar, text="Clear Test Data", fg_color="#7f8c8d",
            hover_color="#66787a", command=self._clear_test_data,
        )
        clear_btn.pack(side="right", padx=15, pady=10)

        ctk.CTkLabel(
            bottom_bar,
            text="All data is synthetic, local-only (SQLite), and scoped to this app's own window.",
            text_color=("gray30", "gray60"),
        ).pack(side="left", padx=15, pady=10)

    def _build_monitor_tab(self):
        self.tab_monitor.grid_columnconfigure(0, weight=1)
        self.tab_monitor.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.tab_monitor,
            text=(
                "Type into the box below while monitoring is running.\n"
                "SECURITY NOTE: keystrokes are ONLY captured while this box has\n"
                "input focus and 'Start Monitoring' is active -- switching to another\n"
                "application (or another window) sends this app NO events at all."
            ),
            justify="left",
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # This is the ONLY widget in the Monitor tab bound to key events.
        # Binding is done on this specific widget (not bind_all, not any
        # OS-level hook), so events only arrive when THIS box has focus.
        self.test_input_box = ctk.CTkTextbox(self.tab_monitor, height=80)
        self.test_input_box.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.test_input_box.bind("<KeyPress>", self._on_key_press)

        ctk.CTkLabel(self.tab_monitor, text="Captured Test Keystroke Log:").grid(
            row=2, column=0, padx=10, pady=(10, 0), sticky="nw"
        )
        self.event_log = ctk.CTkTextbox(self.tab_monitor, state="disabled")
        self.event_log.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.tab_monitor.grid_rowconfigure(3, weight=1)

    def _build_safe_mode_tab(self):
        self.tab_safe_mode.grid_columnconfigure(0, weight=1)
        self.login_form = LoginFormFrame(
            self.tab_safe_mode, on_submit_event=self._on_login_submit
        )
        self.login_form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.tab_safe_mode, text="Simulated Login Events:").grid(
            row=1, column=0, padx=10, pady=(15, 0), sticky="w"
        )
        self.login_event_log = ctk.CTkTextbox(self.tab_safe_mode, state="disabled")
        self.login_event_log.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.tab_safe_mode.grid_rowconfigure(2, weight=1)

    def _build_dashboard_tab(self):
        self.tab_dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard = DashboardFrame(self.tab_dashboard, self.db)
        self.dashboard.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # ------------------------------------------------------------
    # Monitoring control
    # ------------------------------------------------------------
    def _start_monitoring(self):
        if self.key_handler.is_active:
            return
        self.current_session_id = self.db.start_session()
        self.key_handler.start()
        self._set_monitoring_ui_state(active=True)
        self._append_log(self.event_log, "-- Monitoring session started --")

    def _stop_monitoring(self):
        if not self.key_handler.is_active:
            return
        self.key_handler.stop()
        if self.current_session_id is not None:
            self.db.end_session(self.current_session_id)
        self._append_log(self.event_log, "-- Monitoring session stopped --")
        self.current_session_id = None
        self._set_monitoring_ui_state(active=False)
        self.dashboard.refresh()

    def _set_monitoring_ui_state(self, active: bool):
        if active:
            self.status_label.configure(text="RUNNING", text_color="#2fa572")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
        else:
            self.status_label.configure(text="STOPPED", text_color="gray")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    # ------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------
    def _on_key_press(self, tk_event):
        """
        Bound only to self.test_input_box (see _build_monitor_tab).
        Tkinter guarantees this callback fires only when that specific
        widget has input focus within THIS application's window --
        there is no path here that observes keys typed elsewhere.
        """
        result = self.key_handler.process(tk_event)
        if result is None:
            return  # Monitoring is stopped; nothing is recorded.

        if self.current_session_id is not None:
            self.db.log_keystroke(self.current_session_id, result.key_label)
        self._append_log(self.event_log, f"Key: {result.key_label}")

    def _on_login_submit(self, username_display: str, password_display: str):
        """
        Called by LoginFormFrame AFTER redaction already happened.
        This method never sees a raw password.
        """
        session_id = self.current_session_id or self.db.start_session()
        if self.current_session_id is None:
            self.db.end_session(session_id)  # standalone submit outside a session

        self.db.log_login_attempt(
            session_id, username_display, password_redacted=(password_display == "[REDACTED]")
        )
        self._append_log(self.login_event_log, f"Username field: {username_display}")
        self._append_log(self.login_event_log, f"Password field: {password_display}")
        self.dashboard.refresh()

    # ------------------------------------------------------------
    # Data management
    # ------------------------------------------------------------
    def _clear_test_data(self):
        self.db.clear_all_data()
        self._set_textbox(self.event_log, "")
        self._set_textbox(self.login_event_log, "")
        self.dashboard.refresh()
        self._append_log(self.event_log, "-- Test data cleared --")

    # ------------------------------------------------------------
    # Small helpers
    # ------------------------------------------------------------
    @staticmethod
    def _append_log(textbox, line: str):
        textbox.configure(state="normal")
        textbox.insert("end", line + "\n")
        textbox.see("end")
        textbox.configure(state="disabled")

    @staticmethod
    def _set_textbox(textbox, text: str):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
