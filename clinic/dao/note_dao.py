from abc import ABC, abstractmethod

class NoteDAO(ABC):
    """
    An abstract base class that defines the interface for managing notes.
    """
    @abstractmethod
    def search_note(self, key):
        """
        Searches for a note by a unique identifier (key).

        Parameters:
        - key: The unique identifier of the note to search for.

        Return Type:
        - Note: Returns the note object if found, otherwise None.
        """
        pass

    @abstractmethod
    def create_note(self, text):
        """
        Creates a new note with the given text content.

        Parameters:
        - text: The content of the note to create.

        Return Type:
        - Note: Returns the newly created note object.
        """
        pass

    @abstractmethod
    def retrieve_notes(self, search_string):
        """
        Retrieves all notes that contain the specified search string.

        Parameters:
        - search_string: The string to search for within notes.

        Return Type:
        - list: A list of notes matching the search criteria.
        """
        pass

    @abstractmethod
    def update_note(self, key, text):
        """
        Updates the content of an existing note identified by a unique key.

        Parameters:
        - key: The unique identifier of the note to update.
        - text: The new content for the note.

        Return Type:
        - bool: Returns True if the update is successful, otherwise False.
        """
        pass

    @abstractmethod
    def delete_note(self, key):
        """
        Deletes a note by its unique identifier (key).

        Parameters:
        - key: The unique identifier of the note to delete.

        Return Type:
        - bool: Returns True if the deletion is successful, otherwise False.
        """
        pass

    @abstractmethod
    def list_notes(self):
        """
        Lists all notes currently stored.

        Return Type:
        - list: A list of all note objects.
        """
        pass