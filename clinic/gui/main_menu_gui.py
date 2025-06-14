from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QPushButton, QInputDialog, QMessageBox, QSizePolicy, QGridLayout
)
from clinic.gui.add_patient_gui import AddPatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.open_retrieve_patients_gui import RetrievePatientsGUI
from clinic.gui.open_change_patient_data_gui import ChangePatientDataGUI
from clinic.gui.open_remove_patient_gui import RemovePatientGUI
from clinic.gui.open_list_all_patients_gui import ListAllPatientsGUI
from clinic.gui.start_appointment_gui import StartAppointmentGUI

class MainMenuGUI(QWidget):
    """
    Main Menu GUI for the Medical Clinic System.
    Provides navigation to various functionalities such as adding, searching, retrieving, 
    and managing patient records.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the MainMenuGUI.

        Parameters:
        - controller: The Controller instance for managing business logic.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        # Store references for the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Call the main menu setup function
        self.main_menu()

    def main_menu(self):
        """
        Sets up the layout and components for the main menu.
        """
        # Create the main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Spacer to position the title at ~35% vertically
        spacer_top = QWidget()
        spacer_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer_top.setSizePolicy(spacer_policy)
        main_layout.addWidget(spacer_top, stretch=2)  # Add stretch to adjust spacing

        # Title label
        title_label = QLabel("Welcome to the Medical Clinic System Main Menu!")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the title
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000;")
        main_layout.addWidget(title_label, stretch=1)

        # Spacer between the title and buttons
        spacer_middle = QWidget()
        spacer_middle.setSizePolicy(spacer_policy)
        main_layout.addWidget(spacer_middle, stretch=1)

        # Create a grid layout for buttons
        button_layout = QGridLayout()
        button_layout.setContentsMargins(50, 10, 50, 10)  # Margins for better spacing
        button_layout.setHorizontalSpacing(30)  # Space between columns
        button_layout.setVerticalSpacing(10)  # Space between rows

        # Left column buttons
        add_patient_button = QPushButton("Add New Patient")
        add_patient_button.clicked.connect(self.open_add_patient_gui)
        button_layout.addWidget(add_patient_button, 0, 0)

        search_patient_button = QPushButton("Search Patient by PHN")
        search_patient_button.clicked.connect(self.open_search_patient_gui)
        button_layout.addWidget(search_patient_button, 1, 0)

        retrieve_patients_button = QPushButton("Retrieve Patients by Name")
        retrieve_patients_button.clicked.connect(self.open_retrieve_patients_gui)
        button_layout.addWidget(retrieve_patients_button, 2, 0)

        change_patient_data_button = QPushButton("Change Patient Data")
        change_patient_data_button.clicked.connect(self.open_change_patient_data_gui)
        button_layout.addWidget(change_patient_data_button, 3, 0)

        # Right column buttons
        remove_patient_button = QPushButton("Remove Patient")
        remove_patient_button.clicked.connect(self.open_remove_patient_gui)
        button_layout.addWidget(remove_patient_button, 0, 1)

        list_all_patients_button = QPushButton("List All Patients")
        list_all_patients_button.clicked.connect(self.open_list_all_patients_gui)
        button_layout.addWidget(list_all_patients_button, 1, 1)

        start_appointment_button = QPushButton("Start Appointment with Patient")
        start_appointment_button.clicked.connect(self.open_start_appointment_gui)
        button_layout.addWidget(start_appointment_button, 2, 1)

        log_out_button = QPushButton("Log Out")
        log_out_button.clicked.connect(self.logout)
        button_layout.addWidget(log_out_button, 3, 1)

        # Add the grid layout to the main layout
        main_layout.addLayout(button_layout, stretch=5)

        # Spacer to push everything slightly upward
        spacer_bottom = QWidget()
        spacer_bottom.setSizePolicy(spacer_policy)
        main_layout.addWidget(spacer_bottom, stretch=2)

    def open_add_patient_gui(self):
        """
        Opens the AddPatientGUI for adding a new patient.
        """
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AddPatientGUI(self.controller, self.parent_widget))

    def open_search_patient_gui(self):
        """
        Prompts the user to enter a PHN and navigates to SearchPatientGUI if the PHN is valid.
        """
        try:
            phn, ok = QInputDialog.getInt(self, "Search Patient", "Enter Personal Health Number (PHN):")
            if not ok: 
                return

            patient = self.controller.search_patient(phn)
            if patient:
                self.parent_widget.setCentralWidget(SearchPatientGUI(self.controller, self.parent_widget, patient))
            else:
                QMessageBox.warning(self, "No Patient Found", "No patient found with the provided PHN.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_retrieve_patients_gui(self):
        """
        Opens the RetrievePatientsGUI to retrieve patients by name.
        """
        if self.parent_widget:
            self.parent_widget.setCentralWidget(RetrievePatientsGUI(self.controller, self.parent_widget))

    def open_change_patient_data_gui(self):
        """
        Opens the ChangePatientDataGUI for modifying patient data.
        """
        if self.parent_widget:
            self.parent_widget.setCentralWidget(ChangePatientDataGUI(self.controller, self.parent_widget))

    def open_remove_patient_gui(self):
        """
        Prompts the user to enter a PHN and navigates to RemovePatientGUI if the PHN is valid.
        """
        try:
            phn, ok = QInputDialog.getInt(self, "Remove Patient", "Enter Personal Health Number (PHN):")
            if not ok:
                return

            patient = self.controller.search_patient(phn)
            if patient:
                self.parent_widget.setCentralWidget(RemovePatientGUI(self.controller, self.parent_widget, patient))
            else:
                QMessageBox.warning(self, "No Patient Found", "No patient found with the provided PHN.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_list_all_patients_gui(self):
        """
        Opens the ListAllPatientsGUI to display all patients.
        """
        if self.parent_widget:
            self.parent_widget.setCentralWidget(ListAllPatientsGUI(self.controller, self.parent_widget))

    def open_start_appointment_gui(self):
        """
        Opens the StartAppointmentGUI for initiating a patient appointment.
        """
        if self.parent_widget:
            self.parent_widget.setCentralWidget(StartAppointmentGUI(self.controller, self.parent_widget))

    def logout(self):
        """
        Logs out the user and navigates back to the login screen.
        """
        if self.parent():
            self.parent().login_screen()  
