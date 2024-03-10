# goitneo-python-hw-3-group-2
hw-3

## Homework #3:

### CLI Bot endpoint - main.py
This module implements functionality for a CLI Bot. It provides a command-line interface for interacting with the user. The main function main() initializes the address book, loads it from a file if it exists, or creates a new one, then starts a loop for accepting commands. Commands are handled using command handlers defined in the bot_functionality module.

### CLI Bot  functionality - functionality.py
This file contains CLI Bot functionality. It includes functions for handling user input, managing contacts in an address book, and providing command-line interface commands. Key functions include adding, changing, and deleting contacts, managing birthdays, displaying contact information, and providing help messages. Additionally, the file defines a decorator function for error handling and a function to get command handlers for different bot commands.

### Address book - address_book.py
This file contains classes and methods for managing an address book. It includes classes for storing contact information such as name, phone numbers, and birthday, along with methods for adding, finding, and deleting records. Additionally, the file provides functionality for saving and loading address book data to and from a file using pickle. The AddressBook class extends UserDict to manage records efficiently, and it includes methods for retrieving birthdays for the next week.

### Address book DB - address_book.pkl
This is a pickle file used to store the data of the address book. It serves as a persistent storage mechanism for the address book records, allowing the data to be saved and loaded between different sessions of the CLI Bot. The file stores the serialized data of the address book dictionary using the pickle module, enabling efficient data storage and retrieval.

Note: This file is created after the first successful exit from the bot using the commands: exit, close, bye.