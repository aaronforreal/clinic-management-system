from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from clinic.exception import IllegalAccessException, IllegalOperationException


class ChangePatientDataGUI(QWidget):
    """
    GUI for changing a patient's data.
    Allows searching for a patient by PHN, editing their details, and saving the updated data.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the ChangePatientDataGUI.

        Parameters:
        - controller: The Controller instance for handling business logic.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        # Store references to the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Set up the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title label
        title_label = QLabel("CHANGE PATIENT DATA")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # PHN input for searching the patient
        self.phn_label = QLabel("Enter Patient's Current PHN:")
        layout.addWidget(self.phn_label)
        self.phn_input = QLineEdit()
        layout.addWidget(self.phn_input)

        # Search button
        self.search_button = QPushButton("Search Patient")
        self.search_button.setFixedWidth(150)
        self.search_button.clicked.connect(self.search_patient)
        layout.addWidget(self.search_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Editable fields for patient data
        self.new_phn_label = QLabel("New PHN (Optional):")
        self.new_phn_input = QLineEdit()
        layout.addWidget(self.new_phn_label)
        layout.addWidget(self.new_phn_input)

        self.name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.birth_date_label = QLabel("Birth Date (YYYY-MM-DD):")
        self.birth_date_input = QLineEdit()
        layout.addWidget(self.birth_date_label)
        layout.addWidget(self.birth_date_input)

        self.phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)

        # Horizontal layout for action buttons
        button_layout = QHBoxLayout()

        # Update button
        self.update_button = QPushButton("Update Patient Data")
        self.update_button.setFixedWidth(200)
        self.update_button.clicked.connect(self.confirm_and_update_patient_data)
        button_layout.addWidget(self.update_button)

        # Back to menu button
        self.back_to_menu_button = QPushButton("Back to Menu")
        self.back_to_menu_button.setFixedWidth(150)
        self.back_to_menu_button.clicked.connect(self.back_to_menu_func)
        button_layout.addWidget(self.back_to_menu_button)
        layout.addLayout(button_layout)

    def search_patient(self):
        """
        Searches for a patient by PHN and populates the editable fields with their data.
        """
        try:
            phn = int(self.phn_input.text().strip()) 
            patient = self.controller.search_patient(phn) 

            if patient:
                # Populate the fields with the patient's current data
                self.new_phn_input.setText(str(patient.phn))
                self.name_input.setText(patient.name)
                self.birth_date_input.setText(patient.birth_date)
                self.phone_input.setText(patient.phone)
                self.email_input.setText(patient.email)
                self.address_input.setText(patient.address)
            else:
                QMessageBox.warning(self, "Not Found", "No patient found with the provided PHN.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to search for a patient.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def confirm_and_update_patient_data(self):
        """
        Prompts the user for confirmation and updates the patient data if confirmed.
        """
        try:
            # Retrieve the updated data from the fields
            old_phn = int(self.phn_input.text().strip())
            new_phn = self.new_phn_input.text().strip()
            name = self.name_input.text().strip()
            birth_date = self.birth_date_input.text().strip()
            phone = self.phone_input.text().strip()
            email = self.email_input.text().strip()
            address = self.address_input.text().strip()

            # Ensure all fields are filled out
            if not all([name, birth_date, phone, email, address]):
                QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
                return

            # Prompt confirmation from the user
            confirmation = QMessageBox.question(
                self,
                "Confirm Update",
                "Are you sure you want to update the patient data?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                # Convert the new PHN to an integer if provided
                new_phn = int(new_phn) if new_phn else None

                # Update the patient data in the controller
                self.controller.update_patient(old_phn, new_phn, name, birth_date, phone, email, address)
                QMessageBox.information(self, "Success", "Patient data updated successfully.")
                self.back_to_menu_func()
            else:
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to update patient data.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Operation Error", str(ioe))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
