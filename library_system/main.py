"""Command-line entry point for the library management system.

Run with:  python main.py

This module presents a simple text menu so a librarian can add books,
register members, lend and return books, and view reports. All data is
loaded from CSV files in the 'data' directory at start-up and written
back when the user chooses to exit.
"""

from library import Library
from models.book import Book
from models.member import Member
from exceptions import LibraryError


def prompt(message):
    """Ask the user for input and strip surrounding whitespace."""
    return input(message).strip()


def add_book(library):
    """Collect book details from the user and add them to the library."""
    book_id = prompt("book_id: ")
    title = prompt("Title: ")
    author = prompt("Author: ")
    try:
        copies = int(prompt("Number of copies: "))
    except ValueError:
        print("That was not a valid whole number.\n")
        return
    if copies <= 0:
        print("Copies must be a positive number.\n")
        return
    library.add_book(Book(book_id, title, author, copies))
    print(f"Added '{title}'.\n")


def register_member(library):
    """Collect member details from the user and register them."""
    member_id = prompt("Member ID: ")
    name = prompt("Name: ")
    email = prompt("Email: ")
    library.register_member(Member(member_id, name, email))
    print(f"Registered {name}.\n")


def borrow_book(library):
    """Lend a book to a member, reporting any rule violations."""
    member_id = prompt("Member ID: ")
    book_id = prompt("book_id: ")
    try:
        loan = library.borrow_book(member_id, book_id)
        print(f"Done. Due back on {loan.due_date()}.\n")
    except LibraryError as error:
        print(f"Could not lend book: {error}\n")


def return_book(library):
    """Return a borrowed book, reporting any problems."""
    member_id = prompt("Member ID: ")
    book_id = prompt("Book book_id: ")
    try:
        library.return_book(member_id, book_id)
        print("Book returned. Thank you.\n")
    except LibraryError as error:
        print(f"Could not return book: {error}\n")


def list_books(library):
    """Print every book in the catalogue."""
    books = library.list_books()
    if not books:
        print("The catalogue is empty.\n")
        return
    print("\n-- Catalogue --")
    for book in books:
        print(book)
    print()


def list_members(library):
    """Print every registered member."""
    members = library.list_members()
    if not members:
        print("There are no members yet.\n")
        return
    print("\n-- Members --")
    for member in members:
        print(member)
    print()


def show_overdue(library):
    """Print every overdue loan."""
    overdue = library.overdue_loans()
    if not overdue:
        print("No overdue loans.\n")
        return
    print("\n-- Overdue loans --")
    for loan in overdue:
        print(loan)
    print()


MENU = """\
==== Community Library ====
1. Add book
2. Register member
3. Borrow book
4. Return book
5. List books
6. List members
7. Show overdue loans
8. Save and exit
"""

# Map each menu choice to the function that handles it.
ACTIONS = {
    "1": add_book,
    "2": register_member,
    "3": borrow_book,
    "4": return_book,
    "5": list_books,
    "6": list_members,
    "7": show_overdue,
}


def main():
    """Load data, run the menu loop, then save on exit."""
    library = Library()
    library.load_all()
    print("Data loaded.\n")

    while True:
        print(MENU)
        choice = prompt("Choose an option (1-8): ")

        if choice == "8":
            library.save_all()
            print("Data saved. Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please pick a number from 1 to 8.\n")
            continue

        # A safety net so an unexpected error never crashes the menu.
        try:
            action(library)
        except Exception as error:
            print(f"Unexpected error: {error}\n")


if __name__ == "__main__":
    main()
