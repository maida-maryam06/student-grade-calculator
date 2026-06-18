import json
import os
import statistics
from typing import Optional

SUBJECTS = ["Math", "English", "Science", "Computer"]
DATA_FILE = "students.json"

# Letter grade boundaries (inclusive lower bound)
GRADE_BOUNDARIES = [
    (90, "A"),
    (75, "B"),
    (60, "C"),
    (40, "D"),
    (0, "F"),
]


class StudentGradeManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.students = []
        self.load_data()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.students = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.students = []
        else:
            self.students = []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.students, f, indent=2)

    
    # Helpers
    def _find_student(self, student_id: str) -> Optional[dict]:
        for student in self.students:
            if student["student_id"] == student_id:
                return student
        return None

    
    def add_student(self, name: str, student_id: str) -> dict:
        if not name or not str(name).strip():
            raise ValueError("Student name cannot be empty.")
        if not student_id or not str(student_id).strip():
            raise ValueError("Student ID cannot be empty.")
        if self._find_student(student_id) is not None:
            raise ValueError(f"Student with ID '{student_id}' already exists.")

        student = {
            "name": name,
            "student_id": student_id,
            "grades": {subject: None for subject in SUBJECTS},
        }
        self.students.append(student)
        self.save_data()
        return student

    def record_grade(self, student_id: str, subject: str, grade: float) -> None:
        
        student = self._find_student(student_id)
        if student is None:
            raise ValueError(f"No student found with ID '{student_id}'.")
        if subject not in SUBJECTS:
            raise ValueError(
                f"Invalid subject '{subject}'. Must be one of {SUBJECTS}."
            )
        try:
            grade_value = float(grade)
        except (TypeError, ValueError):
            raise ValueError("Grade must be a number.")
        if not (0 <= grade_value <= 100):
            raise ValueError("Grade must be between 0 and 100.")

        student["grades"][subject] = grade_value
        self.save_data()

    def calculate_average(self, student_id: str) -> float:
        student = self._find_student(student_id)
        if student is None:
            raise ValueError(f"No student found with ID '{student_id}'.")

        recorded = [g for g in student["grades"].values() if g is not None]
        if not recorded:
            return 0.0
        return sum(recorded) / len(recorded)

    def get_letter_grade(self, average: float) -> str:
        
        for lower_bound, letter in GRADE_BOUNDARIES:
            if average >= lower_bound:
                return letter
        return "F"  # Defensive fallback; unreachable given boundaries above.

    def get_class_rank(self, student_id: str) -> int:
        
        if self._find_student(student_id) is None:
            raise ValueError(f"No student found with ID '{student_id}'.")
        if not self.students:
            raise ValueError("No students in the class to rank.")

        averages = [
            (s["student_id"], self.calculate_average(s["student_id"]))
            for s in self.students
        ]
        # Sort by average descending.
        averages.sort(key=lambda pair: pair[1], reverse=True)

        target_average = self.calculate_average(student_id)
        # Competition ranking: rank = 1 + number of students strictly above.
        rank = 1 + sum(1 for _, avg in averages if avg > target_average)
        return rank

    def get_top_students(self, n: int) -> list:
       
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer.")

        enriched = [
            {**student, "average": self.calculate_average(student["student_id"])}
            for student in self.students
        ]
        enriched.sort(key=lambda s: s["average"], reverse=True)
        return enriched[:n]

    def find_failing_students(self) -> list:
        
        failing = []
        for student in self.students:
            avg = self.calculate_average(student["student_id"])
            if avg < 40:
                failing.append({**student, "average": avg})
        return failing

    def get_subject_stats(self, subject: str) -> dict:
       
        if subject not in SUBJECTS:
            raise ValueError(
                f"Invalid subject '{subject}'. Must be one of {SUBJECTS}."
            )

        grades = [
            s["grades"][subject]
            for s in self.students
            if s["grades"].get(subject) is not None
        ]
        if not grades:
            return {"min": 0.0, "max": 0.0, "average": 0.0, "median": 0.0}

        return {
            "min": min(grades),
            "max": max(grades),
            "average": sum(grades) / len(grades),
            "median": statistics.median(grades),
        }
