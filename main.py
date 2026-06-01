import sys

from library_system import (
    Library,
    Book,
    Magazine,
    Genre
)


def show_menu():

    print("\n" + "=" * 35)
    print(" ЕЛЕКТРОННИЙ КАТАЛОГ БІБЛІОТЕКИ ")
    print("=" * 35)
    print("1. Показати всі видання")
    print("2. Додати книгу")
    print("3. Додати журнал")
    print("4. Зберегти стан")
    print("5. Експортувати CSV")
    print("0. Вихід")
    print("=" * 35)


if __name__ == "__main__":

    library = Library.load_system_state()

    library.load_config()

    print("Ласкаво просимо до Electronic Library Catalog")

    while True:

        show_menu()

        try:

            choice = input(
                "Оберіть пункт меню: "
            ).strip()

            match choice:

                case "1":

                    library.display_all()

                case "2":

                    title = input("Назва: ")
                    author = input("Автор: ")

                    year = int(
                        input("Рік видання: ")
                    )

                    pages = int(
                        input("Кількість сторінок: ")
                    )

                    print("\nЖанри:")

                    for index, genre in enumerate(
                            Genre,
                            start=1):

                        print(
                            index,
                            genre.name
                        )

                    genre_choice = int(
                        input("Оберіть жанр: ")
                    )

                    genre = list(Genre)[
                        genre_choice - 1
                    ]

                    book = Book(
                        title,
                        author,
                        year,
                        genre,
                        pages
                    )

                    library.add_publication(book)

                    print("Книгу додано")

                case "3":

                    title = input("Назва: ")
                    author = input("Редактор: ")

                    year = int(
                        input("Рік видання: ")
                    )

                    issue = int(
                        input("Номер випуску: ")
                    )

                    print("\nЖанри:")

                    for index, genre in enumerate(
                            Genre,
                            start=1):

                        print(
                            index,
                            genre.name
                        )

                    genre_choice = int(
                        input("Оберіть жанр: ")
                    )

                    genre = list(Genre)[
                        genre_choice - 1
                    ]

                    magazine = Magazine(
                        title,
                        author,
                        year,
                        genre,
                        issue
                    )

                    library.add_publication(
                        magazine
                    )

                    print("Журнал додано")

                case "4":

                    library.save_system_state()

                case "5":

                    library.export_csv()

                case "0":

                    print(
                        "\nАвтоматичне збереження..."
                    )

                    library.save_system_state()

                    print(
                        "Роботу завершено"
                    )

                    sys.exit(0)

                case _:

                    print(
                        "Невірний пункт меню"
                    )

        except ValueError as e:

            print(
                f"\nПомилка введення: {e}"
            )

            print(
                "Перевірте правильність введених даних."
            )

        except Exception as e:

            print(
                f"\nНесподівана помилка: {e}"
            )