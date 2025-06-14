from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox, QInputDialog, QVBoxLayout, QSizePolicy, QHBoxLayout
)
from clinic.exception import IllegalAccessException


class SearchPatientGUI(QWidget):
    """
    GUI for searching and displaying patient details by Personal Health Number (PHN).
    Provides options to search for another patient or return to the main menu.
    """

    def __init__(self, controller, parent=None, patient=None):
        """
        Initializes the SearchPatientGUI.

        Parameters:
        - controller: The Controller instance for handling backend logic.
        - parent: The parent widget, typically the main application window.
        - patient: The patient object to display initially, if available.
        """
        super().__init__(parent)

        self.controller = controller  # Store the controller instance
        self.parent_widget = parent  # Store the parent widget for navigation
        self.patient = patient  # Store the patient object to display

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)  
        main_layout.setSpacing(30)  
        self.setLayout(main_layout)

        # Spacer to lower the title slightly
        spacer_top = QWidget()
        spacer_top.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(spacer_top, stretch=1)

        # Title: Centered Horizontally
        title_label = QLabel("SEARCH PATIENT BY PHN")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        main_layout.addWidget(title_label)

        # Spacer Below Title
        spacer_middle = QWidget()
        spacer_middle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(spacer_middle, stretch=1)

        # Patient Info Section: Centered and Larger Font
        self.patient_info_label = QLabel("")
        self.patient_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.patient_info_label.setStyleSheet("font-size: 18px; color: #555;")
        main_layout.addWidget(self.patient_info_label)

        # Display patient information if provided
        if self.patient:
            self.display_patient_info(self.patient)

        # Button Layout: Buttons Beside Each Other
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)

        # Search Again Button
        search_again_button = QPushButton("Search Again")
        search_again_button.setFixedSize(150, 40)
        search_again_button.clicked.connect(self.search_again)  
        button_layout.addWidget(search_again_button)

        # Back to Menu Button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(150, 40)
        back_to_menu_button.clicked.connect(self.back_to_menu)  
        button_layout.addWidget(back_to_menu_button)

        # Center Button Layout Higher in the Layout
        button_wrapper_layout = QVBoxLayout()
        button_wrapper_layout.addLayout(button_layout)
        button_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        main_layout.addLayout(button_wrapper_layout)

        # Spacer Below Buttons to Lower Title
        spacer_bottom = QWidget()
        spacer_bottom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(spacer_bottom, stretch=2)

    def display_patient_info(self, patient):
        """
        Updates the patient information display.

        Parameters:
        - patient: The patient object whose information will be displayed.
        """
        self.patient_info_label.setText(
            f"PHN: {(patient.phn)}\n"
            f"Name: {self.wrap_text(patient.name)}\n"
            f"Birth Date: {self.wrap_text(patient.birth_date)}\n"
            f"Phone: {self.wrap_text(patient.phone)}\n"
            f"Email: {self.wrap_text(patient.email)}\n"
            f"Address: {self.wrap_text(patient.address)}"
        )
        self.patient_info_label.setWordWrap(True)  # Ensure the label wraps text correctly

    def wrap_text(self, text, max_width=50):
        """
        Wraps the input text to a specified width.

        Parameters:
        - text: The input string to wrap.
        - max_width: The maximum width (number of characters) per line.

        Returns:
        - str: The wrapped text.
        """
        if len(text) <= max_width:
            return text
        wrapped_lines = []
        while len(text) > max_width:
            split_index = text.rfind(" ", 0, max_width)  # Find the last space within the limit
            if split_index == -1:  # No space found, split at max width
                split_index = max_width
            wrapped_lines.append(text[:split_index])  # Add the wrapped line
            text = text[split_index:].strip()  
        wrapped_lines.append(text)  
        return "\n".join(wrapped_lines)

    def search_again(self):
        """
        Allows the user to search for another patient by PHN.
        """
        try:
            # Prompt the user to enter a PHN
            phn, ok = QInputDialog.getInt(self, "Search Patient", "Enter Personal Health Number (PHN):")
            if not ok:  # User canceled
                return

            # Validate the PHN and search for the patient
            patient = self.controller.search_patient(phn)
            if patient:
                self.display_patient_info(patient)
            else:
                QMessageBox.warning(self, "No Patient Found", "No patient found with the provided PHN.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to search for patients.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_menu(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
