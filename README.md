Keyboard Input Monitoring Lab

A beginner-friendly Python cybersecurity project demonstrating keyboard-input monitoring, event handling, password redaction, SQLite storage, and GUI security concepts in a controlled educational environment.

📌 Project Overview

This project is designed for learning how keyboard-input monitoring works from a programming and cybersecurity perspective.

It provides a controlled test environment where keyboard events can be generated and analyzed inside the application's own interface. Sensitive test data is redacted before being stored.

The project focuses on understanding:

Keyboard event handling
GUI application development
Input validation
Password redaction
SQLite database storage
Security logging
Unit testing
Basic cybersecurity concepts
🎯 Objectives

The main objectives of this project are:

Understand how keyboard events are processed by a GUI application.
Learn how sensitive input should be handled securely.
Demonstrate password redaction before logging.
Store safe test events in a local SQLite database.
Build a graphical cybersecurity learning environment.
Apply software testing to security-related functionality.



    🎯 How It Works

The application performs keyboard-input monitoring inside its controlled testing environment.

The workflow includes:

Starting the graphical application.
Creating a controlled test session.
Generating keyboard events inside the application.
Processing the generated input through the event handler.
Detecting sensitive test fields.
Redacting password values before storage.
Saving safe test events in SQLite.
Displaying activity statistics through the dashboard.


📁 Module Description
main.py

The main entry point of the application.

Responsibilities:

Initialize the application.
Initialize the database.
Launch the graphical interface.
Handle application-level errors.
gui/

Contains the graphical user interface.

app.py

Controls the main application window and connects the different components.

dashboard.py

Provides the security-monitoring dashboard and displays test statistics.

login_form.py

Provides the controlled mock login environment used for demonstrating input handling.

monitor/

Contains the keyboard-monitoring logic.

key_event_handler.py

Processes keyboard events generated within the controlled application environment.

redactor.py

Handles sensitive test information and ensures password values are represented as:
[REDACTED]
database/

Contains the SQLite database functionality.

db_manager.py is responsible for:

Creating database tables.
Storing safe test events.
Retrieving test statistics.
Managing test sessions.
Clearing test data.
tests/

Contains automated unit tests for:

Database operations
Keyboard-event handling
Password redaction
🛠️ Technologies Used
Technology	Purpose
Python	Application development
CustomTkinter	Graphical user interface
SQLite	Local test-data storage
unittest	Automated testing
Git/GitHub	Version control
⚙️ Installation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py

The tests cover:

Keyboard event processing
Input redaction
Database operations
🔒 Security & Privacy

This project is intentionally designed as a controlled educational simulator.

It does not:

Capture keystrokes from other applications.
Monitor browser activity.
Capture real website credentials.
Intercept HTTPS traffic.
Collect browser cookies or sessions.
Extract saved passwords.
Install persistence mechanisms.
Hide itself from the user.
Transmit captured information to another system.

Passwords entered into the controlled test environment are redacted before being stored.

🎓 Educational Purpose

This project demonstrates an important cybersecurity principle:

Security tools should be designed with clear boundaries around what data they can access and how sensitive information is handled.

The project can be used to study:

Secure input handling
Logging
Data sanitization
Password protection
GUI event systems
Database security
Security testing
🚀 Future Improvements

Possible future improvements include:

Add more input-validation tests.
Add security-event filtering.
Improve dashboard visualizations.
Add configurable redaction rules.
Add additional mock security scenarios.
Add export of sanitized security reports.
Add more automated security tests.
⚖️ Disclaimer

This project is intended only for authorized cybersecurity education, software development practice, and controlled laboratory environments.

It must not be modified or used to secretly collect credentials, monitor other users, or access information from systems without authorization.
