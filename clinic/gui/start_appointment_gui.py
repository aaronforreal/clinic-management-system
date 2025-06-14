from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout
)
from clinic.exception import IllegalAccessException

class StartAppointmentGUI(QWidget):
    """
    GUI for starting an appointment by searching for a patient using their Personal Health Number (PHN).
    Provides a search interface and navigation options.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the StartAppointmentGUI.

        Parameters:
        - controller: The Controller instance for managing backend logic.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        self.controller = controller  # Store the controller instance
        self.parent_widget = parent  # Store the parent widget for navigation

        # Main layout for the widget
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.layout.setSpacing(20)  
        self.setLayout(self.layout)

        # Set up the initial search view
        self.create_search_view()

    def create_search_view(self):
        """
        Displays the initial search interface for starting an appointment.
        """
        # Clear any existing widgets from the layout
        self.clear_layout()

        # Title Label
        title_label = QLabel("START APPOINTMENT WITH PATIENT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;") 
        self.layout.addWidget(title_label)

        # Spacing between the title and input field
        self.layout.addSpacing(10)

        # PHN Input Section
        phn_layout = QVBoxLayout()
        phn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.phn_label = QLabel("Personal Health Number (PHN):")
        self.phn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phn_label.setStyleSheet("margin-bottom: 10px;")
        phn_layout.addWidget(self.phn_label)

        self.phn_input = QLineEdit() 
        self.phn_input.setFixedWidth(250)  
        phn_layout.addWidget(self.phn_input)

        self.layout.addLayout(phn_layout)

        # Spacing between the input field and buttons
        self.layout.addSpacing(20)

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        # Search Button
        search_button = QPushButton("Search Patient")
        search_button.setFixedSize(150, 40)  
        search_button.clicked.connect(self.search_patient) 
        button_layout.addWidget(search_button)

        # Back to Menu Button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(150, 40)  
        back_to_menu_button.clicked.connect(self.back_to_menu_func)  
        button_layout.addWidget(back_to_menu_button)
        self.layout.addLayout(button_layout)

    def search_patient(self):
        """
        Searches for a patient by PHN and transitions to the appointment menu if successful.
        """
        try:
            # Get and validate the PHN input
            phn = int(self.phn_input.text().strip()) 
            patient = self.controller.search_patient(phn)  

            if patient:
                # Set the current patient in the Controller
                self.controller.set_current_patient(phn)

                # Navigate to the appointment menu
                self.open_appointment_menu()
            else:
                QMessageBox.warning(self, "Not Found", "No patient found with the provided PHN.")
                self.phn_input.clear()  # Clear the input field for invalid PHN

        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
            self.phn_input.clear()
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to search for patients.")
            self.phn_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
            self.phn_input.clear()

    def open_appointment_menu(self):
        """
        Opens the appointment main menu after successfully setting the current patient.
        """
        from clinic.gui.appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))

    def clear_layout(self):
        """
        Clears all widgets from the current layout.
        """
        while self.layout.count():
            # Remove and delete each widget in the layout
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
