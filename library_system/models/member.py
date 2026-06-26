"""Defines the Member class used by the library system."""


class Member:
    """Represents a library member who can borrow books.

    Each member may hold at most ``MAX_LOANS`` books at any one time.
    """

    MAX_LOANS = 3

    def __init__(self, member_id, name, email, borrowed=None):
        """Initialise a Member.

        Args:
            member_id: Unique identifier for the member.
            name: Member's full name.
            email: Member's contact email.
            borrowed: List of book_ids the member currently holds. Defaults
                to an empty list.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed = borrowed if borrowed is not None else []

    def can_borrow(self):
        """Return True if the member is below the loan limit."""
        return len(self.borrowed) < self.MAX_LOANS

    def add_loan(self, book_id):
        """Record that the member has borrowed the given book_id."""
        self.borrowed.append(book_id)

    def remove_loan(self, book_id):
        """Remove a returned book_id from the member's record."""
        if book_id in self.borrowed:
            self.borrowed.remove(book_id)

    def to_row(self):
        """Convert this member into a list of strings for CSV writing."""
        # The book_id list is joined with ';' so it fits in a single cell.
        return [self.member_id, self.name, self.email,
                ";".join(self.borrowed)]

    @classmethod
    def from_row(cls, row):
        """Build a Member from a CSV row (a list of strings)."""
        member_id, name, email, borrowed = row
        borrowed_list = borrowed.split(";") if borrowed else []
        return cls(member_id, name, email, borrowed_list)

    def __str__(self):
        """Return a human-readable summary of the member."""
        return (f"[{self.member_id}] {self.name} <{self.email}> "
                f"- {len(self.borrowed)} book(s) on loan")
