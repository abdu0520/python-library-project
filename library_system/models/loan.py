"""Defines the Loan class used by the library system."""

from datetime import date, timedelta


class Loan:
    """Represents a single borrowing transaction.

    A Loan links a member to a book for a fixed loan period and records
    whether (and when) the book was returned.
    """

    LOAN_DAYS = 14

    def __init__(self, loan_id, book_id, member_id,
                 date_borrowed=None, date_returned=""):
        """Initialise a Loan.

        Args:
            loan_id: Unique identifier for the loan.
            book_id: book_id of the borrowed book.
            member_id: ID of the borrowing member.
            date_borrowed: ISO date string; defaults to today.
            date_returned: ISO date string, or "" while still on loan.
        """
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.date_borrowed = date_borrowed or date.today().isoformat()
        self.date_returned = date_returned

    def due_date(self):
        """Return the date the book is due back as an ISO string."""
        borrowed = date.fromisoformat(self.date_borrowed)
        return (borrowed + timedelta(days=self.LOAN_DAYS)).isoformat()

    def is_active(self):
        """Return True if the book has not yet been returned."""
        return self.date_returned == ""

    def is_overdue(self):
        """Return True if the loan is active and past its due date."""
        if not self.is_active():
            return False
        return date.today() > date.fromisoformat(self.due_date())

    def mark_returned(self):
        """Record today's date as the return date."""
        self.date_returned = date.today().isoformat()

    def to_row(self):
        """Convert this loan into a list of strings for CSV writing."""
        return [self.loan_id, self.book_id, self.member_id,
                self.date_borrowed, self.date_returned]

    @classmethod
    def from_row(cls, row):
        """Build a Loan from a CSV row (a list of strings)."""
        loan_id, book_id, member_id, borrowed, returned = row
        return cls(loan_id, book_id, member_id, borrowed, returned)

    def __str__(self):
        """Return a human-readable summary of the loan."""
        if not self.is_active():
            status = "returned"
        elif self.is_overdue():
            status = "OVERDUE"
        else:
            status = "on loan"
        return (f"Loan {self.loan_id}: book {self.book_id} -> "
                f"member {self.member_id} ({status}, due {self.due_date()})")
