import json

class PatientDecoder(json.JSONDecoder):
    """
    A custom JSON decoder for deserializing JSON objects into Patient objects.
    
    This class handles the conversion of JSON data into Patient instances, along with their
    associated records and notes. It includes custom logic to handle specific attributes 
    and types within the deserialization process.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the PatientDecoder with a custom object hook.
        
        Parameters:
        - *args, **kwargs: Additional arguments passed to the JSONDecoder constructor.
        """
        super().__init__(object_hook=self._custom_object_hook, *args, **kwargs)

    def _custom_object_hook(self, data: dict):
        """
        Processes each JSON object and converts it into a Patient instance if applicable.
        
        Parameters:
        - data (dict): The JSON object to process.

        Return Type:
        - dict or Patient: A Patient object if the structure matches, otherwise the original or modified dictionary.
        """
        # Convert keys to integers where possible
        int_converted_key = {self._convert_to_int(k): v for k, v in data.items()}

        # Import Patient-related classes to prevent circular imports
        from clinic.patient import Patient
        from clinic.patient_record import PatientRecord
        from clinic.note import Note

        # Check if the data can be converted into a Patient object
        if "phn" in int_converted_key and "name" in int_converted_key:
            # Extract and convert records into PatientRecord instances
            records = int_converted_key.get("records", [])
            patient_records = self._convert_records_to_patient_records(records, PatientRecord, Note)

            # Return a Patient object with the extracted attributes
            return Patient(
                phn=int_converted_key["phn"],
                name=int_converted_key["name"],
                birth_date=int_converted_key.get("birth_date"),
                phone=int_converted_key.get("phone_number"),
                email=int_converted_key.get("email"),
                address=int_converted_key.get("address"),
                autosave=True, # Assuming autosave is always enabled
            )
        
        # Return the processed dictionary if it doesn't match Patient attributes
        return int_converted_key

    def _convert_to_int(self,key):
        """
        Attempts to convert a key to an integer.

        Parameters:
        - key: The key to convert.

        Return Type:
        - int or original key: The key as an integer if conversion is successful, otherwise the original key.
        """
        try:
            return int(key)
        except (ValueError, TypeError):
            # Return the key unchanged if conversion fails
            return key

    def _convert_records_to_patient_records(self, records: list, PatientRecord, Note) -> list:
        """
        Converts a list of record dictionaries into PatientRecord instances.

        Parameters:
        - records (list): A list of dictionaries representing records.
        - PatientRecord (class): The PatientRecord class.
        - Note (class): The Note class.

        Return Type:
        - list: A list of PatientRecord instances with associated notes.
        """
        patient_records = []
        
        for record in records:
            # Create a new PatientRecord instance
            patient_record = PatientRecord()
            # Populate the notes in the PatientRecord instance
            patient_record.note_dao.notes = [Note(**note) for note in record.get("notes", [])]
            patient_records.append(patient_record)
        return patient_records