from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout
)

class RetrieveNotesWindow(QWidget):
    """
    Window for displaying retrieved notes that contain specific text.
    Allows users to view matching notes and navigate back to the main menu.
    """

    def __init__(self, controller, parent, notes, search_text):
        """
        Initializes the RetrieveNotesWindow.

        Parameters:
        - controller: The Controller instance for managing backend logic.
        - parent: The parent widget, typically the main application window.
        - notes: A list of notes containing the search text.
        - search_text: The text string used for filtering the notes.
        """
        super().__init__(parent)

        self.controller = controller  # Store the controller for backend interactions
        self.parent_widget = parent  # Parent widget for navigation
        self.notes = notes  # List of notes matching the search
        self.search_text = search_text  # Search text used to filter notes

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title label
        title_label = QLabel(f"RETRIEVED NOTES:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")  
        self.layout.addWidget(title_label)

        # Display the notes in a QPlainTextEdit widget
        self.notes_display = QPlainTextEdit()
        self.notes_display.setReadOnly(True)  
        self.notes_display.setPlainText(self.format_notes())  
        self.layout.addWidget(self.notes_display)

        # Back to Menu button
        back_button_layout = QVBoxLayout()
        back_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        back_button = QPushButton("Back to Menu")
        back_button.setFixedSize(150, 40)  
        back_button.clicked.connect(self.return_to_menu) 

        # Add the back button to the layout
        back_button_layout.addWidget(back_button)
        self.layout.addLayout(back_button_layout)

    def format_notes(self):
        """
        Formats the notes for display in the QPlainTextEdit widget.

        Returns:
        - str: A formatted string containing all matching notes.
        """
        # Join notes into a readable format, separating each with a blank line
        return "\n\n".join(
            [
                f"Note number: {note.code}\nNote #{note.code}, from {note.timestamp}\n{note.text}"
                for note in self.notes
            ]
        )

    def return_to_menu(self):
        """
        Navigates back to the appointment main menu.
        """
        from clinic.gui.appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
