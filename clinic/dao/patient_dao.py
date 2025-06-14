from abc import ABC, abstractmethod
class PatientDAO(ABC):
    """
    An abstract base class that defines the interface for managing patient records.
    """
    @abstractmethod
    def search_patient(self, key):
        """
        Searches for a patient by a unique identifier (e.g., PHN).

        Parameters:
        - key: The unique identifier of the patient to search for.

        Return Type:
        - Patient: Returns the patient object if found, otherwise None.
        """
        pass

    @abstractmethod
    def create_patient(self, patient):
        """
        Adds a new patient to the system.

        Parameters:
        - patient: The patient object to be added.
        """
        pass

    @abstractmethod
    def retrieve_patients(self, search_string):
        """
        Retrieves all patients that match a specific search string.

        Parameters:
        - search_string: The text to search for in patient records.

        Return Type:
        - list: A list of patient objects that match the search criteria.
        """
        pass

    @abstractmethod
    def update_patient(self, key, patient):
        """
        Updates the details of an existing patient.

        Parameters:
        - key: The unique identifier of the patient to update.
        - patient: The updated patient object.
        """
        pass

    @abstractmethod
    def delete_patient(self, key):
        """
        Deletes a patient from the system by their unique identifier.

        Parameters:
        - key: The unique identifier of the patient to delete.
        """
        pass

    @abstractmethod
    def list_patients(self):
        """
        Lists all patients in the system.

        Return Type:
        - list: A list of all patient objects.
        """
        pass