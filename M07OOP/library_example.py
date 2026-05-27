class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_checked_out = False

    def checkout(self):
        if self.is_checked_out:
            print(f"'{self.title}' is already checked out.")
        else:
            self.is_checked_out = True
            print(f"Checked out: '{self.title}'")

    def return_book(self):
        self.is_checked_out = False
        print(f"Returned: '{self.title}'")

    def __str__(self):
        status = "OUT" if self.is_checked_out else "IN "
        return f"[{status}] {self.title} — {self.author} ({self.year})"


class EBook(Book):
    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb

    def __str__(self):
        return f"{super().__str__()} [{self.file_size_mb} MB]"


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added: '{book.title}'")

    def show_all(self):
        print(f"\n=== {self.name} ===")
        if not self.books:
            print("  No books.")
            return
        for book in self.books:
            print(f"  {book}")

    def search(self, keyword):
        keyword = keyword.lower()
        return [
            b for b in self.books
            if keyword in b.title.lower() or keyword in b.author.lower()
        ]


if __name__ == "__main__":
    lib = Library("City Library")

    lib.add_book(Book("Clean Code", "Robert C. Martin", 2008))
    lib.add_book(Book("The Pragmatic Programmer", "Hunt & Thomas", 1999))
    lib.add_book(Book("Python Crash Course", "Eric Matthes", 2023))
    lib.add_book(EBook("Automate the Boring Stuff", "Al Sweigart", 2019, 3.2))

    lib.show_all()

    lib.books[0].checkout()
    lib.books[0].checkout()
    lib.show_all()

    lib.books[0].return_book()

    results = lib.search("python")
    print(f"\nSearch 'python': {len(results)} result(s)")
    for b in results:
        print(f"  {b}")
