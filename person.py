from abc import ABC, abstractmethod


# Abstract Base Class for Person
class Person(ABC):
    def __init__(self, name: str, email: str, contact_number: str, address: str):
        self.__name = name
        self.__email = email
        self._contact_number = contact_number
        self._address = address
        self.courses = [] 

    @property
    def name(self) -> str:
        """Get or set the person's name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def email(self) -> str:
        """Get or set the person's email."""
        return self.__email

    @email.setter  # Corrected to email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        self.__email = value

    @property
    def contact_number(self) -> str:
        """Get or set the person's contact number."""
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value: str):
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Contact number must be at least 10 digits.")
        self._contact_number = value

    @property
    def address(self) -> str:
        """Get or set the person's address."""
        return self._address

    @address.setter
    def address(self, value: str):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        self._address = value

    @abstractmethod
    def display_info(self) -> str:
        """Abstract method to display information about the person."""
        pass