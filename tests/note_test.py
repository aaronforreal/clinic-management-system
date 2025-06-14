# note_test.py

import unittest
from datetime import datetime, timedelta
from clinic.note import Note

class NoteTests(unittest.TestCase):

    def setUp(self):
        # Setting up a common timestamp for consistency in certain tests
        self.timestamp = datetime(2024, 10, 27, 10, 30)

    def test_identical_notes(self):
        """Test if two identical notes are considered equal."""
        note1 = Note(1, "This is a test note.")
        note2 = Note(1, "This is a test note.")
        note2.timestamp = note1.timestamp  # Align timestamps for equality
        self.assertEqual(note1, note2, "Identical notes should be equal")

    def test_different_codes(self):
        """Test notes with different codes."""
        note1 = Note(1, "This is a test note.")
        note2 = Note(2, "This is a test note.")
        self.assertNotEqual(note1, note2, "Notes with different codes should not be equal")

    def test_different_text(self):
        """Test notes with the same code but different text."""
        note1 = Note(1, "This is a test note.")
        note2 = Note(1, "This is a different test note.")
        self.assertNotEqual(note1, note2, "Notes with different text should not be equal")

    def test_non_note_comparison(self):
        """Test comparison of a Note object with a non-Note object."""
        note = Note(1, "This is a test note.")
        self.assertNotEqual(note, "Some string", "Comparing Note to a non-Note object should return False")

    def test_update_details(self):
        """Test updating the details of a note."""
        note = Note(1, "Initial text.")
        old_timestamp = note.timestamp
        note.update_details("Updated text.")
        self.assertEqual(note.text, "Updated text.", "The note's text should be updated correctly.")

    def test_update_details_with_same_text(self):
        """Test updating details with the same text."""
        note = Note(1, "Repeated text.")
        old_timestamp = note.timestamp
        note.update_details("Repeated text.")
        self.assertEqual(note.text, "Repeated text.", "The note's text should remain the same.")

    def test_timestamp_initialization(self):
        """Test if timestamp is correctly initialized."""
        note = Note(1, "Checking timestamp.")
        self.assertIsInstance(note.timestamp, datetime, "Timestamp should be an instance of datetime")

    def test_string_representation(self):
        """Test the string representation of a Note."""
        note = Note(1, "Sample note text.")
        note.timestamp = self.timestamp  # Set timestamp for predictable output
        expected_str = f'(Code: 1, Details: Sample note text., Timestamp: {self.timestamp})'
        self.assertEqual(str(note), expected_str, "String representation should match expected format")

if __name__ == "__main__":
    unittest.main()