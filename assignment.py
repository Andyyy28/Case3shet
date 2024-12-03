from datetime import datetime  # Correctly import datetime

class Assignment:
    def __init__(self, title: str, description: str, due_date: datetime, course):
        self.__title = title
        self.__description = description
        self.__due_date = due_date  # Expecting a datetime object
        self.__course = course  # The course to which this assignment belongs
        self.grades = []  # Initialize grades list

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def due_date(self) -> datetime:
        return self.__due_date

    @property
    def course(self):
        return self.__course

    def is_overdue(self) -> bool:
        """Check if the assignment is overdue."""
        return datetime.now() > self.__due_date

    def display_info(self) -> str:
        """Display information about the assignment."""
        course_name = self.course.course_name if hasattr(self.course, 'course_name') else "Unknown Course"
        return (f"Assignment: {self.title} \n"
                f"Description: {self.description} \n"
                f"Due Date: {self.due_date.strftime('%Y-%m-%d %H:%M:%S')} \n"
                f"Course: {course_name}")

    def add_grade(self, grade: float, feedback: str = '', student_id: str = '') -> None:
        """Add a grade to the assignment, along with optional feedback."""
        if not (0 <= grade <= 100):
            print("Error: Grade must be between 0 and 100.")
            return
        if any(g['student_id'] == student_id for g in self.grades):
            print(f"Grade for student {student_id} already exists for this assignment.")
            return
        self.grades.append({'score': grade, 'student_id': student_id, 'feedback': feedback})
        print(f"Grade of {grade} added for student {student_id} to '{self.title}'.")

    def average_grade(self) -> float:
        """Calculate and return the average grade for the assignment."""
        valid_grades = [grade['score'] for grade in self.grades if grade['score'] >= 0]  # Example of excluding invalid grades
        if not valid_grades:
            return 0.0
        return sum(valid_grades) / len(valid_grades)

    def grade_count(self) -> int:
        """Return the number of grades entered for this assignment."""
        return len(self.grades)

    def display_grades(self):
        """Display all grades for this assignment."""
        if not self.grades:
            print("No grades entered yet.")
        for idx, grade in enumerate(self.grades, start=1):
            print(f"Grade {idx}: {grade['score']} - Feedback: {grade['feedback']} - Student: {grade.get('student_id', 'Unknown')}")