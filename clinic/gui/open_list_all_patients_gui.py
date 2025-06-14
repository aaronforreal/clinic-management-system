from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableView, QMessageBox, QHeaderView, QStyledItemDelegate
)
from PyQt6.QtGui import QTextOption


class WordWrapDelegate(QStyledItemDelegate):
    """
    Custom delegate to enable word wrapping in QTableView cells.
    Ensures that long text wraps properly within cells.
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
    Custom TableModel for displaying patient data in a QTableView.
    Manages the patient data and provides it to the view in a tabular format.
    """

    def __init__(self, patients, parent=None):
        """
        Initializes the PatientTableModel.

        Parameters:
        - patients: A list of patient objects to display.
        - parent: The parent object, typically None.
        """
        super().__init__(parent)
        self.patients = patients 
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]

    def rowCount(self, parent=None):
        """
        Returns the number of rows (patients).

        Parameters:
        - parent: Required for overriding but not used.

        Returns:
        - int: Number of patients.
        """
        return len(self.patients)

    def columnCount(self, parent=None):
        """
        Returns the number of columns.

        Parameters:
        - parent: Required for overriding but not used.

        Returns:
        - int: Number of columns (based on headers).
        """
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        Returns the data for a given index and role.

        Parameters:
        - index: The QModelIndex specifying the cell.
        - role: The data role (e.g., display).

        Returns:
        - The cell's content based on the role.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            patient = self.patients[index.row()]  # Get the patient object for the row
            column = index.column() 
            if column == 0:
                return patient.phn 
            elif column == 1:
                return self.insert_breaking_characters(patient.name)  
            elif column == 2:
                return patient.birth_date  
            elif column == 3:
                return patient.phone  
            elif column == 4:
                return self.insert_breaking_characters(patient.email)  
            elif column == 5:
                return self.insert_breaking_characters(patient.address)  

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Returns the header data for a given section and orientation.

        Parameters:
        - section: The section index (column index for horizontal headers).
        - orientation: Orientation of the header (horizontal or vertical).
        - role: The data role.

        Returns:
        - str: The header text.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

    @staticmethod
    def insert_breaking_characters(text):
        """
        Inserts zero-width spaces into long strings to allow breaking (e.g., email addresses).

        Parameters:
        - text: The text to insert breaking characters into.

        Returns:
        - str: Text with zero-width spaces.
        """
        return "\u200B".join(text)  # Insert zero-width spaces between characters


class ListAllPatientsGUI(QWidget):
    """
    GUI for displaying all patients using QTableView.
    Provides a tabular view of patient information with a back-to-menu button.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the ListAllPatientsGUI.

        Parameters:
        - controller: The Controller instance for managing business logic.
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
        title_label = QLabel("ALL PATIENTS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 20, 50, 50)
        layout.setSpacing(10)

        # Table view for displaying patients
        self.table_view = QTableView()
        self.table_view.setWordWrap(True) 
        self.table_view.setStyleSheet("""
            QTableView {
                border: 1px solid #dcdcdc;
                gridline-color: #dcdcdc;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                text-align: center;
            }
        """)  # Styling for the table
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  
        self.table_view.verticalHeader().setVisible(False)  
        self.table_view.setItemDelegate(WordWrapDelegate())  
        layout.addWidget(self.table_view)

        # Load patients and set up the model
        try:
            patients = self.controller.patient_dao.list_patients() 
            if patients:
                self.model = PatientTableModel(patients)  
                self.table_view.setModel(self.model)  
                self.table_view.resizeRowsToContents()
            else:
                QMessageBox.information(self, "No Patients", "There are no patients in the system.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

        # Back to Main Menu Button
        self.back_to_menu_button = QPushButton("Back to Menu")
        self.back_to_menu_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.back_to_menu_button.clicked.connect(self.back_to_menu_func)
        layout.addWidget(self.back_to_menu_button)

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
