import pickle
from typing import List, Tuple

from handlers.contacts import ContactsHandler
from models.address_book import AddressBook
from services.colorizer import Colorizer

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def load_data(filename="address_book.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Return empty address book if file not found
        return AddressBook()

def save_data(book, filename="address_book.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def main():
    # Initialize address book and contacts handler
    book = load_data()
    contacts_handler = ContactsHandler(book)

    print(Colorizer.highlight("Welcome to the assistant bot!"))
    while True:
        user_input = ""
        try:
            user_input = input(Colorizer.info("Enter a command: "))
        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            print(Colorizer.highlight("\nGood bye!"))
            save_data(book)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(Colorizer.highlight("Good bye!"))
            save_data(book)
            break
        elif command == "hello":
            print(Colorizer.highlight("How can I help you?"))
        elif command in ContactsHandler.get_available_commands():
            print(contacts_handler.handle(command, *args))
        else:
            print(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()