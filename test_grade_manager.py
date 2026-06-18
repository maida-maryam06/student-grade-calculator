"""
test_grade_manager.py

Unit tests for grade_manager.StudentGradeManager.

Run with:
    python -m unittest test_grade_manager.py -v

Each test uses a temporary JSON file so that running the tests never
touches the real students.json used by the CLI app.
"""

import os
import unittest

from grade_manager import StudentGradeManager


class TestStudentGradeManager(unittest.TestCase):
    """Test suite covering each major function of StudentGradeManager."""

    TEST_FILE = "test_students.json"

    def setUp(self):
        """Create a fresh manager with 10 students before each test."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
        self.manager = StudentGradeManager(data_file=self.TEST_FILE)

        # Seed 10 students as required by the assignment.
        self.student_ids = []
        for i in range(1, 11):
            sid = f"S{i:03d}"
            self.manager.add_student(f"Student {i}", sid)
            self.student_ids.append(sid)

    def tearDown(self):
        """Remove the temporary JSON file after each test."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    # ------------------------------------------------------------------
    def test_01_add_student(self):
        """add_student should create exactly 10 students with correct fields."""
        self.assertEqual(len(self.manager.students), 10)
        first = self.manager.students[0]
        self.assertEqual(first["name"], "Student 1")
        self.assertEqual(first["student_id"], "S001")
        self.assertEqual(set(first["grades"].keys()), {"Math", "English", "Science", "Computer"})

        # Duplicate ID should raise.
        with self.assertRaises(ValueError):
            self.manager.add_student("Duplicate", "S001")

    def test_02_record_grade(self):
        """record_grade should store a valid grade and reject invalid ones."""
        self.manager.record_grade("S001", "Math", 88)
        self.assertEqual(self.manager.students[0]["grades"]["Math"], 88.0)

        with self.assertRaises(ValueError):
            self.manager.record_grade("S001", "Math", 150)  # out of range

        with self.assertRaises(ValueError):
            self.manager.record_grade("S001", "History", 80)  # invalid subject

        with self.assertRaises(ValueError):
            self.manager.record_grade("NOPE", "Math", 80)  # unknown student

    def test_03_calculate_average(self):
        """calculate_average should average only recorded grades."""
        self.manager.record_grade("S002", "Math", 80)
        self.manager.record_grade("S002", "English", 90)
        # Science and Computer left ungraded -> should be excluded.
        avg = self.manager.calculate_average("S002")
        self.assertAlmostEqual(avg, 85.0)

        # A student with no grades at all should average to 0.0.
        self.assertEqual(self.manager.calculate_average("S003"), 0.0)

    def test_04_get_letter_grade(self):
        """get_letter_grade should map averages to correct letters at boundaries."""
        self.assertEqual(self.manager.get_letter_grade(95), "A")
        self.assertEqual(self.manager.get_letter_grade(90), "A")
        self.assertEqual(self.manager.get_letter_grade(89.99), "B")
        self.assertEqual(self.manager.get_letter_grade(75), "B")
        self.assertEqual(self.manager.get_letter_grade(74.99), "C")
        self.assertEqual(self.manager.get_letter_grade(60), "C")
        self.assertEqual(self.manager.get_letter_grade(59.99), "D")
        self.assertEqual(self.manager.get_letter_grade(40), "D")
        self.assertEqual(self.manager.get_letter_grade(39.99), "F")
        self.assertEqual(self.manager.get_letter_grade(0), "F")

    def test_05_get_class_rank(self):
        """get_class_rank should rank students 1..N by descending average."""
        # Give distinct averages: S001 highest, S002 second, rest 0.
        self.manager.record_grade("S001", "Math", 100)
        self.manager.record_grade("S002", "Math", 90)

        self.assertEqual(self.manager.get_class_rank("S001"), 1)
        self.assertEqual(self.manager.get_class_rank("S002"), 2)

        # Unknown student should raise.
        with self.assertRaises(ValueError):
            self.manager.get_class_rank("UNKNOWN")

    def test_06_get_top_students(self):
        """get_top_students should return the N highest averages, sorted descending."""
        self.manager.record_grade("S001", "Math", 60)
        self.manager.record_grade("S002", "Math", 95)
        self.manager.record_grade("S003", "Math", 80)

        top_2 = self.manager.get_top_students(2)
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0]["student_id"], "S002")
        self.assertEqual(top_2[1]["student_id"], "S003")

        with self.assertRaises(ValueError):
            self.manager.get_top_students(0)

    def test_07_find_failing_students(self):
        """find_failing_students should return only students averaging below 40."""
        self.manager.record_grade("S001", "Math", 30)  # failing
        self.manager.record_grade("S002", "Math", 70)  # passing

        failing = self.manager.find_failing_students()
        failing_ids = {s["student_id"] for s in failing}

        self.assertIn("S001", failing_ids)
        self.assertNotIn("S002", failing_ids)
        # All students without grades (average 0.0) also count as failing.
        self.assertIn("S004", failing_ids)

    def test_08_get_subject_stats(self):
        """get_subject_stats should compute correct min, max, average, and median."""
        self.manager.record_grade("S001", "English", 60)
        self.manager.record_grade("S002", "English", 80)
        self.manager.record_grade("S003", "English", 100)

        stats = self.manager.get_subject_stats("English")
        self.assertEqual(stats["min"], 60)
        self.assertEqual(stats["max"], 100)
        self.assertAlmostEqual(stats["average"], 80.0)
        self.assertEqual(stats["median"], 80)

        with self.assertRaises(ValueError):
            self.manager.get_subject_stats("History")

    def test_09_persistence_save_and_load(self):
        """Data saved to JSON should be correctly reloaded by a new manager instance."""
        self.manager.record_grade("S001", "Math", 77)

        reloaded = StudentGradeManager(data_file=self.TEST_FILE)
        self.assertEqual(len(reloaded.students), 10)
        self.assertEqual(reloaded.students[0]["grades"]["Math"], 77.0)

    def test_10_add_student_validation(self):
        """add_student should reject empty names and empty IDs."""
        with self.assertRaises(ValueError):
            self.manager.add_student("", "S100")
        with self.assertRaises(ValueError):
            self.manager.add_student("No ID", "")


if __name__ == "__main__":
    unittest.main()
