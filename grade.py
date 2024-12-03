from student import Student
from assignment import Assignment

class Grade:
    def __init__(self, student: 'Student', assignment: 'Assignment', score: float, feedback: str = None):
        self.__student = student  # The student associated with the grade
        self.__assignment = assignment  # The assignment associated with the grade
        self.__score = score  # The score for the assignment
        self.__feedback = feedback  # Optional feedback from the instructor
        self.validate_score()  # Ensure score is valid upon initialization

    @property
    def student(self) -> 'Student':
        return self.__student

    @property
    def assignment(self) -> 'Assignment':
        return self.__assignment

    @property
    def score(self) -> float:
        return self.__score

    @score.setter
    def score(self, value: float) -> None:
        """Update and validate the score."""
        self.__score = value
        self.validate_score()

    @property
    def feedback(self) -> str:
        return self.__feedback

    @feedback.setter
    def feedback(self, value: str) -> None:
        """Update the feedback."""
        self.__feedback = value

    def validate_score(self) -> None:
        """Validate that the score is between 0 and 100."""
        if not (0 <= self.__score <= 100):
            raise ValueError("Score must be between 0 and 100.")

    def display_grade_info(self) -> str:
        """Return a formatted string displaying the grade information."""
        feedback_display = self.feedback if self.feedback else 'No feedback'
        return (f"Student: {self.student.name} \n"
                f"Assignment: {self.assignment.title} \n"
                f"Score: {self.score:.2f} \n"
                f"Feedback: {feedback_display}")

    def to_dict(self) -> dict:
        """Convert the grade to a dictionary for serialization."""
        return {
            'student_id': self.student.student_id,
            'assignment_title': self.assignment.title,
            'score': self.score,
            'feedback': self.feedback
        }

    @classmethod
    def from_dict(cls, data: dict, students: list[Student], assignments: list[Assignment]) -> 'Grade':
        """Create a Grade object from a dictionary."""
        student = next((s for s in students if s.student_id == data['student_id']), None)
        assignment = next((a for a in assignments if a.title == data['assignment_title']), None)

        if not student:
            raise ValueError(f"Student with ID {data['student_id']} not found.")
        if not assignment:
            raise ValueError(f"Assignment titled '{data['assignment_title']}' not found.")

        return cls(student, assignment, data['score'], data.get('feedback'))