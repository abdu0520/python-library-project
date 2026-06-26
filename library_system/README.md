Community Library Management System:

A small command line application for managing a community library:
adding books, registering members, lending and returning books, and
viewing reports such as overdue loans. 

Purpose

The system helps a librarian keep track of three things:

- the **catalogue** of books and how many copies of each are available,
- the **members** who are allowed to borrow, and
- the **loans** that link a member to a book, with a due date.


Installation and Execution:

Requires **Python 3.8+** (uses only the standard library — no packages
to install).

run the program:
python main.py

Example Usage


 Community Library :
1. Add book
2. Register member
3. Borrow book
4. Return book
5. List books
6. List members
7. Show overdue loans
8. Save and exit

Choose an option (1-8): 3
Member ID: M002
book_id : 9780140328721
Done. Due back on 2026-07-09.


If a rule is broken the program explains why instead of crashing:
Choose an option (1-8): 3
Member ID: 2
Book_id : 1
Could not lend book: No copies of 'python proj1' are available.


Key Features:

- Add books (merging copies when a book_id already exists)
- Register members, each limited to 3 simultaneous loans
- Borrow / return books with automatic due-date tracking (14-day period)
- Overdue-loan report
- Automatic CSV save/load — data survives between sessions
- Clear, custom error messages for every rule violation

Project Structure:

| File / folder        | Responsibility                                        |
|----------------------|-------------------------------------------------------|
| `main.py`            | Menu-driven user interface (program entry point)      |
| `library.py`         | `Library` class: rules + CSV save/load                |
| `models/book.py`     | `Book` class                                          |
| `models/member.py`   | `Member` class                                        |
| `models/loan.py`     | `Loan` class                                          |
| `exceptions.py`      | Custom exception types                                |
| `data/*.csv`         | Sample data (books, members, loans)                   |
