"""Defines the Book class used by the library system."""


class Book:
    """Represents a single title in the library catalogue.

    A Book tracks how many copies the library owns in total and how many
    of those copies are currently on the shelf available to borrow.
    """

    def __init__(self, book_id, title, author, total_copies,
                 available_copies=None):
        """Initialise a Book.

        Args:
            book_id: Unique identifier for the title.
            title: The book's title.
            author: The book's author.
            total_copies: Number of copies the library owns.
            available_copies: Copies currently available. Defaults to
                total_copies for a brand-new book.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = int(total_copies)
        if available_copies is None:
            self.available_copies = self.total_copies
        else:
            self.available_copies = int(available_copies)

    def is_available(self):
        """Return True if at least one copy can be borrowed."""
        return self.available_copies > 0

    def borrow_copy(self):
        """Take one copy off the shelf.

        Returns:
            True if a copy was available and taken, otherwise False.
        """
        if self.is_available():
            self.available_copies -= 1
            return True
        return False

    def return_copy(self):
        """Put one copy back on the shelf (never exceeding the total)."""
        if self.available_copies < self.total_copies:
            self.available_copies += 1

    def to_row(self):
        """Convert this book into a list of strings for CSV writing."""
        return [self.book_id, self.title, self.author,
                str(self.total_copies), str(self.available_copies)]

    @classmethod
    def from_row(cls, row):
        """Build a Book from a CSV row (a list of strings)."""
        book_id, title, author, total, available = row
        return cls(book_id, title, author, total, available)

    def __str__(self):
        """Return a human-readable summary of the book."""
        return (f"[{self.book_id}] {self.title} by {self.author} "
                f"({self.available_copies}/{self.total_copies} available)")
