"""
main.py

Command-line interface for the Student Grade Calculator.

Run this file to launch an interactive menu that lets you add students,
record grades, and view averages, rankings, and statistics. All changes
are saved immediately to students.json.
"""

from grade_manager import StudentGradeManager, SUBJECTS

MENU_TEXT = """
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
"""


def prompt_int(prompt_text: str) -> int:
    """Prompt the user until a valid integer is entered.

    Args:
        prompt_text: The text to display to the user.

    Returns:
        The integer the user entered.
    """
    while True:
        try:
            return int(input(prompt_text))
        except ValueError:
            print("Please enter a valid whole number.")


def prompt_float(prompt_text: str) -> float:
    """Prompt the user until a valid number is entered.

    Args:
        prompt_text: The text to display to the user.

    Returns:
        The float the user entered.
    """
    while True:
        try:
            return float(input(prompt_text))
        except ValueError:
            print("Please enter a valid number.")


def choose_subject() -> str:
    """Display the subject list and let the user pick one by number.

    Returns:
        The chosen subject name as a string.
    """
    print("Subjects:")
    for i, subject in enumerate(SUBJECTS, start=1):
        print(f"  {i}. {subject}")
    while True:
        choice = prompt_int("Choose a subject number: ")
        if 1 <= choice <= len(SUBJECTS):
            return SUBJECTS[choice - 1]
        print(f"Please enter a number between 1 and {len(SUBJECTS)}.")


def print_student_summary(student: dict, manager: StudentGradeManager) -> None:
    """Print a one-line summary of a student including average and letter grade."""
    avg = manager.calculate_average(student["student_id"])
    letter = manager.get_letter_grade(avg)
    print(
        f"  {student['student_id']:<8} {student['name']:<20} "
        f"avg={avg:6.2f}  grade={letter}"
    )


def handle_add_student(manager: StudentGradeManager) -> None:
    """Handle menu option: add a new student."""
    try:
        name = input("Student name: ").strip()
        student_id = input("Student ID: ").strip()
        manager.add_student(name, student_id)
        print(f"Student '{name}' ({student_id}) added successfully.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_record_grade(manager: StudentGradeManager) -> None:
    """Handle menu option: record a grade for a student."""
    try:
        student_id = input("Student ID: ").strip()
        subject = choose_subject()
        grade = prompt_float(f"Grade for {subject} (0-100): ")
        manager.record_grade(student_id, subject, grade)
        print("Grade recorded successfully.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_view_average(manager: StudentGradeManager) -> None:
    """Handle menu option: view a student's average and letter grade."""
    try:
        student_id = input("Student ID: ").strip()
        avg = manager.calculate_average(student_id)
        letter = manager.get_letter_grade(avg)
        print(f"Average: {avg:.2f}  |  Letter grade: {letter}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_view_rank(manager: StudentGradeManager) -> None:
    """Handle menu option: view a student's class rank."""
    try:
        student_id = input("Student ID: ").strip()
        rank = manager.get_class_rank(student_id)
        print(f"Class rank: {rank} out of {len(manager.students)}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_top_students(manager: StudentGradeManager) -> None:
    """Handle menu option: view top N students."""
    try:
        n = prompt_int("How many top students to show? ")
        top = manager.get_top_students(n)
        if not top:
            print("No students in the class yet.")
            return
        print(f"Top {len(top)} student(s):")
        for student in top:
            letter = manager.get_letter_grade(student["average"])
            print(
                f"  {student['student_id']:<8} {student['name']:<20} "
                f"avg={student['average']:6.2f}  grade={letter}"
            )
    except ValueError as e:
        print(f"Error: {e}")


def handle_failing_students(manager: StudentGradeManager) -> None:
    """Handle menu option: view all failing students."""
    failing = manager.find_failing_students()
    if not failing:
        print("No failing students. Nice!")
        return
    print(f"{len(failing)} failing student(s):")
    for student in failing:
        print(f"  {student['student_id']:<8} {student['name']:<20} avg={student['average']:6.2f}")


def handle_subject_stats(manager: StudentGradeManager) -> None:
    """Handle menu option: view stats for a subject."""
    try:
        subject = choose_subject()
        stats = manager.get_subject_stats(subject)
        print(f"Stats for {subject}:")
        print(f"  Min:     {stats['min']:.2f}")
        print(f"  Max:     {stats['max']:.2f}")
        print(f"  Average: {stats['average']:.2f}")
        print(f"  Median:  {stats['median']:.2f}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_list_all(manager: StudentGradeManager) -> None:
    """Handle menu option: list all students with their averages."""
    if not manager.students:
        print("No students in the class yet.")
        return
    print(f"All students ({len(manager.students)}):")
    for student in manager.students:
        print_student_summary(student, manager)


def main():
    """Run the interactive command-line menu loop."""
    manager = StudentGradeManager()
    print("Loaded", len(manager.students), "student record(s) from", manager.data_file)

    actions = {
        "1": handle_add_student,
        "2": handle_record_grade,
        "3": handle_view_average,
        "4": handle_view_rank,
        "5": handle_top_students,
        "6": handle_failing_students,
        "7": handle_subject_stats,
        "8": handle_list_all,
    }

    while True:
        print(MENU_TEXT)
        choice = input("Choose an option (1-9): ").strip()

        if choice == "9":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](manager)
        else:
            print("Invalid option. Please choose a number from 1 to 9.")


if __name__ == "__main__":
    main()
