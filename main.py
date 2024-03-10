"""This module implements functionality for a CLI Bot."""

from address_book import AddressBook
from bot_functionality import parse_input, get_command_handlers


def main():
    """Primary function for interacting with the user via the command line."""

    filename = "address_book.pkl"
    try:
        contacts = AddressBook.read_from_file(filename)
    except FileNotFoundError:
        contacts = AddressBook()

    welcome = """
                    !!! Welcome to the assistant bot !!!

        Enter the 'help' command for additional information on the command.
        """
    print(welcome)

    command_handlers = get_command_handlers()

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["all", "birthdays"]:
            command_handlers[command](contacts)
        elif command == "help":
            command_handlers["help"]()
        elif command in command_handlers:
            command_handlers[command](args, contacts)
        elif command == "hello":
            print("Hi! How can I help you?")
        elif command in ["close", "exit", "bye"]:
            contacts.save_to_file(filename)
            print("Goodbye!")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
