# Medical Clinic System GUI

This project implements a medical clinic system in Python using a Model-View-Controller (MVC) architecture. It supports both a command-line interface (CLI) and a graphical user interface (GUI) built with PyQt6.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Usage](#usage)

   * [Command-Line Interface](#command-line-interface)
   * [Graphical User Interface](#graphical-user-interface)
7. [Testing](#testing)
8. [Development & Version Control](#development--version-control)
9. [Contributing](#contributing)
10. [Authors](#authors)

---

## Overview

This application manages patient records and clinical notes for a medical clinic. It follows the MVC pattern:

* **Model:** Core classes (`Patient`, `PatientRecord`, `Note`) and business logic.
* **View:** Two front-ends:

  * CLI via `clinic/cli`
  * GUI via `clinic/gui` (PyQt6)
* **Controller:** Orchestrates CRUD operations between view and model.

## Features

* User authentication (login/logout)
* CRUD operations for patients and notes
* JSON persistence for patient metadata
* Pickle persistence for clinical notes
* Interactive tables and editors via PyQt6 widgets

## Prerequisites

* Python 3.9 or later
* pip package manager
* PyQt6 framework

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:

   ```bash
   pip install PyQt6
   ```

## Project Structure

```plaintext
.
├── clinic
│   ├── cli
│   │   └── __main__.py        # CLI entry point
│   ├── dao                   # Data access objects
│   │   ├── patient_dao_json.py
│   │   ├── patient_encoder.py
│   │   ├── patient_decoder.py
│   │   └── note_dao_pickle.py
│   ├── gui                   # GUI components
│   │   ├── clinic_gui.py     # Main GUI window
│   │   └── ...               # Additional widgets
│   ├── controller.py         # Application logic
│   ├── patient.py            # Patient model
│   ├── patient_record.py     # PatientRecord model
│   └── note.py               # Note model
└── tests
    ├── patient_test.py
    ├── patient_record_test.py
    ├── note_test.py
    └── integration_test.py    # Persistence & integration tests
```

## Usage

### Command-Line Interface

Run the CLI prototype:

```bash
python3 -m clinic.cli
```

Follow prompts to log in, manage patients, and edit notes.

### Graphical User Interface

Launch the PyQt6 GUI:

```bash
python3 -m clinic.gui
```

Use menus and forms to:

* Log in / Log out
* Search, list, create, update, delete patients
* View and manage notes per patient

## Testing

* **Unit Tests:** Model logic and DAO operations

  ```bash
  python3 -m unittest -v tests/patient_test.py tests/patient_record_test.py tests/note_test.py
  ```
* **Integration Tests:** JSON & pickle persistence

  ```bash
  python3 -m unittest -v tests/integration_test.py
  ```

## Development & Version Control

* Create feature branches off `main`.
* Commit frequently with clear messages.
* Merge only after tests pass.

## Contributing

1. Fork the repo and create a new branch.
2. Implement changes and add tests.
3. Commit, push to your fork, and open a pull request.
