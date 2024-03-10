"""'This file contains classes and methods for managing an address book."""

from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import pickle


class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Mandatory field."""

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        super().__init__(value)


class Phone(Field):
    """Class for storing phone number. Has format validation (10 digits)."""

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    """Class for storing birthday date."""

    def __init__(self, value):
        super().__init__(value)


class Record:
    """Class for storing contact information, including name,
    phones, and birthday.
    """

    def __init__(self, record_name):
        self.name = Name(record_name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        """Method adds phone number, handles errors."""

        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
        except ValueError as e:
            print(e)

    def add_birthday(self, birthday):
        """Method adds birthday, handles errors."""

        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phone: {'; '.join(str(p) for p in self.phones)}, "
            f"birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    """Class for storing and managing records."""

    def add_record(self, new_record):
        """Method adds record, handles existing."""

        self.data[new_record.name.value] = new_record

    def find(self, target_name):
        """Method finds record by name, prints if absent."""

        if target_name in self.data:
            return self.data[target_name]
        else:
            print(f"Record for {target_name} not found")

    def get_birthdays_per_week(self):
        """Method that returns a list of birthdays for the next week."""

        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()

        for contact in self.data.values():
            name = contact.name.value
            birthday = contact.birthday
            if not birthday:
                continue

            birthday = birthday.value

            try:
                birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()
            except ValueError:
                print(f"Invalid birthday format for {name}. Skipping.")
                continue

            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days
            birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")

            if 0 <= delta_days < 7:
                if birthday_weekday in ["Saturday", "Sunday"]:
                    birthday_weekday = "Monday"
                birthdays_per_week[birthday_weekday].append(name)

        return birthdays_per_week

    def delete(self, name, phone):
        """Method deletes record by name and phone, prints if absent."""

        records_to_delete = [
            record
            for record in self.data.values()
            if record.name.value == name
            and any(p.value == phone for p in record.phones)
        ]

        if records_to_delete:
            for record in records_to_delete:
                del self.data[record.name.value]
                print(
                    f"Record for {record.name.value} "
                    f"with phone number {phone} deleted."
                )
        else:
            print(f"No record found for {name} with phone number {phone}.")

    def save_to_file(self, filename):
        """Method to save the address book to a file using pickle."""

        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    @classmethod
    def read_from_file(cls, filename):
        """Class method to read the address book from a file using pickle."""

        with open(filename, "rb") as f:
            data = pickle.load(f)
            address_book = cls()
            address_book.data = data
            return address_book

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
