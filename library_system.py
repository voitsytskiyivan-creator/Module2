import pickle
import csv
import json
import os
from enum import Enum
from datetime import datetime


class Genre(Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    HISTORY = "History"


class Publication:

    def __init__(self, title, author, year, genre):

        current_year = datetime.now().year

        if year > current_year or year < 1450:
            raise ValueError("Некоректний рік видання")

        if not isinstance(genre, Genre):
            raise ValueError("Жанр повинен бути типу Genre")

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def get_info(self):
        return (
            f"{self.title} | "
            f"{self.author} | "
            f"{self.year} | "
            f"{self.genre.value}"
        )

    def publication_type(self):
        return "Publication"

    def __lt__(self, other):

        if not isinstance(other, Publication):
            return NotImplemented

        return self.year < other.year


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
                "Кількість сторінок повинна бути більше 0"
            )

        self.pages = pages

    def publication_type(self):
        return f"Book ({self.pages} pages)"


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
                "Номер випуску повинен бути більше 0"
            )

        self.issue_number = issue_number

    def publication_type(self):
        return f"Magazine №{self.issue_number}"


# Ітератор для посторінкового виводу
class PageIterator:

    def __init__(self, publications, page_size=5):

        self.publications = publications
        self.page_size = page_size
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.publications):
            raise StopIteration

        page = self.publications[
            self.index:self.index + self.page_size
        ]

        self.index += self.page_size

        return page


class Library:

    def __init__(self):

        self.publications = []

        self.company_name = "My Library"
        self.page_size = 5

    def load_config(
            self,
            filename="config.json"):

        if not os.path.exists(filename):
            print(
                "config.json не знайдено. "
                "Використовуються стандартні налаштування."
            )
            return

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

    def add_publication(self, publication):

        if not isinstance(
                publication,
                Publication):

            raise TypeError(
                "Можна додавати лише об'єкти Publication"
            )

        self.publications.append(publication)

    def display_all(self):

        if not self.publications:
            print("Каталог порожній")
            return

        for page_num, page in enumerate(
                PageIterator(
                    self.publications,
                    self.page_size
                ),
                start=1):

            print(
                f"\n=== Сторінка {page_num} ==="
            )

            for item in page:
                print(item.get_info())

    def save_system_state(
            self,
            filename="library_backup.pkl"):

        try:

            with open(filename, "wb") as file:
                pickle.dump(self, file)

            print(
                f"Стан системи збережено "
                f"у файл {filename}"
            )

        except Exception as e:

            print(
                f"Помилка збереження: {e}"
            )

    @staticmethod
    def load_system_state(
            filename="library_backup.pkl"):

        if not os.path.exists(filename):
            print(
                "Резервну копію не знайдено. "
                "Створено нову бібліотеку."
            )
            return Library()

        try:

            with open(filename, "rb") as file:
                library = pickle.load(file)

            print(
                f"Резервну копію завантажено "
                f"з {filename}"
            )

            return library

        except Exception as e:

            print(
                f"Помилка завантаження "
                f"резервної копії: {e}"
            )

            print(
                "Створено нову порожню бібліотеку."
            )

            return Library()

    def export_csv(
            self,
            filename="library_report.csv"):

        try:

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
                f"CSV звіт сформовано: "
                f"{filename}"
            )

        except Exception as e:

            print(
                f"Помилка експорту CSV: {e}"
            )