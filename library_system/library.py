"""The Library class ties books, members and loans together.

It enforces the borrowing rules and handles all CSV persistence, so the
rest of the program never touches files directly.
"""

import csv
import os

from models.book import Book
from models.member import Member
from models.loan import Loan
from exceptions import (
    LibraryError,
    BookNotFoundError,
    MemberNotFoundError,
    BookUnavailableError,
    BorrowLimitError,
)


class Library:
    """Coordinates the catalogue, the membership list and all loans."""

    def __init__(self, data_dir="data"):
        """Initialise an empty library backed by CSV files in data_dir."""
        self.data_dir = data_dir
        self.books = {}      #  book_id -> Book
        self.members = {}    # member_id -> Member
        self.loans = []      # list of Loan objects
        self._next_loan_id = 1

    # ---- catalogue and membership management -------------------------

    def add_book(self, book):
        """Add a book, merging copies if the book_id already exists."""
        if book.book_id in self.books:
            existing = self.books[book.book_id]
            existing.total_copies += book.total_copies
            existing.available_copies += book.total_copies
        else:
            self.books[book.book_id] = book

    def register_member(self, member):
        """Add a new member to the library."""
        self.members[member.member_id] = member

    def find_book(self, book_id):
        """Return the Book for an book_id or raise BookNotFoundError."""
        if book_id not in self.books:
            raise BookNotFoundError(f"No book found with book_id '{book_id}'.")
        return self.books[book_id]

    def find_member(self, member_id):
        """Return the Member for an ID or raise MemberNotFoundError."""
        if member_id not in self.members:
            raise MemberNotFoundError(
                f"No member found with ID '{member_id}'.")
        return self.members[member_id]

    # ---- core borrowing workflow -------------------------------------

    def borrow_book(self, member_id, book_id):
        """Lend one copy of a book to a member.

        Raises:
            MemberNotFoundError: if the member ID is unknown.
            BookNotFoundError: if the book_id is unknown.
            BorrowLimitError: if the member already holds the maximum.
            BookUnavailableError: if no copies are available.
        """
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if not member.can_borrow():
            raise BorrowLimitError(
                f"{member.name} already holds the maximum of "
                f"{Member.MAX_LOANS} books.")
        if not book.is_available():
            raise BookUnavailableError(
                f"No copies of '{book.title}' are available.")

        book.borrow_copy()
        member.add_loan(book_id)
        loan = Loan(str(self._next_loan_id), book_id, member_id)
        self._next_loan_id += 1
        self.loans.append(loan)
        return loan

    def return_book(self, member_id, book_id):
        """Return a borrowed copy and close the matching loan.

        Raises:
            MemberNotFoundError, BookNotFoundError, LibraryError
        """
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        loan = self._find_active_loan(member_id, book_id)
        if loan is None:
            raise LibraryError(
                f"{member.name} has no active loan for book_id '{book_id}'.")

        loan.mark_returned()
        book.return_copy()
        member.remove_loan(book_id)
        return loan

    def _find_active_loan(self, member_id, book_id):
        """Return the active Loan for this member and book, or None."""
        for loan in self.loans:
            if (loan.member_id == member_id and loan.book_id == book_id
                    and loan.is_active()):
                return loan
        return None

    # ---- reporting ---------------------------------------------------

    def list_books(self):
        """Return all books sorted by title."""
        return sorted(self.books.values(), key=lambda b: b.title.lower())

    def list_members(self):
        """Return all members sorted by name."""
        return sorted(self.members.values(), key=lambda m: m.name.lower())

    def overdue_loans(self):
        """Return every loan that is currently overdue."""
        return [loan for loan in self.loans if loan.is_overdue()]

    # ---- CSV persistence ---------------------------------------------

    def load_all(self):
        """Load books, members and loans from the CSV data files.

        Missing files are ignored, so the program also works on a fresh
        install with no data yet.
        """
        self._load_books()
        self._load_members()
        self._load_loans()

    def save_all(self):
        """Write books, members and loans back to their CSV files."""
        os.makedirs(self.data_dir, exist_ok=True)
        self._save_rows(
            "books.csv",
            ["book_id", "title", "author", "total_copies", "available_copies"],
            [b.to_row() for b in self.books.values()])
        self._save_rows(
            "members.csv",
            ["member_id", "name", "email", "borrowed"],
            [m.to_row() for m in self.members.values()])
        self._save_rows(
            "loans.csv",
            ["loan_id", "book_id", "member_id", "date_borrowed", "date_returned"],
            [loan.to_row() for loan in self.loans])

    def _path(self, filename):
        """Return the full path to a file inside the data directory."""
        return os.path.join(self.data_dir, filename)

    def _load_books(self):
        """Read books.csv into the catalogue, if the file exists."""
        path = self._path("books.csv")
        if not os.path.exists(path):
            return
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)  # skip the header row
            for row in reader:
                if row:
                    book = Book.from_row(row)
                    self.books[book.book_id] = book

    def _load_members(self):
        """Read members.csv into the membership list, if it exists."""
        path = self._path("members.csv")
        if not os.path.exists(path):
            return
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            for row in reader:
                if row:
                    member = Member.from_row(row)
                    self.members[member.member_id] = member

    def _load_loans(self):
        """Read loans.csv into the loan list, if it exists."""
        path = self._path("loans.csv")
        if not os.path.exists(path):
            return
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            max_id = 0
            for row in reader:
                if row:
                    loan = Loan.from_row(row)
                    self.loans.append(loan)
                    max_id = max(max_id, int(loan.loan_id))
            self._next_loan_id = max_id + 1

    def _save_rows(self, filename, header, rows):
        """Write a header plus rows to a CSV file in the data directory."""
        with open(self._path(filename), "w", newline="",
                  encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
