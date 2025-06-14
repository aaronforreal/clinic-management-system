from datetime import datetime

class Note:
    """
    Note class with unique code, detils and current timestamp
    """

    def __init__(self, code: int, text: str, timestamp = None) -> None:
        """
        Initializes a Note instance with unique code, detils and current timestamp

        Parameters:
        - code (int): The unique identifier for the note.
        - text (str): The textual content or details of the note.

        Return Type:
        - None
        """
        self.code = code
        self.text = text
        self.timestamp = datetime.now()

    def update_details(self, text: str) -> None:
        """
        Updates the details of the note and refreshes the timestamp to the current time.

        Parameters:
        - text (str): The updated text details for the note.

        Return Type:
        - None
        """
        self.text = text
        self.timestamp = datetime.now()

    def __eq__(self, other: 'Note') -> bool:
        """
        Check if two patients have the same code

        Parameters:
        - other (Note): Another instance of the Note class to compare with.

        Return Type:
        - bool: Returns True if both notes have the same code and text, False otherwise.
        """
        return (
            isinstance(other, Note) and self.code == other.code and self.text == other.text
        )
    
    def __str__(self) -> str:
        """
        Returns a string representation of the note

        Parameters:
        - None

        Return Type:
        - str: A string describing the note's code, text, and timestamp.
        """
        return f'(Code: {self.code}, Details: {self.text}, Timestamp: {self.timestamp})'