from typing import List, Dict, Union
from student import Student
from course import Course

class Enrollment:
    def __init__(self):
        self._enrollments: List[Dict[str, Union[Student, Course]]] = []  # List to track enrollments

    def enroll_student(self, student: Student, course: Course) -> None:
        """
        Enroll a student in a course if they are not already enrolled.
        """
        if not self.is_student_enrolled(student, course):
            course.add_student(student)  # Assuming the 'Course' class has a method to add students
            self._enrollments.append({'student': student, 'course': course})
            print(f"{student.name} has been enrolled in {course.course_name}.")
        else:
            print(f"{student.name} is already enrolled in {course.course_name}.")

    def is_student_enrolled(self, student: Student, course: Course) -> bool:
        """
        Check if a student is already enrolled in a specific course.
        """
        return any(enrollment['student'] == student and enrollment['course'] == course for enrollment in self._enrollments)

    def unenroll_student(self, student: Student, course: Course) -> None:
        """
        Unenroll a student from a course if they are enrolled.
        """
        for enrollment in self._enrollments:
            if enrollment['student'] == student and enrollment['course'] == course:
                course.remove_student(student)  # Assuming the 'Course' class has a method to remove students
                self._enrollments.remove(enrollment)
                print(f"{student.name} has been unenrolled from {course.course_name}.")
                return
        print(f"{student.name} is not enrolled in {course.course_name}.")

    def get_enrollment_list(self) -> List[str]:
        """
        Return a list of all enrollments in a readable format.
        """
        if not self._enrollments:
            return ["No enrollments found."]
        return [
            f"{enrollment['student'].name} enrolled in {enrollment['course'].course_name}"
            for enrollment in self._enrollments
        ]

    def display_enrollments(self) -> None:
        """
        Display all enrollments in a user-friendly format.
        """
        enrollments = self.get_enrollment_list()
        print("Current Enrollments:")
        for enrollment in enrollments:
            print(f"- {enrollment}")

    def get_courses_by_student(self, student: Student) -> List[Course]:
        """
        Get a list of courses a specific student is enrolled in.
        """
        return [enrollment['course'] for enrollment in self._enrollments if enrollment['student'] == student]

    def get_students_by_course(self, course: Course) -> List[Student]:
        """
        Get a list of students enrolled in a specific course.
        """
        return [enrollment['student'] for enrollment in self._enrollments if enrollment['course'] == course]