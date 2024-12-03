from person import Person

class Student(Person):
    def __init__(self, name, email, contact_number, address, student_id, year_level, program, gpa=0.0, birth_date=None, enrolled_courses=None, role="Student"):
        super().__init__(name, email, contact_number, address)
        self.__student_id = student_id
        self.__year_level = year_level
        self.__program = program
        self.__gpa = gpa
        self.__birth_date = birth_date
        self.role = role
        self.__enrolled_courses = enrolled_courses if enrolled_courses is not None else []
        self.course = []

    def to_dict(self):
        """Convert the Student object to a dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number,  # Use the getter method
            'address': self.address,  # Use the getter method
            'student_id': self.student_id,
            'year_level': self.year_level,
            'program': self.program,
            'gpa': self.gpa,
            'birth_date': self.birthdate,  # Use the getter method
            'enrolled_courses': [course.to_dict() for course in self.enrolled_courses]  # Assumes Course has a to_dict method
        }

    @classmethod
    def from_dict(cls, data, all_courses):
        """
        Create a Student object from a dictionary.
        :param data: A dictionary containing student details.
        :param all_courses: A list of Course objects to map enrolled courses.
        :return: A Student object.
        """
        student = cls(
            data['name'],
            data['email'],
            data['contact_number'],
            data['address'],
            data['student_id'],
            data['year_level'],
            data['program'],
            gpa=data.get('gpa', 0.0),
            birth_date=data.get('birth_date')
        )
        # Map enrolled_courses to actual Course objects
        for course_data in data.get('enrolled_courses', []):
            course = next((c for c in all_courses if c.course_code == course_data['course_code']), None)
            if course:
                student.enroll(course)

        return student

    @property
    def student_id(self):
        return self.__student_id

    @property
    def year_level(self):
        return self.__year_level

    @property
    def program(self):
        return self.__program

    @property
    def birthdate(self):
        return self.__birth_date

    @birthdate.setter
    def birthdate(self, value):
        self.__birth_date = value

    @property
    def enrolled_courses(self):
        return self.__enrolled_courses

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if 0 <= value <= 4.0:
            self.__gpa = value
        else:
            raise ValueError("GPA must be between 0 and 4.0")

    def enroll(self, course):
        """
        Enroll the student in a course.
        :param course: A Course object to enroll in.
        """
        if course not in self.__enrolled_courses:  # Avoid duplicates
            self.__enrolled_courses.append(course)

    def display_info(self):
        """
        Display basic student information.
        :return: A formatted string with student details.
        """
        return (
            f"ID: {self.student_id}\n"
            f"Student: {self.name}\n"
            f"Year Level: {self.year_level}\n"
            f"Program: {self.program}\n"
            f"Email: {self.email}\n"
            f"Contact#: {self.contact_number}\n"
            f"Address: {self.address}"
        )