# patient_record_test.py

import unittest
from clinic.patient_record import PatientRecord
from clinic.note import Note

class TestPatientRecord(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a PatientRecord instance before each test.
        """
        self.record = PatientRecord()

    def test_create_note(self):
        """
        Test if a note is correctly created and added to the record.
        """
        note = self.record.create_note("Sample note text.")
        self.assertIsInstance(note, Note, "create_note should return a Note instance")
        self.assertEqual(note.text, "Sample note text.", "The text of the note should match the input")
        self.assertEqual(note.code, 1, "The first created note should have a code of 1")

    def test_autocounter_increment(self):
        """
        Test if autocounter increments correctly with each new note.
        """
        note1 = self.record.create_note("First note")
        note2 = self.record.create_note("Second note")
        self.assertEqual(note1.code, 1, "The first note should have code 1")
        self.assertEqual(note2.code, 2, "The second note should have code 2")

    def test_search_note_existing(self):
        """
        Test searching for an existing note by code.
        """
        note = self.record.create_note("Existing note")
        found_note = self.record.search_note(note.code)
        self.assertEqual(found_note, note, "search_note should return the correct Note instance")

    def test_search_note_nonexistent(self):
        """
        Test searching for a note by code that doesn't exist.
        """
        self.record.create_note("Only note in record")
        result = self.record.search_note(999)
        self.assertIsNone(result, "search_note should return None for a nonexistent code")

    def test_update_note_existing(self):
        """
        Test updating an existing note's text.
        """
        note = self.record.create_note("Original text")
        updated_note = self.record.update_note(note.code, "Updated text")
        self.assertEqual(updated_note.text, "Updated text", "update_note should correctly update the note's text")

    def test_update_note_nonexistent(self):
        """
        Test updating a note by a code that doesn't exist.
        """
        result = self.record.update_note(999, "Attempted update")
        self.assertIsNone(result, "update_note should return None when attempting to update a nonexistent note")

    def test_retrieve_notes_by_text_match(self):
        """
        Test retrieving notes that contain specified search text.
        """
        self.record.create_note("First note about headache")
        self.record.create_note("No issues reported")
        self.record.create_note("Follow-up on headache symptoms")
        matches = self.record.retrieve_notes_by_text("headache")
        self.assertEqual(len(matches), 2, "retrieve_notes_by_text should return 2 matching notes for 'headache'")

    def test_retrieve_notes_by_text_no_match(self):
        """
        Test retrieving notes when no notes contain the specified search text.
        """
        self.record.create_note("Note about unrelated topic")
        matches = self.record.retrieve_notes_by_text("nonexistent term")
        self.assertEqual(len(matches), 0, "retrieve_notes_by_text should return an empty list if no match is found")

    def test_list_notes_reverse_order(self):
        """
        Test listing notes in reverse chronological order.
        """
        note1 = self.record.create_note("First note")
        note2 = self.record.create_note("Second note")
        listed_notes = self.record.list_notes()
        self.assertEqual(listed_notes, [note2, note1], "list_notes should return notes in reverse order of creation")

    def test_delete_existing_note(self):
        """
        Test deleting an existing note by its code.
        """
        note = self.record.create_note("To be deleted")
        result = self.record.delete_note(note.code)
        self.assertTrue(result, "delete_note should return True when a note is successfully deleted")
        self.assertIsNone(self.record.search_note(note.code), "Deleted note should not be found in the record")

    def test_delete_nonexistent_note(self):
        """
        Test attempting to delete a note by a code that doesn't exist.
        """
        result = self.record.delete_note(999)
        self.assertFalse(result, "delete_note should return False when trying to delete a nonexistent note")

    def test_no_duplicate_codes(self):
        """
        Test that each note created has a unique code.
        """
        codes = {self.record.create_note(f"Note {i}").code for i in range(5)}
        self.assertEqual(len(codes), 5, "Each note should have a unique code")

if __name__ == "__main__":
    unittest.main()