from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox, QInputDialog, QVBoxLayout, QHBoxLayout
)

class RemoveNoteWindow(QWidget):
    """
    Window for removing a specific note from a patient's record.
    Allows the user to view, confirm, and delete a note.
    """

    def __init__(self, controller, note_code, parent=None):
        """
        Initializes the RemoveNoteWindow.

        Parameters:
        - controller: The Controller instance for handling business logic.
        - note_code: The code of the note to be displayed and potentially removed.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        self.controller = controller
        self.note_code = note_code  
        self.parent_widget = parent  

        # Attempt to fetch the note details
        try:
            self.note = self.controller.search_note(self.note_code) 
            if not self.note:
                raise Exception(f"Note #{self.note_code} does not exist.") 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load note details: {str(e)}")
            self.return_to_menu() 
            return

        # Setup the GUI layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)  
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        # Title
        title_label = QLabel("REMOVE NOTE FROM PATIENT RECORD:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Display note details
        self.note_details_label = QLabel(
            f"Note number: {self.note.code}\n"
            f"Note #{self.note.code}, from {self.note.timestamp}\n"
            f"{self.wrap_text(self.note.text)}"
        )
        self.note_details_label.setStyleSheet("font-size: 14px; color: gray;")
        self.note_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.note_details_label)

        # Add spacing between elements
        self.layout.addSpacing(5)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Remove Note button
        self.remove_note_button = QPushButton("Remove Note")
        self.remove_note_button.setFixedSize(150, 40)
        self.remove_note_button.clicked.connect(self.confirm_remove_note)
        button_layout.addWidget(self.remove_note_button)

        # Search Again button
        search_again_button = QPushButton("Search Again")
        search_again_button.setFixedSize(150, 40)
        search_again_button.clicked.connect(self.search_again)
        button_layout.addWidget(search_again_button)

        # Back to Menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(150, 40)
        back_to_menu_button.clicked.connect(self.return_to_menu)
        button_layout.addWidget(back_to_menu_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

    def wrap_text(self, text, max_width=50):
        """
        Wraps the input text to a specified width.

        Parameters:
        - text: The input string to wrap.
        - max_width: The maximum number of characters per line.

        Returns:
        - str: The wrapped text.
        """
        if len(text) <= max_width:
            return text
        wrapped_lines = []
        while len(text) > max_width:
            split_index = text.rfind(" ", 0, max_width)  # Find the last space within the limit
            if split_index == -1: 
                split_index = max_width
            wrapped_lines.append(text[:split_index]) 
            text = text[split_index:].strip() 
        wrapped_lines.append(text)  
        return "\n".join(wrapped_lines)

    def search_again(self):
        """
        Allows the user to search for a new note and updates the display.
        """
        try:
            # Prompt the user to enter a new note code
            note_code, ok = QInputDialog.getInt(self, "Search Note", "Enter Note Number:")
            if not ok:  # If the user cancels, do nothing
                return

            # Search for the note
            note = self.controller.search_note(note_code)
            if note:
                self.note = note  
                self.note_code = note_code
                self.note_details_label.setText(
                    f"Note number: {note.code}\n"
                    f"Note #{note.code}, from {note.timestamp}\n"
                    f"{self.wrap_text(note.text)}"
                )
                self.remove_note_button.setEnabled(True)  # Enable the remove button
            else:
                QMessageBox.warning(self, "Not Found", f"No note found with number #{note_code}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def confirm_remove_note(self):
        """
        Displays a confirmation dialog and removes the note if confirmed.
        """
        confirmation = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove note #{self.note_code}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                if self.controller.delete_note(self.note_code):  # Attempt to delete the note
                    QMessageBox.information(self, "Success", f"Note #{self.note_code} successfully removed.")
                    self.return_to_menu()
                else:
                    QMessageBox.warning(self, "Failure", f"Failed to remove note #{self.note_code}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def return_to_menu(self):
        """
        Navigates back to the appointment main menu.
        """
        from .appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
        else:
            QMessageBox.critical(self, "Error", "Parent widget not set. Cannot navigate back.")
            self.close()  # Close the current window as a fallback
