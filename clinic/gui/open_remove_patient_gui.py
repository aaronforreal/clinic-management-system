from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QInputDialog, QSizePolicy
)

class RemovePatientGUI(QWidget):
    """
    GUI for removing a patient by Personal Health Number (PHN).
    Allows users to search for a patient, view their details, and remove them from the system.
    """

    def __init__(self, controller, parent=None, patient=None):
        """
        Initializes the RemovePatientGUI.

        Parameters:
        - controller: The Controller instance for managing business logic.
        - parent: The parent widget, typically the main application window.
        - patient: The patient object to display and remove, if provided.
        """
        super().__init__(parent)

        # Store the controller, parent widget, and currently displayed patient
        self.controller = controller
        self.parent_widget = parent
        self.current_patient = patient

        # Main layout for the GUI
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)  
        main_layout.setSpacing(30) 
        self.setLayout(main_layout)

        # Title label
        title_label = QLabel("REMOVE PATIENT BY PHN")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        main_layout.addWidget(title_label)

        # Spacer below the title
        spacer_middle = QWidget()
        spacer_middle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(spacer_middle, stretch=1)

        # Patient information label
        self.patient_info_label = QLabel("")
        self.patient_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.patient_info_label.setStyleSheet("font-size: 18px; color: #555;")
        main_layout.addWidget(self.patient_info_label)

        # Remove button
        self.remove_button = QPushButton("Remove Patient")
        self.remove_button.setFixedSize(150, 40)
        self.remove_button.setEnabled(False) 
        self.remove_button.clicked.connect(self.confirm_and_remove_patient)

        # Display patient information if provided
        if self.current_patient:
            self.display_patient_info(self.current_patient)

        # Button layout for action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20) 

        # Add "Remove Patient" button
        button_layout.addWidget(self.remove_button)

        # Search again button
        search_again_button = QPushButton("Search Again")
        search_again_button.setFixedSize(150, 40)
        search_again_button.clicked.connect(self.search_again)
        button_layout.addWidget(search_again_button)

        # Back to menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(150, 40)
        back_to_menu_button.clicked.connect(self.back_to_menu_func)
        button_layout.addWidget(back_to_menu_button)

        # Center the buttons
        button_wrapper_layout = QVBoxLayout()
        button_wrapper_layout.addLayout(button_layout)
        button_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        main_layout.addLayout(button_wrapper_layout)

    def display_patient_info(self, patient):
        """
        Updates the patient information display with the selected patient's details.

        Parameters:
        - patient: The patient object to display.
        """
        self.patient_info_label.setText(
            f"PHN: {patient.phn}\n"
            f"Name: {self.wrap_text(patient.name)}\n"
            f"Birth Date: {self.wrap_text(patient.birth_date)}\n"
            f"Phone: {self.wrap_text(patient.phone)}\n"
            f"Email: {self.wrap_text(patient.email)}\n"
            f"Address: {self.wrap_text(patient.address)}"
        )
        self.patient_info_label.setWordWrap(True)
        self.remove_button.setEnabled(True)  # Enable the Remove button

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
            split_index = text.rfind(" ", 0, max_width)
            if split_index == -1:  # No space found, split at max_width
                split_index = max_width
            wrapped_lines.append(text[:split_index])
            text = text[split_index:].strip()
        wrapped_lines.append(text)  # Add remaining text
        return "\n".join(wrapped_lines)

    def search_again(self):
        """
        Prompts the user to enter a PHN and updates the patient information if a valid patient is found.
        """
        try:
            phn, ok = QInputDialog.getInt(self, "Search Patient", "Enter Patient's PHN to Remove:")
            if not ok:  # User canceled
                return

            patient = self.controller.search_patient(phn) 
            if patient:
                self.current_patient = patient  # Update the current patient
                self.display_patient_info(patient)
            else:
                QMessageBox.warning(self, "Not Found", "No patient found with the provided PHN.")
                # Reset display if no patient is found
                if self.current_patient:
                    self.display_patient_info(self.current_patient)
                else:
                    self.patient_info_label.setText("")
                    self.remove_button.setEnabled(False)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def confirm_and_remove_patient(self):
        """
        Prompts the user to confirm removal of the currently displayed patient and removes them if confirmed.
        """
        if not self.current_patient:
            QMessageBox.warning(self, "Operation Error", "No patient is currently selected.")
            return

        try:
            phn = self.current_patient.phn
            confirmation = QMessageBox.question(
                self,
                "Confirm Removal",
                f"Are you sure you want to remove {self.current_patient.name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                self.controller.delete_patient(phn)  # Remove the patient
                QMessageBox.information(self, "Success", f"Patient {self.current_patient.name} has been successfully removed.")
                self.back_to_menu_func()  # Navigate back to the main menu
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
