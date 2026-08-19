"""
gui/dashboard.py
------------------
SECURITY CONCEPT: Transparency.

A defining trait of legitimate monitoring/auditing tools (vs. spyware)
is that the subject of monitoring can SEE what has been collected, in
plain terms, at any time. This dashboard is the lab's transparency
surface: it shows aggregate counts pulled straight from the local
SQLite database -- nothing here is hidden or obfuscated.
"""

import customtkinter as ctk


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, db_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.db_manager = db_manager

        ctk.CTkLabel(
            self, text="Educational Dashboard", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=10, sticky="w")

        self.stat_labels = {}
        stats_config = [
            ("keystrokes", "Test keystrokes captured"),
            ("sessions", "Test sessions"),
            ("login_attempts", "Simulated login attempts"),
            ("passwords_redacted", "Passwords redacted"),
        ]

        for i, (key, caption) in enumerate(stats_config, start=1):
            card = ctk.CTkFrame(self, corner_radius=10)
            card.grid(row=i, column=0, columnspan=2, padx=10, pady=6, sticky="ew")
            card.grid_columnconfigure(1, weight=1)

            value_label = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=26, weight="bold"))
            value_label.grid(row=0, column=0, padx=15, pady=10)

            ctk.CTkLabel(card, text=caption, font=ctk.CTkFont(size=14)).grid(
                row=0, column=1, padx=5, pady=10, sticky="w"
            )
            self.stat_labels[key] = value_label

        self.grid_columnconfigure(0, weight=1)

        refresh_btn = ctk.CTkButton(self, text="Refresh Stats", command=self.refresh)
        refresh_btn.grid(row=len(stats_config) + 1, column=0, columnspan=2, padx=10, pady=(15, 10))

        self.refresh()

    def refresh(self):
        """Re-reads counts from the database and updates the labels."""
        stats = self.db_manager.get_stats()
        for key, label_widget in self.stat_labels.items():
            label_widget.configure(text=str(stats.get(key, 0)))
