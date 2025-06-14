import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy
)
from clinic.gui.quit_gui import QuitGUI 
from clinic.gui.main_menu_gui import MainMenuGUI  
from clinic.controller import Controller 
from clinic.exception import InvalidLoginException  


class ClinicGUI(QMainWindow):
    """
    The main GUI window for the Medical Clinic System.
    Handles the login screen and transitions to other screens like MainMenuGUI and QuitGUI.
    """

    def __init__(self):
        """
        Initializes the ClinicGUI instance and sets up the login screen.
        """
        super().__init__()

        # Set the window title and fixed size
        self.setWindowTitle("MEDICAL CLINIC SYSTEM")
        self.setFixedSize(1024, 768)
        self.center_window()

        # Initialize the controller with autosave enabled
        self.controller = Controller(autosave=True)

        # Display the login screen
        self.login_screen()

    def login_screen(self):
        """
        Sets up and displays the login screen.
        Resets the logged_in status in the controller to prevent unauthorized access.
        """
        # Ensure the logged_in flag is reset
        self.controller.logged_in = False

        # Create the central widget and set it as the main content
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a grid layout for the central widget
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # Add top spacer to push the title downward
        spacer_top = QWidget()
        spacer_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer_top.setSizePolicy(spacer_policy)
        main_layout.addWidget(spacer_top, 0, 0, 1, 3)

        # Add the system title
        medicalSystemTitle = QLabel("MEDICAL CLINIC SYSTEM")
        medicalSystemTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        medicalSystemTitle.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000;")
        main_layout.addWidget(medicalSystemTitle, 1, 0, 1, 3)

        # Create a grid layout for inputs and buttons
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)  
        layout.setVerticalSpacing(10)  
        layout.setHorizontalSpacing(5)  

        # Username input
        username_label = QLabel("Username:")
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(username_label, 0, 0)

        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(200)
        layout.addWidget(self.username_input, 0, 1)

        # Password input
        password_label = QLabel("Password:")
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(password_label, 1, 0)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  
        self.password_input.setFixedWidth(200)
        layout.addWidget(self.password_input, 1, 1)

        # Quit button
        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(90, 35) 
        quit_button.clicked.connect(self.quit)
        layout.addWidget(quit_button, 2, 0, 1, 2, Qt.AlignmentFlag.AlignRight)

        # Login button
        login_button = QPushButton("Log In")
        login_button.setFixedSize(90, 35)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button, 2, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)

        # Add the grid layout to the main layout
        main_layout.addLayout(layout, 2, 0, 1, 3)

        # Add bottom spacer to push content upward slightly
        spacer_bottom = QWidget()
        spacer_bottom.setSizePolicy(spacer_policy)
        main_layout.addWidget(spacer_bottom, 3, 0, 1, 3)

    def center_window(self):
        """
        Centers the window on the primary screen.
        """
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def login(self):
        """
        Handles the login button click event.
        Verifies the username and password using the Controller and navigates to MainMenuGUI upon success.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text() 

        try:
            # Attempt login via the controller
            if self.controller.login(username, password):
                QMessageBox.information(self, "Login Successful", "Welcome!")
                self.controller.logged_in = True  # Mark user as logged in
                self.open_main_menu()  # Navigate to the main menu
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
        except InvalidLoginException:
            QMessageBox.critical(self, "Login Error", "Invalid username or password. Please try again.")
            self.username_input.clear()
            self.password_input.clear()

    def open_main_menu(self):
        """
        Opens the MainMenuGUI after successful login.
        """
        self.setCentralWidget(MainMenuGUI(self.controller, self))

    def quit(self):
        """
        Opens the QuitGUI to terminate the session.
        """
        self.setCentralWidget(QuitGUI(self))


def main():
    """
    Main entry point for the application.
    Sets up the QApplication, applies the stylesheet, and launches the ClinicGUI.
    """
    app = QApplication(sys.argv)

    # Apply the stylesheet
    with open("clinic/gui/style.qss", "r") as file:
        app.setStyleSheet(file.read())

    window = ClinicGUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
