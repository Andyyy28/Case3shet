import json
import os
from typing import List
import course
import instructor
import student
import schedule

class PlatformAdmin:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
        self.enrollments = []  # Handles enrollments
      

    @staticmethod
    def admin_login():
        """Authenticate admin user."""
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        try:
            if os.path.exists("data.json"):
                with open("data.json", "r") as file:
                    data = json.load(file)

                admins = data.get("admins", [])
                if any(admin["email"] == email and admin["password"] == password for admin in admins):
                    print("Login successful. Welcome, Admin!")
                    return True
                else:
                    print("Invalid email or password. Access denied.")
                    return False
            else:
                print("Error: data.json file not found.")
                return False

        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def load_data(self, filename='data.json'):
        """
        Load data from a JSON file and initialize the platform's entities.
        :param filename: Path to the JSON file.
        """
        try:
            if not os.path.exists(filename):
                print(f"File '{filename}' not found. Starting with empty data.")
                return

            with open(filename, 'r') as f:
                data = json.load(f)

            # Load instructors
            self.instructors = [
                instructor.Instructor(**inst_data)
                for inst_data in data.get('instructors', [])
            ]

            # Load courses
            self.courses = []
            for course_data in data.get('courses', []):
                instructor_id = course_data.get('instructor_id')
                instructor_obj = next((i for i in self.instructors if i.instructor_id == instructor_id), None)

                if not instructor_obj:
                    print(f"Warning: Instructor ID {instructor_id} not found for course '{course_data.get('course_name', 'Unknown')}'. Skipping.")
                    continue

                course_obj = course.Course(
                    course_data['course_name'],
                    course_data['course_code'],
                    instructor_obj,
                    course_data['units']
                )
                self.courses.append(course_obj)

            # Load students
            self.students = [
                student.Student.from_dict(student_data, self.courses)
                for student_data in data.get('students', [])
            ]

            # Load enrollments
            self.enrollments = []
            for enrollment_data in data.get('enrollments', []):
                student_obj = next((s for s in self.students if s.student_id == enrollment_data['student_id']), None)
                course_obj = next((c for c in self.courses if c.course_code == enrollment_data['course_code']), None)

                if student_obj and course_obj:
                    student_obj.enroll(course_obj)
                    course_obj.enrolled_students.append(student_obj)
                else:
                    if not student_obj:
                        print(f"Warning: Student ID {enrollment_data['student_id']} not found.")
                    if not course_obj:
                        print(f"Warning: Course code {enrollment_data['course_code']} not found.")

            # Load schedules
            schedules = data.get('schedules', [])
            for schedule_data in schedules:
                course_obj = next((c for c in self.courses if c.course_code == schedule_data['course_code']), None)
                if course_obj:
                    # Ensure to use the correct class name 'Schedule' instead of 'schedules'
                    schedule_obj = schedule.Schedule(course_obj, schedule_data['day'], schedule_data['time'])
                    course_obj.schedule = schedule_obj
                else:
                    print(f"Warning: Course code {schedule_data['course_code']} not found for schedule.")
            
        except json.JSONDecodeError:
            print("Error decoding JSON. Please ensure the file is formatted correctly.")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Ensure the file exists in the correct path.")
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")

    def save_data(self, filename='data.json'):
        """
        Save the current platform data to a JSON file.
        :param filename: Path to the JSON file.
        """
        try:
            data = {
                "students": [student.to_dict() for student in self.students],
                "instructors": [instructor.to_dict() for instructor in self.instructors],
                "courses": [course.to_dict() for course in self.courses],
                "enrollments": [
                    {"student_id": student.student_id, "course_code": course.course_code}
                    for student in self.students for course in student.enrolled_courses
                ],
                "schedules": [
                    {"course_code": course.course_code, "day": course.schedule.day, "time": course.schedule.time}
                    for course in self.courses if hasattr(course, 'schedule') and course.schedule
                ]
            }

            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Data successfully saved to {filename}.")

        except Exception as e:
            print(f"Error saving data: {e}")

   