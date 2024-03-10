"""This file contains CLI Bot functionality."""

from datetime import datetime
from address_book import Record


def input_error(func):
    """Decorator function for handling errors."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as error:
            print(f"A KeyError occurred: {error}")
            return None
        except ValueError:
            print(
                "Invalid number of arguments. Enter the 'help' "
                "command for additional information on the command."
            )
            return None

    return inner


def parse_input(user_input):
    """This function parses user-entered arguments and returns them."""

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def get_all(contacts):
    """This function returns all user data."""

    if len(contacts) == 0:
        print("Contacts not found. Please add a first contact.")
        return

    print("Contacts:")
    print(f"{'Name':<10} {'Phone':<15} {'Birthday':<15}")

    for name, record in contacts.items():
        phone_numbers = ", ".join(str(phone) for phone in record.phones)
        birthday = record.birthday.value if record.birthday else ""
        print(f"{name:<10} {phone_numbers:<15} {birthday:<15}")


@input_error
def add_contact(args, contacts):
    """This function adds a new user to the storage."""

    name, phone = args
    if len(phone) != 10 or not phone.isdigit():
        raise ValueError(
            "Invalid phone number. Phone number must consist of 10 digits."
        )
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    print("Contact added.")


@input_error
def change_contact(args, contacts):
    """This function changes the phone number of a contact."""

    name, new_phone = args
    contact = contacts.find(name)
    if not contact:
        print("Contact not found.")
        return

    if len(new_phone) != 10 or not new_phone.isdigit():
        print("Invalid phone number. Phone number must consist of 10 digits.")
        return

    contact.phones.clear()
    contact.add_phone(new_phone)
    print("Phone number updated.")


@input_error
def get_phone_contact(args, contacts):
    """This function returns the user's phone number."""
    print("args", args)
    (name,) = args
    user_name = name.capitalize()
    print("user_name", user_name)
    if user_name not in contacts:
        print("Contact not found.")
        return
    print(f"{user_name} phone: {contacts[user_name].phones[0].value}")


@input_error
def add_birthday(args, contacts):
    """This function adds a birthday to the contact."""

    name, birthday = args

    try:
        datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        print("Invalid birthday format. Please use DD.MM.YYYY format.")
        return

    record = contacts.data.get(name)
    if record:
        record.add_birthday(birthday)
        print("Birthday added.")
    else:
        print("Contact not found.")


@input_error
def change_birthday(args, contacts):
    """This function changes the birthday of a contact."""

    name, new_birthday = args
    contact = contacts.find(name)
    if not contact:
        print("Contact not found.")
        return

    try:
        datetime.strptime(new_birthday, "%d.%m.%Y")
    except ValueError:
        print("Invalid birthday format. Please use DD.MM.YYYY format.")
        return

    if contact.birthday:
        contact.birthday.value = new_birthday
    else:
        contact.add_birthday(new_birthday)
    print("Birthday updated.")


@input_error
def show_birthday(args, contacts):
    """This function shows the birthday of the contact."""

    (name,) = args
    record = contacts.data.get(name)
    if record and record.birthday:
        print(f"{name}'s birthday: {record.birthday}")
    elif record:
        print(f"{name} has no birthday recorded.")
    else:
        print("Contact not found.")


@input_error
def birthdays(contacts):
    """This function shows birthdays for the next week."""

    birthdays_per_week = contacts.get_birthdays_per_week()
    desired_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    sorted_birthdays_per_week = dict(
        sorted(
            birthdays_per_week.items(),
            key=lambda item: (
                desired_order.index(item[0])
                if item[0] in desired_order
                else len(desired_order)
            ),
        )
    )

    if sorted_birthdays_per_week:
        print("Birthdays for the next week:")
        for weekday, names in sorted_birthdays_per_week.items():
            names_str = ", ".join(names)
            print(f"{weekday}: {names_str}")
    else:
        print("No birthdays for the next week.")


@input_error
def delete_contact(args, contacts):
    """This function deletes a user from the storage."""

    name, phone = args
    contacts.delete(name, phone)


def help_message():
    """Bot command assistant function"""

    help_text = """
        >>> BOT COMMAND HELPER:

        hello (It is customary to say hello as a rule of good manners)
        add (Add a new user. Arguments: user_name phone_number)
        change (Change user phone. Arguments: user_name phone_number)
        phone (Display user phone. Argument: user_name)
        all (Display all users info)
        add-birthday (Add birthday. Arguments: user_name DD.MM.YYYY)
        change-birthday (Change user birthday. Arguments: user_name DD.MM.YYYY)
        show-birthday (Display birthday of a contact. Arguments: user_name)
        birthdays (Display birthdays for the next week)
        delete (Delete user. Arguments: user_name phone_number)
        exit, close OR bye (Finishes the work of the bot)

        >>> GOOD LUCK!
        """
    print(help_text)


def get_command_handlers():
    """Return a dictionary mapping commands to their corresponding handlers."""

    return {
        "all": get_all,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone_contact,
        "add-birthday": add_birthday,
        "change-birthday": change_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "delete": delete_contact,
        "help": help_message,
    }
