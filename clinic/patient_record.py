from clinic.note import Note
from datetime import datetime
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    """
    A class representing a patient's record, which manages a collection of notes.
    """

    def __init__(self, phn: int, autosave: bool) -> None:
        """
        Initializes a PatientRecord instance for a specific patient.

        Parameters:
        - phn (int): The unique Personal Health Number (PHN) of the patient.
        - autosave (bool): Whether to enable automatic saving of changes to notes.
        
        Return Type:
        - None
        """
        self.phn = phn
        self.autosave = autosave
        self.note_dao = NoteDAOPickle(self.phn,self.autosave) # Initialize the NoteDAOPickle instance for managing notes
        
    def create_note(self, text: str) -> Note:
        """
        Creates a new note with the given text.

        Parameters:
        - text (str): The content of the note to create.

        Return Type:
        - Note: The newly created Note instance.
        """
        return self.note_dao.create_note(text)
    
    def search_note(self, code: int) -> Note:
        """
        Searches for a note by its unique code.

        Parameters:
        - code (int): The unique identifier of the note to search for.

        Return Type:
        - Note: The note instance if found, otherwise None.
        """
        return self.note_dao.search_note(code)
    
    def update_note(self, code: int, text: str) -> bool:
        """
        Updates the content of an existing note.

        Parameters:
        - code (int): The unique identifier of the note to update.
        - text (str): The new content for the note.

        Return Type:
        - bool: Returns True if the update is successful, otherwise False.
        """
        note =  self.note_dao.update_note(code,text)
        return note

    def retrieve_notes_by_text(self, search_text: str) -> list:
        """
        Retrieves notes containing the specified search text.

        Parameters:
        - search_text (str): The text to search for in notes.

        Return Type:
        - list: A list of notes matching the search text.
        """
        search_text_lower = search_text.lower() # Convert search text to lowercase for case-insensitive matching
        return self.note_dao.retrieve_notes(search_text_lower)

    def list_notes(self) -> list:
        """
        Lists all notes in the patient's record in reverse chronological order.

        Return Type:
        - list: A list of all Note instances.
        """ 
        return self.note_dao.list_notes()
        
    def delete_note(self, code: int) -> bool:
        """
        Deletes a note by its unique code.

        Parameters:
        - code (int): The unique identifier of the note to delete.

        Return Type:
        - bool: Returns True if the note is successfully deleted, otherwise False.
        """
        return self.note_dao.delete_note(code)