from enum import Enum
import time
import pickle
import csv
import json
import os

# ENUM
class Genre(Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    HISTORY = "History"

# BASE CLASS
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
        if not isinstance(other, Publication):
            return NotImplemented

        return self.year < other.year

    def __add__(self, other):

        if isinstance(other, Publication):
            return abs(self.year - other.year)

        elif isinstance(other, int):
            return Publication(
                self.title,
                self.author,
                self.year + other,
                self.genre
            )

        raise TypeError("Непідтримуваний тип")

    def __str__(self):
        return self.get_info()

# BOOK
class Book(Publication):
    def __init__(
            self,
            title,
            author,
            year,
            genre,
            pages):

        super().__init__(
            title,
            author,
            year,
            genre
        )

        if pages <= 0:
            raise ValueError(
                "Кількість сторінок повинна бути > 0"
            )

        self.pages = pages

    def publication_type(self):
        return f"Книга, {self.pages} сторінок"

# MAGAZINE
class Magazine(Publication):
    def __init__(
            self,
            title,
            author,
            year,
            genre,
            issue_number):

        super().__init__(
            title,
            author,
            year,
            genre
        )

        if issue_number <= 0:
            raise ValueError(
                "Номер випуску повинен бути > 0"
            )

        self.issue_number = issue_number

    def publication_type(self):
        return f"Журнал, випуск №{self.issue_number}"

# FUNCTOR
class PublicationValidator:

    def __init__(self):
        self.calls_count = 0
        self.duplicates = []

    def __call__(self, library, publication):

        self.calls_count += 1

        for item in library.publications:

            if item.title.lower() == publication.title.lower():

                self.duplicates.append(
                    publication.title
                )

                return False

        return True

    def get_statistics(self):
        return {
            "calls_count": self.calls_count,
            "duplicates": self.duplicates
        }

# CUSTOM ITERATOR
class GenreIterator:

    def __init__(self, publications, genre):

        self.filtered = [
            pub for pub in publications
            if pub.genre == genre
        ]

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.filtered):
            raise StopIteration

        item = self.filtered[self.index]

        self.index += 1

        return item

# CONTEXT MANAGER
class LibraryContext:

    def __init__(self, library, timeout=3):

        self.library = library
        self.timeout = timeout
        self.status = "Active"

    def __enter__(self):

        self.start_time = time.time()

        print("Вхід у бібліотеку")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        elapsed = time.time() - self.start_time

        if elapsed > self.timeout:
            self.status = "Expired"

        print(
            f"Вихід з бібліотеки. Статус: {self.status}"
        )

# LIBRARY
class Library:

    def __init__(self):

        self.publications = []
        self.validator = PublicationValidator()

        self.company_name = "My Library"
        self.page_size = 5

    # JSON
    def load_config(self, filename):

        with open(
                filename,
                "r",
                encoding="utf-8") as file:

            config = json.load(file)

        self.company_name = config.get(
            "company_name",
            "My Library"
        )

        self.page_size = config.get(
            "page_size",
            5
        )

        print("Конфігурацію завантажено")

    # Додавання
    def add_publication(self, publication):

        if not isinstance(
                publication,
                Publication):

            raise TypeError(
                "Можна додавати тільки Publication"
            )

        if self.validator(self, publication):

            self.publications.append(
                publication
            )

            print(
                f"Додано: {publication.title}"
            )

        else:

            print(
                f"Видання '{publication.title}' вже існує"
            )

    # Виведення
    def show_all(self):

        for item in self.publications:

            print(item.get_info())
            print(item.publication_type())

    # Сортування
    def sort_by_year(self):
        self.publications.sort()

    # Ітератор
    def get_by_genre(self, genre):
        return GenreIterator(
            self.publications,
            genre
        )

    # Генератор по 5 записів
    def paginate(self):

        for i in range(
                0,
                len(self.publications),
                self.page_size):

            yield self.publications[
                  i:i + self.page_size
                  ]

    # PICKLE SAVE
    def save_pickle(self, filename):

        with open(filename, "wb") as file:
            pickle.dump(self, file)

        print(
            f"Бекап збережено у {filename}"
        )

    # PICKLE LOAD
    @staticmethod
    def load_pickle(filename):

        with open(filename, "rb") as file:
            library = pickle.load(file)

        print(
            f"Бекап завантажено з {filename}"
        )

        return library

    # CSV EXPORT
    def export_csv(self, filename):

        with open(
                filename,
                "w",
                newline="",
                encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Title",
                "Author",
                "Year",
                "Genre",
                "Type"
            ])

            for pub in self.publications:

                writer.writerow([
                    pub.title,
                    pub.author,
                    pub.year,
                    pub.genre.value,
                    pub.publication_type()
                ])

        print(
            f"CSV звіт створено: {filename}"
        )

# MAIN
if __name__ == "__main__":
    library = Library()

    # JSON конфігурація
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config.json"
    )

    library.load_config(config_path)

    book1 = Book(
        "Dune",
        "Frank Herbert",
        1965,
        Genre.SCI_FI,
        412
    )

    book2 = Book(
        "Harry Potter",
        "J.K. Rowling",
        1997,
        Genre.FANTASY,
        350
    )

    mag1 = Magazine(
        "Science Today",
        "Editorial Team",
        2020,
        Genre.SCIENCE,
        12
    )

    book3 = Book(
        "History of Europe",
        "John Smith",
        2010,
        Genre.HISTORY,
        500
    )

    book4 = Book(
        "Foundation",
        "Isaac Asimov",
        1951,
        Genre.SCI_FI,
        255
    )

    book5 = Book(
        "The Hobbit",
        "J.R.R. Tolkien",
        1937,
        Genre.FANTASY,
        310
    )

    book6 = Magazine(
        "Physics Monthly",
        "Editors",
        2022,
        Genre.SCIENCE,
        7
    )

    library.add_publication(book1)
    library.add_publication(book2)
    library.add_publication(mag1)
    library.add_publication(book3)
    library.add_publication(book4)
    library.add_publication(book5)
    library.add_publication(book6)

    duplicate = Book(
        "Dune",
        "Frank Herbert",
        1965,
        Genre.SCI_FI,
        412
    )

    library.add_publication(duplicate)

    print("\n=== Оператор + ===")
    print("Різниця років:", book1 + book2)

    new_book = book1 + 5
    print(new_book.get_info())

    print("\n=== SCI_FI ===")

    for item in library.get_by_genre(
            Genre.SCI_FI):
        print(item.get_info())

    print("\n=== Пагінація ===")

    for page_num, page in enumerate(
            library.paginate(),
            start=1):

        print(f"\nСторінка {page_num}")

        for item in page:
            print(item.get_info())

    print("\n=== CSV ===")
    library.export_csv(
        "library_report.csv"
    )

    print("\n=== PICKLE ===")
    library.save_pickle(
        "library_backup.pkl"
    )

    restored = Library.load_pickle(
        "library_backup.pkl"
    )

    print("\n=== Відновлена бібліотека ===")
    restored.show_all()

    print("\n=== Статистика функтора ===")

    stats = library.validator.get_statistics()

    print(
        "Кількість викликів:",
        stats["calls_count"]
    )

    print(
        "Дублікати:",
        stats["duplicates"]
    )

    print("\n=== Контекстний менеджер ===")

    with LibraryContext(
            library,
            timeout=2):

        time.sleep(3)

    print("\n=== Краш-тест ===")

    try:

        bad_book = Book(
            "Impossible Book",
            "Unknown",
            3000,
            Genre.SCI_FI,
            -50
        )

    except ValueError as e:

        print("Помилка:", e)