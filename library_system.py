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
    def __init__(self, title, author, year, genre, pages):
        super().__init__(title, author, year, genre)

        if pages <= 0:
            raise ValueError("Кількість сторінок повинна бути більше 0")

        self.pages = pages

    def publication_type(self):
        return f"Book ({self.pages} pages)"


class Magazine(Publication):
    def __init__(self, title, author, year, genre, issue_number):
        super().__init__(title, author, year, genre)

        if issue_number <= 0:
            raise ValueError("Номер випуску повинен бути більше 0")

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

        page = self.publications[self.index:self.index + self.page_size]
        self.index += self.page_size
        return page


class Library:
    def __init__(self):
        self.publications = []
        self.company_name = "My Library"
        self.page_size = 5

    def load_config(self, filename="config.json"):
        if not os.path.exists(filename):
            print(
                "config.json не знайдено. "
                "Використовуються стандартні налаштування."
            )
            return

        with open(filename, "r", encoding="utf-8") as file:
            config = json.load(file)

        self.company_name = config.get("company_name", "My Library")
        self.page_size = config.get("page_size", 5)

        print("Конфігурацію завантажено")

    def add_publication(self, publication):
        if not isinstance(publication, Publication):
            raise TypeError("Можна додавати лише об'єкти Publication")

        self.publications.append(publication)

    def display_all(self):
        if not self.publications:
            print("Каталог порожній")
            return

        for page_num, page in enumerate(
            PageIterator(self.publications, self.page_size),
            start=1
        ):
            print(f"\n=== Сторінка {page_num} ===")
            for item in page:
                print(item.get_info(), "|", item.publication_type())

    def display_publications(self, publications):
        if not publications:
            print("Нічого не знайдено")
            return

        for index, pub in enumerate(publications, start=1):
            print(
                f"{index}. {pub.get_info()} | {pub.publication_type()}"
            )

    def search_by_title(self, title):
        return [
            pub for pub in self.publications
            if title.lower() in pub.title.lower()
        ]

    def search_by_author(self, author):
        return [
            pub for pub in self.publications
            if author.lower() in pub.author.lower()
        ]

    def search_by_genre(self, genre):
        return [
            pub for pub in self.publications
            if pub.genre == genre
        ]

    def sort_by_year(self):
        self.publications.sort()

    def sort_by_title(self):
        self.publications.sort(key=lambda pub: pub.title.lower())

    def sort_by_author(self):
        self.publications.sort(key=lambda pub: pub.author.lower())

    def filter_by_type(self, publication_class):
        return [
            pub for pub in self.publications
            if isinstance(pub, publication_class)
        ]

    def filter_by_year_range(self, start_year, end_year):
        return [
            pub for pub in self.publications
            if start_year <= pub.year <= end_year
        ]

    def edit_publication(
            self,
            index,
            title=None,
            author=None,
            year=None,
            genre=None,
            pages=None,
            issue_number=None):
        if index < 0 or index >= len(self.publications):
            raise IndexError("Невірний індекс")

        publication = self.publications[index]

        if title is not None and title != "":
            publication.title = title

        if author is not None and author != "":
            publication.author = author

        if year is not None:
            current_year = datetime.now().year
            if year > current_year or year < 1450:
                raise ValueError("Некоректний рік видання")
            publication.year = year

        if genre is not None:
            if not isinstance(genre, Genre):
                raise ValueError("Жанр повинен бути типу Genre")
            publication.genre = genre

        if isinstance(publication, Book) and pages is not None:
            if pages <= 0:
                raise ValueError("Кількість сторінок повинна бути більше 0")
            publication.pages = pages

        if isinstance(publication, Magazine) and issue_number is not None:
            if issue_number <= 0:
                raise ValueError("Номер випуску повинен бути більше 0")
            publication.issue_number = issue_number

    def save_system_state(self, filename="library_backup.pkl"):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self, file)

            print(f"Стан системи збережено у файл {filename}")

        except Exception as e:
            print(f"Помилка збереження: {e}")

    @staticmethod
    def load_system_state(filename="library_backup.pkl"):
        if not os.path.exists(filename):
            print(
                "Резервну копію не знайдено. "
                "Створено нову бібліотеку."
            )
            return Library()

        try:
            with open(filename, "rb") as file:
                library = pickle.load(file)

            print(f"Резервну копію завантажено з {filename}")
            return library

        except Exception as e:
            print(f"Помилка завантаження резервної копії: {e}")
            print("Створено нову порожню бібліотеку.")
            return Library()

    def export_csv(self, filename="library_report.csv"):
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
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

            print(f"CSV звіт сформовано: {filename}")

        except Exception as e:
            print(f"Помилка експорту CSV: {e}")