from assignment import Assignment  # Ensure Assignment class is defined and imported
from person import Person  # Ensure Person class is defined and imported

# Ensure Instructor class is properly defined, inherits from Person class
class Instructor(Person):
    def __init__(self, name: str, email: str, contact_number: str, address: str, instructor_id: str, role="Instructor"):
        # Initialize the Person class
        super().__init__(name, email, contact_number, address)
        self.__instructor_id = instructor_id  # Private attribute for instructor ID
        self.role = role  # Role of the instructor
        self._courses_taught = []  # List to store courses taught by the instructor
        self._assignments = []  # List to store assignments assigned by the instructor
        self.course = []


    @property
    def instructor_id(self) -> str:
        return self.__instructor_id

    @property
    def courses_taught(self) -> list:
        return self._courses_taught

    @property
    def assignments(self) -> list:
        return self._assignments

    def to_dict(self) -> dict:
        """Convert instructor details to a dictionary."""
        return {
            'instructor_id': self.instructor_id,
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number,  # Using getter
            'address': self.address,  # Using getter
            'role': self.role,
            'courses_taught': [course.course_code for course in self._courses_taught],  # Course codes for taught courses
        }

    def teach_course(self, course) -> None:
        """Add a course to the list of courses taught by the instructor."""
        if course not in self._courses_taught:  # Avoid duplicates
            self._courses_taught.append(course)
            print(f"Course '{course.course_name}' added to instructor '{self.name}'.")
        else:
            print(f"Instructor '{self.name}' is already teaching the course '{course.course_name}'.")

    def assign_assignment(self, assignment: Assignment) -> None:
        """Assign an assignment to a course taught by the instructor."""
        if assignment.course not in self._courses_taught:
            print(f"Cannot assign '{assignment.title}' to instructor '{self.name}': course not taught by instructor.")
        else:
            if assignment not in self._assignments:  # Avoid duplicates
                self._assignments.append(assignment)
                print(f"Assignment '{assignment.title}' assigned to instructor '{self.name}'.")
            else:
                print(f"Assignment '{assignment.title}' is already assigned.")

    def display_info(self) -> str:
        """Display detailed information about the instructor."""
        courses = ', '.join(course.course_name for course in self._courses_taught) if self._courses_taught else "No courses taught"
        return (f"ID: {self.instructor_id} \nInstructor: {self.name} \nRole: {self.role} "
                f"\nEmail: {self.email} \nContact#: {self.contact_number} \nAddress: {self.address} "
                f"\nCourses Taught: {courses}")