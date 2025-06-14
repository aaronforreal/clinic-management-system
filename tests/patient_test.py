# patient_test.py

import unittest
from clinic.patient import Patient
from clinic.controller import Controller
from datetime import datetime

class TestPatient(unittest.TestCase):

    def setUp(self):
        """Set up a Controller instance and login before each test."""
        self.controller = Controller()
        self.controller.login("user", "clinic2024")

    def test_create_search_patient(self):
        """Test creating and searching for patients in the controller."""
        # Expected patients
        expected_patient_1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

        # Add and search for the first patient
        actual_patient = self.controller.create_patient(expected_patient_1.phn, expected_patient_1.name, expected_patient_1.birth_date, expected_patient_1.phone, expected_patient_1.email, expected_patient_1.address)
        self.assertEqual(actual_patient, expected_patient_1, "Created patient John Doe should match expected data")

        # Verify searching for the patient works
        found_patient = self.controller.search_patient(expected_patient_1.phn)
        self.assertEqual(found_patient, expected_patient_1, "Found patient should match created patient")

        # Attempt to create a patient with duplicate PHN
        duplicate_patient = self.controller.create_patient(expected_patient_1.phn, "Duplicate Doe", "1990-01-01", "250 000 0000", "duplicate@gmail.com", "400 Different St")
        self.assertIsNone(duplicate_patient, "Creating a patient with duplicate PHN should return None")

        # Add and verify the second patient
        actual_patient = self.controller.create_patient(expected_patient_2.phn, expected_patient_2.name, expected_patient_2.birth_date, expected_patient_2.phone, expected_patient_2.email, expected_patient_2.address)
        self.assertEqual(actual_patient, expected_patient_2, "Created patient Mary Doe should match expected data")

    def test_retrieve_patients(self):
        """Test retrieving patients by partial and exact names."""
        # Create several patients
        self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd")
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St")
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St")

        # Retrieve patients by surname
        retrieved_patients = self.controller.retrieve_patients("Doe")
        self.assertEqual(len(retrieved_patients), 2, "Retrieving patients by surname 'Doe' should return 2 matches")
        self.assertEqual(retrieved_patients[0].name, "John Doe", "First retrieved patient should be John Doe")
        self.assertEqual(retrieved_patients[1].name, "Mary Doe", "Second retrieved patient should be Mary Doe")

        # Attempt retrieval for a name with no matches
        retrieved_patients = self.controller.retrieve_patients("Smith")
        self.assertEqual(len(retrieved_patients), 0, "Retrieving patients by a non-existing name should return 0 matches")

    def test_update_patient(self):
        """Test updating patient information with and without changing PHN."""
        # Initial patient setup
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St")

        # Update patient information without changing PHN
        updated = self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "250 203 2021", "john.doe@hotmail.com", "301 Moss St")
        self.assertTrue(updated, "Updating patient information without changing PHN should succeed")
        
        # Confirm patient information updated
        updated_patient = self.controller.search_patient(9790012000)
        expected_patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 2021", "john.doe@hotmail.com", "301 Moss St")
        self.assertEqual(updated_patient, expected_patient, "Updated patient data should match the new information")

        # Attempt to change PHN to an existing one (conflict)
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St")
        updated = self.controller.update_patient(9790012000, 9790014444, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St")
        self.assertFalse(updated, "Updating PHN to an existing PHN should fail")

if __name__ == "__main__":
    unittest.main()