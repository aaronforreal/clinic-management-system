from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QTextEdit, QHBoxLayout
)
from clinic.exception import NoCurrentPatientException, IllegalOperationException


class ChangeNoteWindow(QWidget):
    """
    GUI window for changing a specific note in the patient's record.
    Provides functionality to display the current note and update it with new text.
    """

    def __init__(self, controller, note_code, parent=None):
        """
        Initializes the ChangeNoteWindow.

        Parameters:
        - controller: The Controller instance for managing business logic.
        - note_code: The unique code of the note to be changed.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        self.controller = controller  # Store the controller for later use
        self.note_code = note_code  # Store the note code to identify the note
        self.parent_widget = parent  # Store the parent widget for navigation

        # Attempt to retrieve the note details
        try:
            self.note = self.controller.search_note(self.note_code)
            if not self.note:
                raise IllegalOperationException(f"Note #{self.note_code} does not exist.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Error", str(ioe))
            self.return_to_appointment_menu()
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load note details: {str(e)}")
            self.return_to_appointment_menu()
            return

        # Set up the main layout for the window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title of the window
        title_label = QLabel("CHANGE NOTE FROM PATIENT RECORD:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Display current note details
        current_note_label = QLabel(f"Note number: {self.note.code}")
        current_note_label.setStyleSheet("font-size: 14px; color: gray;")
        self.layout.addWidget(current_note_label)

        note_details = QTextEdit()
        note_details.setPlainText(
            f"Note #{self.note.code}, from {self.note.timestamp}\n{self.note.text}"
        )
        note_details.setReadOnly(True)
        self.layout.addWidget(note_details)

        # Input field for the new note text
        new_note_label = QLabel("Enter New Note Text:")
        self.layout.addWidget(new_note_label)

        self.new_note_text = QLineEdit()
        self.layout.addWidget(self.new_note_text)

        # Buttons for updating and navigating back
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Update Note button
        update_button = QPushButton("Update Note")
        update_button.setFixedSize(150, 40)
        update_button.clicked.connect(self.update_note)
        button_layout.addWidget(update_button)

        # Back to Menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(150, 40) 
        back_to_menu_button.clicked.connect(self.return_to_appointment_menu) 
        button_layout.addWidget(back_to_menu_button)

        # Add button layout to the main layout
        self.layout.addLayout(button_layout)

    def update_note(self):
        """
        Handles updating the note with the new text after user confirmation.
        """
        try:
            new_text = self.new_note_text.text().strip()

            if not new_text:
                # Show a warning if the new text is empty
                QMessageBox.warning(self, "Input Error", "Note text cannot be empty.")
                return

            # Confirm the update with the user
            confirmation = QMessageBox.question(
                self,
                "Confirm Update",
                f"Are you sure you want to change note #{self.note_code}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if confirmation != QMessageBox.StandardButton.Yes:
                return

            # Update the note in the controller
            if self.controller.update_note(self.note_code, new_text):
                QMessageBox.information(self, "Success", f"Note #{self.note_code} successfully updated.")
                self.return_to_appointment_menu()  # Navigate back to the appointment menu
            else:
                QMessageBox.warning(self, "Failure", f"Failed to update note #{self.note_code}.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Operation Error", str(ioe))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def return_to_appointment_menu(self):
        """
        Navigates back to the appointment main menu GUI.

        If the parent widget is not set, displays an error and closes the window.
        """
        from clinic.gui.appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular dependencies
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
            self.deleteLater()
        else:
            QMessageBox.critical(self, "Error", "Parent widget not set. Cannot navigate back.")
            self.close()  # Close the window as a fallback
