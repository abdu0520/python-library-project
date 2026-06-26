"""Custom exception classes for the library management system.

Defining our own exception types (instead of using generic ones) makes
the borrowing rules explicit and lets the menu layer report clear,
user-friendly messages.
"""


class LibraryError(Exception):
    """Base class for every error raised by the library system."""


class BookNotFoundError(LibraryError):
    """Raised when no book matches a given book_id."""


class MemberNotFoundError(LibraryError):
    """Raised when no member matches a given ID."""


class BookUnavailableError(LibraryError):
    """Raised when a member tries to borrow a book with no copies left."""


class BorrowLimitError(LibraryError):
    """Raised when a member has reached the maximum number of loans."""
