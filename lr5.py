from enum import Enum
import time

# Enum для суворої типізації жанрів
class Genre(Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    SCIENCE = "Science"
    HISTORY = "History"

# Базовий клас Publication
class Publication:
    def __init__(self, title, author, year, genre):
        # Валідація року видання
        if year > 2026 or year < 1450:
            raise ValueError("Некоректний рік видання")

        # Перевірка типу жанру
        if not isinstance(genre, Genre):
            raise ValueError("Жанр повинен бути типу Genre")

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    # Основна інформація
    def get_info(self):
        return f"{self.title} - {self.author}, {self.year}, {self.genre.value}"

    # Поліморфний метод
    def publication_type(self):
        return "Звичайне видання"

    # Порівняння за роком видання
    def __lt__(self, other):
        if not isinstance(other, Publication):
            return NotImplemented
        return self.year < other.year

    # Перевантаження оператора +
    def __add__(self, other):
        # Різниця між роками двох видань
        if isinstance(other, Publication):
            return abs(self.year - other.year)

        # Створення нового видання зі зміненим роком
        elif isinstance(other, int):
            return Publication(
                self.title,
                self.author,
                self.year + other,
                self.genre
            )

        raise TypeError("Непідтримуваний тип для додавання")

    def __str__(self):
        return self.get_info()

# Клас Book
class Book(Publication):
    def __init__(self, title, author, year, genre, pages):
        super().__init__(title, author, year, genre)

        if pages <= 0:
            raise ValueError("Кількість сторінок має бути більше 0")

        self.pages = pages

    def publication_type(self):
        return f"Книга, {self.pages} сторінок"

# Клас Magazine
class Magazine(Publication):
    def __init__(self, title, author, year, genre, issue_number):
        super().__init__(title, author, year, genre)

        if issue_number <= 0:
            raise ValueError("Номер випуску має бути більше 0")

        self.issue_number = issue_number

    def publication_type(self):
        return f"Журнал, випуск №{self.issue_number}"

# ФУНКТОР
# Бізнес-логіка: перевірка унікальності назв
# Запам'ятовує:
#   - кількість викликів
#   - список дублікатів
class PublicationValidator:
    def __init__(self):
        self.calls_count = 0
        self.duplicates = []

    def __call__(self, library, publication):
        self.calls_count += 1

        for item in library.publications:
            if item.title.lower() == publication.title.lower():
                self.duplicates.append(publication.title)
                return False

        return True

    def get_statistics(self):
        return {
            "calls_count": self.calls_count,
            "duplicates": self.duplicates
        }

# КАСТОМНИЙ ІТЕРАТОР
# Повертає тільки книги певного жанру
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

# Контекстний менеджер
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

        print(f"Вихід з бібліотеки. Статус: {self.status}")

# Клас Library (композиція)
class Library:
    def __init__(self):
        self.publications = []

        # Композиція з функтором
        self.validator = PublicationValidator()

    # Додавання нового видання
    def add_publication(self, publication):
        if not isinstance(publication, Publication):
            raise TypeError("Можна додавати лише Publication")

        # Використання функтора
        if self.validator(self, publication):
            self.publications.append(publication)
            print(f"Додано: {publication.title}")
        else:
            print(f"Видання '{publication.title}' вже існує")

    # Показ усіх видань
    def show_all(self):
        for item in self.publications:
            print(item.get_info())
            print(item.publication_type())

    # Сортування за роком
    def sort_by_year(self):
        self.publications.sort()

    # Повертає кастомний ітератор
    def get_by_genre(self, genre):
        return GenreIterator(self.publications, genre)

    # Генератор пагінації (по 3 об'єкти)
    def paginate(self, page_size=3):
        for i in range(0, len(self.publications), page_size):
            yield self.publications[i:i + page_size]

# ТЕСТУВАННЯ
if __name__ == "__main__":
    library = Library()

    book1 = Book("Dune", "Frank Herbert", 1965, Genre.SCI_FI, 412)
    book2 = Book("Harry Potter", "J.K. Rowling", 1997, Genre.FANTASY, 350)
    mag1 = Magazine("Science Today", "Editorial Team", 2020, Genre.SCIENCE, 12)
    book3 = Book("History of Europe", "John Smith", 2010, Genre.HISTORY, 500)
    book4 = Book("Foundation", "Isaac Asimov", 1951, Genre.SCI_FI, 255)
    book5 = Book("The Hobbit", "J.R.R. Tolkien", 1937, Genre.FANTASY, 310)
    book6 = Magazine("Physics Monthly", "Editors", 2022, Genre.SCIENCE, 7)

    # Додавання в бібліотеку
    library.add_publication(book1)
    library.add_publication(book2)
    library.add_publication(mag1)
    library.add_publication(book3)
    library.add_publication(book4)
    library.add_publication(book5)
    library.add_publication(book6)

    # Спроба додати дубль
    duplicate = Book("Dune", "Frank Herbert", 1965, Genre.SCI_FI, 412)
    library.add_publication(duplicate)

    print("\n=== Перевантаження оператора + ===")
    print("Різниця років:", book1 + book2)

    new_book = book1 + 5
    print("Нове видання:", new_book.get_info())

    print("\n=== Кастомний ітератор (лише SCI_FI) ===")
    for item in library.get_by_genre(Genre.SCI_FI):
        print(item.get_info())

    print("\n=== Генератор paginate() (по 3 об'єкти) ===")
    for page_number, page in enumerate(library.paginate(3), start=1):
        print(f"\nСторінка {page_number}:")
        for item in page:
            print(item.get_info())

    print("\n=== Статистика функтора ===")
    stats = library.validator.get_statistics()
    print("Кількість викликів:", stats["calls_count"])
    print("Дублікати:", stats["duplicates"])

 
    print("\n=== Контекстний менеджер ===")
    with LibraryContext(library, timeout=2) as ctx:
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