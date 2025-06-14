import json

class PatientEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for serializing Patient and PatientRecord objects to JSON.

    This class overrides the default JSON encoding to handle custom object types,
    such as Patient and PatientRecord, and ensures their attributes are serialized
    into JSON-compatible formats.
    """
    
    def default(self, obj):
        """
        Overrides the default JSON encoding method to handle custom objects.
        
        Parameters:
        - obj: The object to serialize.

        Return Type:
        - dict: A dictionary representation of the object if it matches a recognized type.
        - Any: The default JSONEncoder behavior for unrecognized types.
        """

        # Import Patient and PatientRecord to avoid circular import issues
        from clinic.patient import Patient
        from clinic.patient_record import PatientRecord

        if isinstance(obj, Patient):
            """
            Serializes a Patient object into a dictionary.
            
            Patient attributes such as PHN, name, birth date, and records are included
            in the serialized JSON.
            """

            return {
                "phn": obj.phn,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone_number": obj.phone,
                "email": obj.email,
                "address": obj.address,
            }
        
        elif isinstance(obj, PatientRecord):
            """
            Serializes a PatientRecord object into a dictionary.
            
            Converts the list of notes in the PatientRecord into a list of dictionaries,
            using each note's `__dict__` representation.
            """
            return {
                "notes": [note.__dict__ for note in obj.note_dao.notes], # Serialize notes
            }
        
         # Fallback to default behavior for unsupported types
        return super().default(obj)