# Student Grade Calculator (Python CLI)

A command-line **Python student grade management system** that calculates
averages, letter grades (A–F), class rank, top performers, and per-subject
statistics (min/max/average/median) for a class of students — with JSON
file persistence and a full `unittest` test suite. Built as the Python
Fundamentals task for the Enischyo Interns Python Development internship
program.

**Keywords:** python project, student grade calculator, grade management
system, CLI application, command-line tool, JSON file storage, unittest
testing, python fundamentals, beginner python project, data structures
(list of dictionaries), internship project.

## Quick start

```bash
git clone https://github.com/maida-maryam06/student-grade-calculator.git
cd student-grade-calculator
python3 main.py
```

No external dependencies — pure Python standard library (`json`, `os`,
`statistics`, `unittest`).

## Features

- Stores at least 10 student records as a list of dictionaries (no
  database yet) — each record has a name, student ID, a dict of subject
  grades (Math, English, Science, Computer), and an attendance percentage.
- Core operations, each with a docstring:
  - `add_student(name, student_id)`
  - `record_grade(student_id, subject, grade)`
  - `calculate_average(student_id)`
  - `get_letter_grade(average)` — A/B/C/D/F with explicit boundaries
  - `get_class_rank(student_id)` — rank 1 to N
  - `get_top_students(n)` — top N students sorted by average
  - `find_failing_students()` — students with average below 40
  - `get_subject_stats(subject)` — min, max, average, median for a subject
- JSON persistence: data loads from `students.json` on startup (if it
  exists) and is saved back to that file immediately after every change.
- An interactive numbered CLI menu, with `try/except` handling around all
  user input and all manager operations.
- A `unittest` suite with 10 tests covering every major function plus
  persistence and input validation.

## Project structure

```
student-grade-calculator/
├── grade_manager.py        # Core StudentGradeManager class (all logic)
├── main.py                 # CLI menu application
├── test_grade_manager.py   # unittest suite
└── README.md
```

`students.json` is created automatically the first time you run `main.py`
and add a student — it is not committed empty, since the app generates it.

## Letter grade boundaries

| Average      | Letter |
|---------------|--------|
| 90 – 100       | A      |
| 75 – 89.99     | B      |
| 60 – 74.99     | C      |
| 40 – 59.99     | D      |
| below 40       | F      |

Averages are computed only over subjects that have actually been graded —
an ungraded subject is excluded rather than counted as a zero.

## Running the app

```bash
python3 main.py
```

You'll see a menu like:

```
========================================
   STUDENT GRADE CALCULATOR
========================================
1. Add a student
2. Record a grade
3. View a student's average and letter grade
4. View a student's class rank
5. View top N students
6. View failing students (average < 40)
7. View subject statistics
8. List all students
9. Exit
========================================
```

Add at least 10 students via option 1, then use option 2 to record grades
for Math, English, Science, and Computer. Every action saves immediately
to `students.json`, so you can quit and resume later without losing data.

## Running the tests

```bash
python3 -m unittest test_grade_manager.py -v
```

The test suite uses a separate `test_students.json` file (created and
deleted automatically in `setUp`/`tearDown`), so running the tests never
touches your real `students.json` data.

### Actual test output

The following is the real output from running the test suite in this
repo (10 tests, all passing):

```
test_01_add_student (test_grade_manager.TestStudentGradeManager.test_01_add_student)
add_student should create exactly 10 students with correct fields. ... ok
test_02_record_grade (test_grade_manager.TestStudentGradeManager.test_02_record_grade)
record_grade should store a valid grade and reject invalid ones. ... ok
test_03_calculate_average (test_grade_manager.TestStudentGradeManager.test_03_calculate_average)
calculate_average should average only recorded grades. ... ok
test_04_get_letter_grade (test_grade_manager.TestStudentGradeManager.test_04_get_letter_grade)
get_letter_grade should map averages to correct letters at boundaries. ... ok
test_05_get_class_rank (test_grade_manager.TestStudentGradeManager.test_05_get_class_rank)
get_class_rank should rank students 1..N by descending average. ... ok
test_06_get_top_students (test_grade_manager.TestStudentGradeManager.test_06_get_top_students)
get_top_students should return the N highest averages, sorted descending. ... ok
test_07_find_failing_students (test_grade_manager.TestStudentGradeManager.test_07_find_failing_students)
find_failing_students should return only students averaging below 40. ... ok
test_08_get_subject_stats (test_grade_manager.TestStudentGradeManager.test_08_get_subject_stats)
get_subject_stats should compute correct min, max, average, and median. ... ok
test_09_persistence_save_and_load (test_grade_manager.TestStudentGradeManager.test_09_persistence_save_and_load)
Data saved to JSON should be correctly reloaded by a new manager instance. ... ok
test_10_add_student_validation (test_grade_manager.TestStudentGradeManager.test_10_add_student_validation)
add_student should reject empty names and empty IDs. ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.023s

OK
```

(The task asked for at least 8 tests; this suite includes 10 — 8 mapping
directly to the 8 required functions, plus persistence and validation
coverage.)

## Sample run

```
Loaded 0 student record(s) from students.json

========================================
   STUDENT GRADE CALCULATOR
========================================
1. Add a student
2. Record a grade
3. View a student's average and letter grade
4. View a student's class rank
5. View top N students
6. View failing students (average < 40)
7. View subject statistics
8. List all students
9. Exit
========================================
Choose an option (1-9): 1
Student name: Ali Raza
Student ID: S001
Student 'Ali Raza' (S001) added successfully.
```

## Design notes

- **Why a class instead of free functions?** `StudentGradeManager` wraps
  the student list and the data file path together, so the CLI and the
  tests can each create independent instances (pointing at different
  JSON files) without global state.
- **Ranking ties:** `get_class_rank` uses standard competition ranking —
  students with an identical average share the same rank (e.g. two
  students tied for the best average are both rank 1).
- **Missing grades:** A subject that hasn't been graded yet is stored as
  `None` and excluded from averages and subject statistics, rather than
  silently counted as a 0.


## License

MIT — free to use, copy, and modify.