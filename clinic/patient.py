from clinic.patient_record import PatientRecord

class Patient:
    """ 
    Patient class with unique Personal health number, name, birthdate, phone,
    email and address 
    """

    def __init__(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str, autosave = False) -> None:
        """ Initializes an instance of a Patient class with unique Personal health number, name, 
            birthdate, phone, email and address and patient record

        Parameters:
        - phn (int): The unique Personal Health Number (PHN) of the patient.
        - name (str): The patient's full name.
        - birth_date (str): The patient's birth date, in string format (assumed format: 'YYYY-MM-DD').
        - phone (str): The patient's phone number.
        - email (str): The patient's email address.
        - address (str): The patient's home address.
        - autosave (bool, optional): Determines whether changes to the patient's record 
        are automatically saved. Defaults to False.

        Return Type:
        - None
        """
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave
        self.record = PatientRecord(self.phn,self.autosave)
        
    def get_patient_record(self) -> 'PatientRecord':
        """
        Retrieves the patient's associated record.

        Return Type:
        - PatientRecord: The patient's record object, which manages notes and other related data.
        """
        return self.record
        
    def __eq__(self, other: 'Patient') -> bool:
        """
        Check if two patients are equal based on their PHN

        Parameters:
        - other (Patient): Another instance of the Patient class for comparison.

        Return Type:
        - bool: Returns True if all attributes of both patients match, False otherwise.
        """
        if not isinstance(other, Patient):
            return False
        # Compares all patient attributes to determine equality
        return (
            self.phn == other.phn and
            self.name == other.name and
            self.birth_date == other.birth_date and
            self.phone == other.phone and
            self.email == other.email and
            self.address == other.address
        )
    
    def __str__(self) -> str:
        """
        Return a string representation of the patient

        Parameters:
        - None

        Return Type:
        - str: A string detailing the patient's PHN, name, birth date, phone, email, and address.
        """
        return f'''Patient(PHN: {self.phn}, Name: {self.name}, Birth {self.birth_date}, Phone {self.phone},
        Email {self.email}, Address {self.address})'''

    def create_note(self, text: str) -> None:
        """
        Creates a new note in the patient's record.

        Parameters:
        - text (str): The text content of the note to be added.

        Return Type:
        - None
        """
        return self.record.create_note(text)
        
    def search_note(self, code: int) -> None:
        """
        Searches for a note by its code in the patient's record.

        Parameters:
        - code (int): The unique code of the note to search for.

        Return Type:
        - Note: Returns the Note instance if found, or None if no matching note exists.
        """
        return self.record.search_note(code)

    def retrieve_notes_by_text(self, search_text: str) -> list:
        """
        Retrieves all notes containing the specified text.

        Parameters:
        - search_text (str): Text to search for within the notes' details.

        Return Type:
        - list: A list of Note instances that contain the search text.
        """
        return  self.record.retrieve_notes_by_text(search_text)

    def delete_note(self, code: int) -> bool:
        """
        Deletes a note by its unique code.

        Parameters:
        - code (int): The unique code of the note to delete.

        Return Type:
        - bool: Returns True if the note was successfully deleted, False otherwise.
        """
        return self.record.delete_note(code)

    def  update_note(self, code: int, text: str) -> bool:
        """
        Updates an existing note's details by its code.

        Parameters:
        - code (int): The unique code of the note to update.
        - text (str): The new text to update the note with.

        Return Type:
        - bool: Returns True if the note was successfully updated, False otherwise.
        """
        return self.record.update_note(code,text)

    def list_notes(self) -> list:
        """
        Lists all notes in the patient's record.

        Parameters:
        - None

        Return Type:
        - list: A list of all Note instances in the patient's record.
        """
        return self.record.list_notes()