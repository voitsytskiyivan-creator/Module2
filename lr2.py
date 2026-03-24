from dataclasses import dataclass
from enum import Enum


class Genre(Enum):
    SCI_FI = "SCI_FI"
    FANTASY = "FANTASY"
    SCIENCE = "SCIENCE"
    HISTORY = "HISTORY"


@dataclass
class Publication:
    title: str
    author: str
    year: int
    genre: Genre

    def __lt__(self, other):
        return self.year < other.year


class Book(Publication):
    def __init__(self, title, author, year, genre, pages):
        super().__init__(title, author, year, genre)
        self._pages = pages

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Кількість сторінок повинна бути додатним числом")
        self._pages = value

    def __str__(self):
        return f"Book: {self.title}, {self.author}, {self.year}, {self.genre.name}, {self.pages} стор."


class Magazine(Publication):
    def __init__(self, title, author, year, genre, issue_number):
        super().__init__(title, author, year, genre)
        self._issue_number = issue_number

    @property
    def issue_number(self):
        return self._issue_number

    @issue_number.setter
    def issue_number(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номер випуску повинен бути додатним числом")
        self._issue_number = value

    def __str__(self):
        return f"Magazine: {self.title}, {self.author}, {self.year}, {self.genre.name}, випуск №{self.issue_number}"


class Library:
    def __init__(self):
        self._items = []

    def add_publication(self, publication):
        self._items.append(publication)

    def sort_by_year(self):
        self._items.sort()

    def __iter__(self):
        for i in range(0, len(self._items), 5):
            yield self._items[i:i+5]


if __name__ == "__main__":
    library = Library()

    try:
        title = input("Введіть назву книги: ")
        author = input("Введіть автора: ")
        year = int(input("Введіть рік видання: "))
        pages = int(input("Введіть кількість сторінок: "))

        if len(title.strip()) < 2:
            raise ValueError("Назва повинна містити мінімум 2 символи")

        if year < 0 or year > 2026:
            raise ValueError("Некоректний рік видання")

        book1 = Book(title, author, year, Genre.SCIENCE, pages)

        book2 = Book("Dune", "Frank Herbert", 1965, Genre.SCI_FI, 412)
        mag1 = Magazine("Science Today", "Editorial Team", 2023, Genre.SCIENCE, 12)

        library.add_publication(book1)
        library.add_publication(book2)
        library.add_publication(mag1)

        library.sort_by_year()

        print("\nКаталог бібліотеки:")
        for page in library:
            for item in page:
                print(item)
            print("--- Сторінка ---")

        print("\nВнутрішній стан об'єкта:")
        print(vars(book1))

    except ValueError as e:
        print("Помилка:", e)