import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
)


class QuitGUI(QWidget):
    """
    GUI for displaying a session termination screen.
    Includes a central message and an inspirational quote.
    """

    def __init__(self, parent=None):
        """
        Initializes the QuitGUI.

        Parameters:
        - parent: The parent widget, typically None for a standalone window.
        """
        super().__init__(parent)

        # Create the main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) 
        layout.setSpacing(0)  
        self.setLayout(layout)

        # Add a spacer at the top to push elements to the center
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_top)

        # Add the main session finished message
        label = QLabel("SESSION FINISHED.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        label.setStyleSheet("font-size: 48px; font-weight: bold; margin-bottom: 0px;") 
        layout.addWidget(label)

        # Add the inspirational quote below the main message
        quote_label = QLabel(
            "“Do as much as possible for the patient,\n"
            "and as little as possible to the patient.”\n"
            "— Sigmund Freud"
        )
        quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_label.setStyleSheet("font-size: 20px; font-style: italic; color: gray; margin-top: 10px;")  
        layout.addWidget(quote_label)

        # Add a spacer at the bottom to keep elements vertically centered
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_bottom)


if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window = QuitGUI()  
    window.show()  
    sys.exit(app.exec())  
