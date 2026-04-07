from enum import Enum


class Genre(Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    HISTORY = "History"


class Publication:
    def __init__(self, title, author, year, genre):
        if year > 2026 or year < 1450:
            raise ValueError("Некоректний рік видання")

        if not isinstance(genre, Genre):
            raise ValueError("Жанр повинен бути типу Genre")

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def get_info(self):
        return f"{self.title} - {self.author}, {self.year}, {self.genre.value}"

    def publication_type(self):
        return "Звичайне видання"

    def __lt__(self, other):
        return self.year < other.year


class Book(Publication):
    def __init__(self, title, author, year, genre, pages):
        super().__init__(title, author, year, genre)

        if pages <= 0:
            raise ValueError("Книга не може мати 0 або від'ємну кількість сторінок")

        self.pages = pages

    def publication_type(self):
        return f"Книга, {self.pages} сторінок"


class Magazine(Publication):
    def __init__(self, title, author, year, genre, issue_number):
        super().__init__(title, author, year, genre)

        if issue_number <= 0:
            raise ValueError("Номер випуску має бути більше 0")

        self.issue_number = issue_number

    def publication_type(self):
        return f"Журнал, випуск №{self.issue_number}"


class Library:
    def __init__(self):
        self.publications = []

    def add_publication(self, publication):
        if not isinstance(publication, Publication):
            raise TypeError("Можна додавати лише Publication")
        self.publications.append(publication)

    def show_all(self):
        for item in self.publications:
            print(item.get_info())
            print(item.publication_type())

    def sort_by_year(self):
        self.publications.sort()

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.publications):
            raise StopIteration

        batch = self.publications[self.index:self.index + 5]
        self.index += 5
        return batch


library = Library()

book1 = Book("Dune", "Frank Herbert", 1965, Genre.SCI_FI, 412)
book2 = Book("Harry Potter", "J.K. Rowling", 1997, Genre.FANTASY, 350)
mag1 = Magazine("Science Today", "Editorial Team", 2020, Genre.SCIENCE, 12)
book3 = Book("History of Europe", "John Smith", 2010, Genre.HISTORY, 500)
book4 = Book("Foundation", "Isaac Asimov", 1951, Genre.SCI_FI, 255)
book5 = Book("The Hobbit", "J.R.R. Tolkien", 1937, Genre.FANTASY, 310)
book6 = Book("Physics Monthly", "Editors", 2022, Genre.SCIENCE, 7)

library.add_publication(book1)
library.add_publication(book2)
library.add_publication(mag1)
library.add_publication(book3)
library.add_publication(book4)
library.add_publication(book5)
library.add_publication(book6)

print("=== Поліморфізм ===")
library.show_all()

print("\n=== Сортування за роком ===")
library.sort_by_year()
library.show_all()

print("\n=== Ітератор по 5 елементів ===")
for batch in library:
    print("Нова сторінка:")
    for item in batch:
        print(item.get_info())

print("\n=== Краш-тест ===")
try:
    bad_book = Book("Impossible Book", "Unknown", 3000, Genre.SCI_FI, -50)
except ValueError as e:
    print("Помилка:", e)