What the project does

The project is a safe educational simulator that demonstrates the basic mechanics behind keyboard-input monitoring.

The application contains three main areas:

Monitor
Starts and stops monitoring explicitly.
Captures keyboard events only inside the application's own test input area.
Does not monitor other applications or browser windows.
Safe Test Mode
Provides a simulated username/password form.
Demonstrates how sensitive input can be detected and safely redacted.
Passwords are represented as [REDACTED] rather than being stored.
Dashboard
Displays statistics about the synthetic test activity.
Shows keystroke counts, sessions, simulated login attempts, and redacted passwords.
Allows the local test database to be cleared.
Project architecture
keyboard_input_monitoring_lab/
│
├── main.py
├── requirements.txt
├── README.md
│
├── gui/
│   ├── app.py
│   ├── dashboard.py
│   └── login_form.py
│
├── monitor/
│   ├── key_event_handler.py
│   └── redactor.py
│
├── database/
│   └── db_manager.py
│
└── tests/
    ├── test_db_manager.py
    ├── test_key_handler.py
    └── test_redactor.py
How the components work together
                 ┌──────────────┐
                 │   main.py    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   GUI App    │
                 │ CustomTkinter│
                 └──────┬───────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │ Key Handler │       │ Mock Login  │
       └──────┬──────┘       └──────┬──────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                  ┌─────────────┐
                  │  Redactor   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   SQLite    │
                  │ Local Data  │
                  └─────────────┘
Installation for your GitHub README

Your existing README already has the PEP 668 solution. For Parrot/Debian-based Linux, the quick-start commands are:

git clone <YOUR-GITHUB-REPOSITORY-URL>
cd keyboard_input_monitoring_lab


sudo apt update
sudo apt install -y python3-venv python3-full python3-tk


python3 -m venv .venv
source .venv/bin/activate


pip install -r requirements.txt && python main.py



Run the tests with:

python -m unittest discover -s tests -v
Security concept demonstrated


The most useful educational aspect is the distinction between application-level input handling and system-wide keyboard monitoring.

Your project deliberately uses application/widget-level events. Therefore, typing into Firefox, a terminal, or another application is outside the project's monitoring scope. This makes it suitable for demonstrating the concept without creating a credential-stealing tool.

If you're putting this on GitHub as a college/cybersecurity project, I'd recommend presenting it as:

“A Safe Keyboard Input Monitoring Simulator for Cybersecurity Education”

rather than claiming it is a functional credential-capturing keylogger. This makes the project's purpose and security boundaries clear.
