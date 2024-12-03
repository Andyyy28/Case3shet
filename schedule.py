from course import Course

class Schedule:
    def __init__(self, course: Course, day: str, time: str):
        """
        Initialize a schedule entry.
        :param course: A Course object associated with the schedule.
        :param day: The day of the week (e.g., "Monday").
        :param time: The time of the class (e.g., "09:00 AM - 11:00 AM").
        """
        self.__course = course
        self.__day = day
        self.__time = time

    @property
    def course(self) -> Course:
        """Return the associated course."""
        return self.__course

    @property
    def day(self) -> str:
        """Return the day of the schedule."""
        return self.__day

    @property
    def time(self) -> str:
        """Return the time of the schedule."""
        return self.__time

    def to_dict(self) -> dict:
        """
        Convert the schedule to a dictionary format.
        :return: A dictionary representing the schedule.
        """
        return {
            "course": self.course.course_code,  # Assuming Course has a unique course_code
            "day": self.day,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, data: dict, all_courses: list[Course]):
        """
        Create a Schedule object from a dictionary.
        :param data: A dictionary containing schedule details.
        :param all_courses: A list of available Course objects to match the course_code.
        :return: A Schedule object.
        """
        # Look up the course based on the course_code from the list of all courses
        course = next((c for c in all_courses if c.course_code == data["course"]), None)
        if not course:
            raise ValueError(f"Course with code {data['course']} not found.")
        # Return the newly created Schedule object
        return cls(course, data["day"], data["time"])

    def display_schedule(self) -> str:
        """
        Display the schedule details in a formatted string.
        :return: A string with course name, day, and time.
        """
        return f"Course: {self.course.course_name} (Code: {self.course.course_code}), Day: {self.day}, Time: {self.time}"

    def __repr__(self) -> str:
        """
        Provide a string representation for the Schedule object.
        :return: A formatted string representing the schedule.
        """
        return f"<Schedule(course={self.course.course_name}, day={self.day}, time={self.time})>"