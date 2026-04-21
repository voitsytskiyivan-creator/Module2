from enum import Enum
import time


# Перелічуваний тип для суворої типізації жанрів
class Genre(Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    HISTORY = "History"


# Базовий клас Publication
class Publication:
    def __init__(self, title, author, year, genre):
        # Валідація року видання (архітектурний краш-тест)
        if year > 2026 or year < 1450:
            raise ValueError("Некоректний рік видання")

        # Перевірка типу жанру
        if not isinstance(genre, Genre):
            raise ValueError("Жанр повинен бути типу Genre")

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    # Метод для виводу основної інформації
    def get_info(self):
        return f"{self.title} - {self.author}, {self.year}, {self.genre.value}"

    # Базова реалізація поліморфного методу
    def publication_type(self):
        return "Звичайне видання"

    # Перевантаження оператора < (сортування за роком)
    def __lt__(self, other):
        return self.year < other.year

    # Перевантаження оператора +
    def __add__(self, other):
        # Якщо додаємо два видання — повертаємо різницю років
        if isinstance(other, Publication):
            return abs(self.year - other.year)

        # Якщо додаємо число — створюємо нове "оновлене" видання
        elif isinstance(other, int):
            return Publication(
                self.title,
                self.author,
                self.year + other,
                self.genre
            )
        else:
            raise TypeError("Непідтримуваний тип для додавання")


# Клас Book наслідує Publication
class Book(Publication):
    def __init__(self, title, author, year, genre, pages):
        # Виклик конструктора базового класу
        super().__init__(title, author, year, genre)

        # Валідація кількості сторінок
        if pages <= 0:
            raise ValueError("Книга не може мати 0 або від'ємну кількість сторінок")

        self.pages = pages

    # Перевизначення поліморфного методу
    def publication_type(self):
        return f"Книга, {self.pages} сторінок"


# Клас Magazine наслідує Publication
class Magazine(Publication):
    def __init__(self, title, author, year, genre, issue_number):
        super().__init__(title, author, year, genre)

        # Валідація номера випуску
        if issue_number <= 0:
            raise ValueError("Номер випуску має бути більше 0")

        self.issue_number = issue_number

    # Перевизначення поліморфного методу
    def publication_type(self):
        return f"Журнал, випуск №{self.issue_number}"


# Контекстний менеджер для контролю часу роботи
class LibraryContext:
    def __init__(self, library, timeout=3):
        self.library = library
        self.timeout = timeout
        self.status = "Active"

    # Викликається при вході в блок with
    def __enter__(self):
        self.start_time = time.time()
        print("Вхід у бібліотеку")
        return self

    # Викликається при виході з блоку with
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time

        # Якщо перевищено час — змінюємо статус
        if elapsed > self.timeout:
            self.status = "Expired"

        print(f"Вихід з бібліотеки. Статус: {self.status}")


# Клас-менеджер Library (композиція)
class Library:
    def __init__(self):
        # Список об'єктів Publication
        self.publications = []

    # Додавання нового видання
    def add_publication(self, publication):
        if not isinstance(publication, Publication):
            raise TypeError("Можна додавати лише Publication")
        self.publications.append(publication)

    # Вивід усіх видань (поліморфізм)
    def show_all(self):
        for item in self.publications:
            print(item.get_info())
            print(item.publication_type())

    # Сортування за роком
    def sort_by_year(self):
        self.publications.sort()

    # Ітератор (видає відсортовані об'єкти)
    def __iter__(self):
        # Сортуємо перед ітерацією
        self.sorted_list = sorted(self.publications, key=lambda x: x.year)
        self.index = 0
        return self

    # Повертає по 5 елементів (посторінковий вивід)
    def __next__(self):
        if self.index >= len(self.sorted_list):
            raise StopIteration

        batch = self.sorted_list[self.index:self.index + 5]
        self.index += 5
        return batch


# ТЕСТУВАННЯ
library = Library()

book1 = Book("Dune", "Frank Herbert", 1965, Genre.SCI_FI, 412)
book2 = Book("Harry Potter", "J.K. Rowling", 1997, Genre.FANTASY, 350)
mag1 = Magazine("Science Today", "Editorial Team", 2020, Genre.SCIENCE, 12)
book3 = Book("History of Europe", "John Smith", 2010, Genre.HISTORY, 500)
book4 = Book("Foundation", "Isaac Asimov", 1951, Genre.SCI_FI, 255)
book5 = Book("The Hobbit", "J.R.R. Tolkien", 1937, Genre.FANTASY, 310)
book6 = Book("Physics Monthly", "Editors", 2022, Genre.SCIENCE, 7)

# Додавання об'єктів у бібліотеку
library.add_publication(book1)
library.add_publication(book2)
library.add_publication(mag1)
library.add_publication(book3)
library.add_publication(book4)
library.add_publication(book5)
library.add_publication(book6)


print("=== Перевантаження оператора + ===")
print("Різниця років:", book1 + book2)

new_book = book1 + 5
print("Нове видання:", new_book.get_info())


print("\n=== Ітерація (відсортовано) ===")
for batch in library:
    print("Нова сторінка:")
    for item in batch:
        print(item.get_info())


print("\n=== Контекстний менеджер ===")
with LibraryContext(library, timeout=2) as ctx:
    time.sleep(3)  # імітація перевищення часу


print("\n=== Краш-тест ===")
try:
    bad_book = Book("Impossible Book", "Unknown", 3000, Genre.SCI_FI, -50)
except ValueError as e:
    print("Помилка:", e)