from typing import Dict
from collections import UserDict
from datetime import datetime, timedelta
from models.exceptions import PhoneValueError, BirthdayValueError

class Field:
    def __init__(self, value: str):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)
    
class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self._value 
    
    @value.setter
    def value(self, value: str):
        if not value.isdigit():
            raise PhoneValueError("Phone number must contain only digits")
        
        if len(value) != 10:
            raise PhoneValueError("Phone number must contain 10 digits")
        
        self._value = value

class Birthday(Field):
    format = '%d.%m.%Y'

    def __str__(self):
        return self.value.strftime(Birthday.format)

    @property
    def value(self):
        return self._value 
    
    @value.setter
    def value(self, value: str):
        try:
            date = datetime.strptime(value, Birthday.format)
            self._value = date.date()
        except ValueError:
            raise BirthdayValueError("Invalid date format. Use DD.MM.YYYY")
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday or 'not specified'}"
    
    def add_phone(self, phone: str) -> None:
        """Add phone to record if it's valid, otherwise handle ValueError"""

        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit phone in record if it exists"""

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def remove_phone(self, phone: str) -> None:
        """Remove phone from record if it exists"""

        self.phones = [p for p in self.phones if p.value != phone]

    def find_phone(self, phone: str) -> Phone | None:
        """Find phone in record by value, return None if not found"""

        for p in self.phones:
            if p.value == phone:
                return p

        return None
    
    def add_birthday(self, birthday: str) -> None:
        """Add birthday to record if it's valid, otherwise handle ValueError"""

        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        """Add record to address book"""

        self.data[record.name.value] = record
    
    def delete(self, name: str) -> None:
        """Delete record from address book by name"""

        del self.data[name]
        
    def find(self, name: str) -> Record | None:
        """Find record in address book by name, return None if not found"""
        
        if name in self.data:
            return self.data[name]
        
        return None
    
    def get_upcoming_birthdays(self) -> Dict[str, datetime]:
        """Return dict of contacts with upcoming birthdays"""

        today = datetime.today().date()
        upcoming_birthdays = {}

        # Iterate through all users
        for record in self.data.values():
            if record.birthday is None:
                continue

            birthdate: Birthday = record.birthday.value
            name: str = record.name.value
            # Calculate this year's birthday
            birthdate_this_year = birthdate.replace(year=today.year)
            # If this year's birthday in past, calculate next year's birthday
            if birthdate_this_year < today:
                birthdate_this_year = birthdate.replace(year=today.year + 1)

            # Calculate days to birthday
            days_to_birthday = (birthdate_this_year - today).days

            # If days to birthday less than or equal to 7, calculate congratulation date
            if days_to_birthday <= 7:
                congratulation_date = birthdate_this_year
                # If congratulation date is weekend, calculate next week's date
                if birthdate_this_year.weekday() >= 5:
                    congratulation_date = birthdate_this_year + timedelta(days=7 - birthdate_this_year.weekday())
                # Add user to upcoming birthdays dict
                upcoming_birthdays[name] = congratulation_date

        return upcoming_birthdays