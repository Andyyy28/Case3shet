from datetime import datetime
import json
import os
from typing import List
from discussion import DiscussionThread
from student import Student
from instructor import Instructor
from platform_admin import PlatformAdmin
from announcement import Announcement
from course import Course

class E_Learning_Environment:
    mission = "To provide quality education through innovative technology."
    vision = "To become a leading platform fostering accessible learning for all."

    def __init__(self):
        self.platform_admin = PlatformAdmin()
        self.platform_admin.load_data()  # Load data on startup
        self.courses = self.platform_admin.courses
        self.students = self.platform_admin.students
        self.instructors = self.platform_admin.instructors
        self.announcements = []
        self.discussions = []


    def set_courses(self, courses):
        self.courses = courses

    @classmethod
    def display_mission(cls):
        """Class method to display the mission statement."""
        print("\n🌟 Mission:")
        print(f"   {cls.mission}")

    @classmethod
    def display_vision(cls):
        """Class method to display the vision statement."""
        print("\n🌟 Vision:")
        print(f"   {cls.vision}")



    def main_menu(self):
        while True:
            print("=" * 50)
            print("🎓 Welcome to the E-Learning Environment 🎓".center(50))
            print("=" * 50)
            # Display mission and vision using class methods
            E_Learning_Environment.display_mission()
            E_Learning_Environment.display_vision()
            print("-" * 50)
            print("\nSign in as? Student(1) or Instructor(2)")
            print("1. Student")
            print("2. Instructor")
            print("3. Sign in as Admin")
            print("4. Exit")
            print("-" * 50)
            choice = input("Select an option: ") 

            if choice == "1":
                self.student_menu()
            elif choice == "2":
                self.instructor_menu()
            elif choice == "3":
                if self.platform_admin.admin_login():  # Static method call
                    self.admin_menu()
            elif choice == "4":
                self.platform_admin.save_data()  # Save data on exit
                print("Exiting the platform. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def student_menu(self):
        student = self.get_student_by_name()
        if not student:
            print("Student not found.")
            return

        while True:
            print(f"\nWelcome, {student.name}")
            print("1. View My Grades")
            print("2. Submit Assignment")
            print("3. Enroll in Courses")
            print("4. View All Enrolled Courses")
            print("5. View Discussion Threads")
            print("6. Display All Schedule")
            print("7. View Announcements")
            print("8. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                self.view_student_grades(student)
            elif choice == "2":
                self.submit_assignment(student)
            elif choice == "3":
                self.enroll_in_courses(student)
            elif choice == "4":
                self.view_student_courses(student)
            elif choice == "5":
                self.view_discussion_threads(student)
            elif choice == "6":
                self.display_all_schedules()
            elif choice == "7":
                self.view_announcements(student)
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def get_student_by_name(self):
        name = input("Enter your name: ")
        return next((s for s in self.platform_admin.students if s.name == name), None)

    def view_student_grades(self, student):
        print(f"\nGrades for {student.name}:")
        found_grades = False

        # Check the student's own grades
        for grade_info in student.grades:
            found_grades = True
            print(f"Course: {grade_info['course_name']} (Code: {grade_info['course_code']}), Grade: {grade_info['grade']}")

        # Alternatively, check enrollments if needed
        for enrollment in self.enrollments:
            if enrollment.get('student_id') == student.student_id:
                found_grades = True
                print(f"Course: {enrollment['course_name']} (Code: {enrollment['course_code']}), Grade: {enrollment.get('grade', 'N/A')}")

        if not found_grades:
            print("No grades found.")

    def submit_assignment(self, student):
        print("\nYour Courses:")
        for course in student.enrolled_courses:
            print(f"- {course.course_name}")

        course_name = input("Enter the course name for which you want to submit an assignment: ").strip()
        course = next((c for c in student.enrolled_courses if c.course_name == course_name), None)

        if not course:
            print("You are not enrolled in this course.")
            return

        assignment_title = input("Enter the assignment title: ").strip()
        assignment = next((a for a in course.assignments if a.title == assignment_title), None)

        if not assignment:
            print("Assignment not found in this course.")
            return

        submission_content = input("Enter your submission content: ").strip()
        print(f"Assignment '{assignment_title}' submitted successfully for course '{course_name}'.")
        print(f"Submission Content: {submission_content}")

    def enroll_in_courses(self, student):
        print("\nAvailable Courses:")
        for course in self.platform_admin.courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")

        course_name = input("Enter the course name to enroll in: ")
        course = next((c for c in self.platform_admin.courses if c.course_name == course_name), None)

        if course:
            # Check if the student is already enrolled
            if course in student.enrolled_courses:
                print(f"You are already enrolled in {course_name}.")
            else:
                self.platform_admin.enrollments.enroll_student(student, course)
                print(f"Enrolled in {course_name} successfully!")
        else:
            print("Course not found.")

    def view_student_courses(self, student):
        print(f"\nEnrolled Courses for {student.name}:")
        if not student.enrolled_courses:
            print("You are not enrolled in any courses.")
            return

        for course in student.enrolled_courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")


    def display_all_schedules(self):
        print("All schedules:")
        for course in self.courses:
            if hasattr(course, 'schedule') and course.schedule:  # Ensure the course has a schedule
                print(course.schedule.display_schedule())
            else:
                print(f"Course: {course.course_name} has no schedule assigned.")


    def instructor_menu(self):
        instructor = self.get_instructor_by_name()
        if not instructor:
            print("Instructor not found.")
            return

        while True:
            print(f"\nWelcome, {instructor.name}")
            print("1. Assign Assignments")
            print("2. Input Grades")
            print("3. View Enrolled Students")
            print("4. View Courses Taught")
            print("5. View Discussion Threads")
            print("6. Create Announcements")
            print("7. View Announcements")
            print("8. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                self.assign_assignments(instructor)
            elif choice == "2":
                self.input_grades(instructor)
            elif choice == "3":
                self.view_enrolled_students(instructor)
            elif choice == "4":
                self.view_courses_taught(instructor)
            elif choice == "5":
                self.view_discussion_threads(instructor)
            elif choice == "6":
                title = input("Enter announcement title: ")
                content = input("Enter announcement content: ")
                date = input("Enter announcement date (YYYY-MM-DD): ")
                recipient_groups = input("Enter recipient groups (e.g., Student, Instructor, Admin): ").split(", ")
                self.create_announcement(title, content, date, recipient_groups)
            elif choice == "7":
                self.view_announcements(instructor)
            elif choice == "8":
                print(f"Goodbye, {instructor.name}!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def get_instructor_by_name(self):
        name = input("Enter your name: ")
        return next((i for i in self.platform_admin.instructors if i.name == name), None)

    def assign_assignments(self, instructor):
        print("Available Courses:")
        for course in self.platform_admin.courses:
            if course.instructor.instructor_id == instructor.instructor_id:
                print(f"- {course.course_name} ({course.course_code})")

        course_code = input("Enter the course code to assign an assignment: ")
        course = next((c for c in self.platform_admin.courses if c.course_code == course_code), None)

        if course:
            title = input("Enter assignment title: ")
            description = input("Enter assignment description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            course.assign_assignment(title, description, due_date)
        else:
            print("Course not found.")

    def input_grades(self, instructor):
        # Get the course code and find the corresponding course taught by the instructor
        course_code = input("Enter the course code: ")
        course = next(
            (c for c in self.platform_admin.courses if c.course_code == course_code and c.instructor == instructor),
        None
    )

        if course:
            # Proceed to input grades for the students in this course
            student_id = input("Enter the student ID: ")
            grade = input("Enter the grade: ")

            # Add grade for the student (assuming the course has a list of enrolled students)
            student = next((s for s in course.enrolled_students if s.student_id == student_id), None)
            if student:
                student.add_grade(course, grade)  # Assuming there's a method to add grades to the student
                print(f"Grade for student {student.name} in course {course.course_name} is {grade}.")
            else:
                print(f"Student with ID {student_id} is not enrolled in this course.")
        else:
            print(f"Course with code {course_code} not found.")

    def view_enrolled_students(self, instructor):
        """Display a list of students enrolled in the courses taught by the instructor."""
        print("\nCourses Taught:")
        instructor_courses = [course for course in self.platform_admin.courses if course.instructor.instructor_id == instructor.instructor_id]

        if not instructor_courses:
            print("You are not teaching any courses.")
            return

        for course in instructor_courses:
            print(f"\nCourse: {course.course_name} (Code: {course.course_code})")
            if not course.enrolled_students:
                print("  No students are currently enrolled in this course.")
            else:
                print("  Enrolled Students:")
                for student in course.enrolled_students:
                    print(f"  - {student.name} (ID: {student.student_id})")

    def view_courses_taught(self, instructor):
        """Return a list of course names taught by this instructor."""
        instructor_courses = [course for course in self.platform_admin.courses if course.instructor.instructor_id == instructor.instructor_id]
        
        for course in instructor_courses:
            print(f"\nCourse: {course.course_name} (Code: {course.course_code})")    
            if not instructor_courses:
                print("You are not teaching any courses.")
                return
            
    def view_discussion_threads(self, creator):
        print("\nAvailable Discussion Threads:")

    # Check if the user is a student or instructor and display courses accordingly
        if isinstance(creator, Student):
            courses_to_display = creator.enrolled_courses
        elif isinstance(creator, Instructor):
            courses_to_display = creator._courses_taught  # Instructor teaches courses
        else:
            print("Invalid user type.")
            return
    
    # Display discussion threads for the courses
        for course in courses_to_display:
            print(f"\nCourse: {course.course_name}")
            for thread in course.discussion_threads:
                thread.display_thread()

    # Option to add a post to a discussion thread
        add_post_choice = input("\nDo you want to add a post? (yes/no): ")
        if add_post_choice.lower() == "yes":
            self.add_post_to_thread(creator)


    def add_post_to_thread(self, creator):
        """Allow user to add a post to a discussion thread."""
        course_name = input("Enter the course name for the thread you want to post in: ")
        course = next((c for c in creator.course if c.course_name().strip().lower() == course_name.lower()), None)

        if not course:
            print("Course not found.")
            return

        thread_title = input("Enter the title of the thread you want to post in: ")
        thread = next((t for t in course.discussion_threads if t.title.strip().lower() == thread_title), None)

        if not thread:
            print("Discussion thread not found.")
            return

        message = input("Enter your message: ")
        thread.add_post(creator, message)
        print("Post added successfully!")


    def create_announcement(self, title, content, date, recipient_groups):
        try:
            announcement = Announcement(title, content, date, recipient_groups)
            self.announcements.append(announcement)
            print("Announcement created.")
        except Exception as e:
            print(f"Error creating announcement: {e}")


    def view_announcements(self, user):
        """Method to view announcements for the given user."""
        print("\nAnnouncements:")
        for announcement in self.announcements:
            if user.role in announcement.recipient_groups:  # Assuming user has a role attribute
                print(f"- {announcement.title} ({announcement.date}): {announcement.content}")
        if not any(user.role in announcement.recipient_groups for announcement in self.announcements):
            print("No announcements available.")

    def admin_menu(self):
        """Display the admin menu options."""
        print("Admin Menu:")
        print("1. View Users")
        print("2. Create Announcement")
        print("3. Log Out")

        choice = input("Select an option: ")
        if choice == "1":
            self.view_users()
        elif choice == "2":
            self.create_announcements()
        elif choice == "3":
            self.log_out()
        else:
            print("Invalid choice, please try again.")

    def view_users(self):
        """Logic to view users."""
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                try:
                    data = json.load(file)

                    students = data.get("students", [])
                    instructors = data.get("instructors", [])

                    print("Displaying Users:")
                    print("\nStudents:")
                    if students:
                        for student in students:
                            print(f"Email: {student['email']}, Name: {student['name']}")
                    else:
                        print("No students found.")

                    print("\nInstructors:")
                    if instructors:
                        for instructor in instructors:
                            print(f"Email: {instructor['email']}, Name: {instructor['name']}")
                    else:
                        print("No instructors found.")

                except json.JSONDecodeError:
                    print("Error: Could not decode JSON data.")
        else:
            print("No data file found.")

    def create_announcements(self, title: str, content: str, date: str, recipient_groups: List[str]):
        try:
            announcement_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print("Error: Date format must be YYYY-MM-DD.")
            return

        announcement = Announcement(title=title, content=content, date=announcement_date, recipient_groups=recipient_groups)
        self.create_announcement(announcement)
        print("Announcement created successfully.")

    def log_out(self):
        """Logic to log out."""
        print("Logging out...")
        self.current_admin = None
