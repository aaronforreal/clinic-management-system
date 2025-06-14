from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableView, QHeaderView, QStyledItemDelegate, QHBoxLayout
)
from PyQt6.QtGui import QTextOption
from clinic.exception import IllegalAccessException


class WordWrapDelegate(QStyledItemDelegate):
    """
    Custom delegate to enable word wrapping in QTableView cells.
    Ensures text wraps within cells rather than being truncated.
    """

    def initStyleOption(self, option, index):
        """
        Configures the style options for the delegate.

        Parameters:
        - option: The QStyleOptionViewItem instance to configure.
        - index: The QModelIndex for the item being styled.
        """
        super().initStyleOption(option, index)
        option.textElideMode = Qt.TextElideMode.ElideNone 
        option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        option.wrapMode = QTextOption.WrapMode.WrapAnywhere  # Enable word wrapping


class PatientTableModel(QAbstractTableModel):
    """
    Custom TableModel for displaying patient data in QTableView.
    Manages patient data and provides it in a tabular format for the view.
    """

    def __init__(self, patients=None):
        """
        Initializes the PatientTableModel.

        Parameters:
        - patients: A list of patient objects to display, defaults to an empty list.
        """
        super().__init__()
        self.patients = patients or [] 
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]  

    def rowCount(self, parent=None):
        """
        Returns the number of rows (patients).

        Parameters:
        - parent: Required for overriding but not used.

        Returns:
        - int: The number of patients.
        """
        return len(self.patients)

    def columnCount(self, parent=None):
        """
        Returns the number of columns.

        Parameters:
        - parent: Required for overriding but not used.

        Returns:
        - int: The number of headers (columns).
        """
        return len(self.headers)

    def data(self, index, role):
        """
        Returns the data for a given index and role.

        Parameters:
        - index: The QModelIndex specifying the cell.
        - role: The data role (e.g., display).

        Returns:
        - str: The content for the cell based on the index and role.
        """
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        patient = self.patients[index.row()]  # Get the patient for the row
        column = index.column()
        if column == 0:
            return self.insert_breaking_characters(str(patient.phn))  # PHN
        elif column == 1:
            return self.insert_breaking_characters(patient.name)  # Name
        elif column == 2:
            return self.insert_breaking_characters(patient.birth_date)  # Birth Date
        elif column == 3:
            return self.insert_breaking_characters(patient.phone)  # Phone
        elif column == 4:
            return self.insert_breaking_characters(patient.email)  # Email
        elif column == 5:
            return self.insert_breaking_characters(patient.address)  # Address
        return None

    def headerData(self, section, orientation, role):
        """
        Returns the header data for a given section and orientation.

        Parameters:
        - section: The section index (column index for horizontal headers).
        - orientation: Orientation of the header (horizontal or vertical).
        - role: The data role.

        Returns:
        - str: The header text for horizontal headers.
        """
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    @staticmethod
    def insert_breaking_characters(text):
        """
        Inserts zero-width spaces into all strings to allow breaking.

        Parameters:
        - text: The string to insert breaking characters into.

        Returns:
        - str: The text with zero-width spaces added.
        """
        return "\u200B".join(text) if isinstance(text, str) else text


class RetrievePatientsGUI(QWidget):
    """
    GUI for retrieving patients by name.
    Displays a search input and a table for showing retrieved patient data.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the RetrievePatientsGUI.

        Parameters:
        - controller: The Controller instance for handling business logic.
        - parent: The parent widget, typically the main application window.
        """
        super().__init__(parent)

        # Store references to the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title label
        title_label = QLabel("RETRIEVE PATIENTS BY NAME")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # Name input
        self.name_label = QLabel("Enter Patient's Name (or part of the name):")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Buttons for search and back to menu
        search_button = QPushButton("Retrieve Patients")
        search_button.setFixedSize(140, 30) 
        search_button.clicked.connect(self.retrieve_patients)

        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.setFixedSize(140, 30)  
        back_to_menu_button.clicked.connect(self.back_to_menu_func)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(back_to_menu_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.addLayout(button_layout)

        # Patient table view
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel() 
        self.patient_table.setModel(self.patient_model)
        self.patient_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.patient_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.patient_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Enable word wrapping
        word_wrap_delegate = WordWrapDelegate()
        self.patient_table.setItemDelegate(word_wrap_delegate)

        # Adjust rows and columns for content
        self.patient_table.resizeRowsToContents()
        header = self.patient_table.horizontalHeader()
        header.sectionResized.connect(self.patient_table.resizeRowsToContents)  # Adjust rows when columns resize
        header.setStretchLastSection(True)  # Stretch the last column
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # PHN
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Birth Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Phone
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Email
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Address

        layout.addWidget(self.patient_table)

    def retrieve_patients(self):
        """
        Handles retrieving patients by name and updates the table view.
        """
        try:
            # Get the search string
            search_string = self.name_input.text().strip()

            if not search_string:
                QMessageBox.warning(self, "Input Error", "Please enter a name to search.")
                return

            # Fetch patients matching the search string
            patients = self.controller.retrieve_patients(search_string)

            if patients:
                self.patient_model = PatientTableModel(patients) 
                self.patient_table.setModel(self.patient_model)
                self.patient_table.resizeRowsToContents() 
            else:
                QMessageBox.information(self, "No Results", "No patients found matching the search criteria.")
                self.patient_model = PatientTableModel() 
                self.patient_table.setModel(self.patient_model)

        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to retrieve patients.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
