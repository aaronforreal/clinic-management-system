import json
from clinic.dao.patient_dao import PatientDAO  
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):
    """
    This class allows for operations such as creating, updating, deleting, and searching
    for patient records. Records are stored in a JSON file and can be autosaved after
    each modification if autosave is enabled.
    """
    def __init__(self, autosave: bool):
        """
        Initializes the PatientDAOJSON instance.
        
        Parameters:
        - autosave (bool): Determines whether changes are automatically saved.
        """
        self.patients = {}
        self.autosave = autosave
        self.filename = 'clinic/patients.json'

        # Load patients from file if available
        patients_loaded = self.load_patients()
        if patients_loaded and self.autosave is not None:
            self.patients = patients_loaded
        
    def load_patients(self) -> dict:
        """
        Loads patient records from the JSON file.

        Return Type:
        - dict: A dictionary of patient records if the file exists, otherwise an empty dictionary.
        """
        try:
            with open("clinic/patients.json","r") as file:
                self.patients = json.load(file,cls=PatientDecoder)
        except FileNotFoundError:
            # Return an empty dictionary if the file does not exist
            return {}

    def save_patients(self):
        """
        Saves all patient records to the JSON file.

        This method writes the current state of the `patients` dictionary to a JSON file,
        ensuring data persistence if autosave is enabled.
        """
        if self.autosave is not None:
            self.autosave
        with open(self.filename,"w") as file:
            json.dump(self.patients, file, cls=PatientEncoder)
      
    def search_patient(self, key: str):
        """
        Searches for a patient by their PHN.
        
        Parameters:
        - key (str): The PHN of the patient to search for.

        Return Type:
        - Patient: The patient object if found, otherwise None.
        """
        return self.patients.get(key)

    def create_patient(self,patient):
        """
        Adds a new patient to the records.
        
        Parameters:
        - patient (Patient): The patient object to be added.
        """
        # Add the patient to the dictionary using their PHN as the key
        self.patients[patient.phn] = patient

        if self.autosave:
            self.save_patients()

    def retrieve_patients(self, search_string: str) -> list:
        """
        Retrieves all patients whose names contain the specified search string.
        
        Parameters:
        - search_string (str): The string to search for in patient names.
        
        Return Type:
        - list: A list of patients matching the search string, or an empty list if none match.
        """
        # Perform a case-insensitive search in patient names
        matching_patients = [patient for patient in self.patients.values() if search_string.lower() in patient.name.lower()]

        if matching_patients:
            return matching_patients
        return []

    def update_patient(self, key: str, patient):
        """
        Updates an existing patient's record.
        
        Parameters:
        - key (str): The PHN of the patient to update.
        - patient (Patient): The updated patient object.
        """
        if key in self.patients:
            # Replace the patient record with the updated object
            self.patients[key] = patient

        if self.autosave:
            self.save_patients()
    
    def delete_patient(self, key: str):
        """
        Deletes a patient record by their PHN.
        
        Parameters:
        - key (str): The PHN of the patient to delete.
        """
        if key in self.patients:
            # Remove the patient record from the dictionary
            del self.patients[key]
            
        if self.autosave:
            self.save_patients()

    def list_patients(self):
        """
        Lists all patient records.
        
        Return Type:
        - list: A list of all patient objects in the system.
        """
        return list(self.patients.values())