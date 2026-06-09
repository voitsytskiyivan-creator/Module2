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
    print("6. Пошук")
    print("7. Сортування")
    print("8. Фільтрація")
    print("9. Редагування")
    print("0. Вихід")
    print("=" * 35)


def choose_genre():
    print("\nЖанри:")
    for index, genre in enumerate(Genre, start=1):
        print(index, genre.name)

    genre_choice = int(input("Оберіть жанр: "))
    return list(Genre)[genre_choice - 1]


def print_publications_with_indices(library):
    if not library.publications:
        print("Каталог порожній")
        return

    for index, pub in enumerate(library.publications, start=1):
        print(f"{index}. {pub.get_info()} | {pub.publication_type()}")


if __name__ == "__main__":
    library = Library.load_system_state()
    library.load_config()

    print("Ласкаво просимо до Electronic Library Catalog")

    while True:
        show_menu()

        try:
            choice = input("Оберіть пункт меню: ").strip()

            match choice:
                case "1":
                    library.display_all()

                case "2":
                    title = input("Назва: ")
                    author = input("Автор: ")
                    year = int(input("Рік видання: "))
                    pages = int(input("Кількість сторінок: "))
                    genre = choose_genre()

                    book = Book(title, author, year, genre, pages)
                    library.add_publication(book)

                    print("Книгу додано")

                case "3":
                    title = input("Назва: ")
                    author = input("Редактор: ")
                    year = int(input("Рік видання: "))
                    issue = int(input("Номер випуску: "))
                    genre = choose_genre()

                    magazine = Magazine(title, author, year, genre, issue)
                    library.add_publication(magazine)

                    print("Журнал додано")

                case "4":
                    library.save_system_state()

                case "5":
                    library.export_csv()

                case "6":
                    print("\n1. За назвою")
                    print("2. За автором")
                    print("3. За жанром")

                    search_choice = input("Оберіть тип пошуку: ").strip()

                    if search_choice == "1":
                        title = input("Назва: ")
                        results = library.search_by_title(title)

                    elif search_choice == "2":
                        author = input("Автор: ")
                        results = library.search_by_author(author)

                    elif search_choice == "3":
                        genre = choose_genre()
                        results = library.search_by_genre(genre)

                    else:
                        print("Невірний пункт пошуку")
                        continue

                    library.display_publications(results)

                case "7":
                    print("\n1. За роком")
                    print("2. За назвою")
                    print("3. За автором")

                    sort_choice = input("Оберіть: ").strip()

                    if sort_choice == "1":
                        library.sort_by_year()
                    elif sort_choice == "2":
                        library.sort_by_title()
                    elif sort_choice == "3":
                        library.sort_by_author()
                    else:
                        print("Невірний пункт сортування")
                        continue

                    print("Список відсортовано")

                case "8":
                    print("\n1. Лише книги")
                    print("2. Лише журнали")
                    print("3. За роками")

                    filter_choice = input("Оберіть: ").strip()

                    if filter_choice == "1":
                        result = library.filter_by_type(Book)

                    elif filter_choice == "2":
                        result = library.filter_by_type(Magazine)

                    elif filter_choice == "3":
                        start_year = int(input("Від року: "))
                        end_year = int(input("До року: "))
                        result = library.filter_by_year_range(start_year, end_year)

                    else:
                        print("Невірний пункт фільтрації")
                        continue

                    library.display_publications(result)

                case "9":
                    print_publications_with_indices(library)

                    if not library.publications:
                        continue

                    index = int(
                        input("\nНомер запису для редагування: ")
                    ) - 1

                    print(
                        "Залиште поле порожнім, "
                        "щоб не змінювати значення."
                    )

                    title = input("Нова назва: ").strip()
                    author = input("Новий автор/редактор: ").strip()

                    year_input = input("Новий рік: ").strip()
                    year = int(year_input) if year_input else None

                    print("\nОберіть новий жанр або натисніть Enter, щоб не змінювати:")
                    for i, genre in enumerate(Genre, start=1):
                        print(i, genre.name)

                    genre_input = input("Жанр: ").strip()
                    genre = list(Genre)[int(genre_input) - 1] if genre_input else None

                    pages = None
                    issue_number = None

                    current_pub = library.publications[index]
                    if isinstance(current_pub, Book):
                        pages_input = input("Нові сторінки: ").strip()
                        pages = int(pages_input) if pages_input else None
                    elif isinstance(current_pub, Magazine):
                        issue_input = input("Новий номер випуску: ").strip()
                        issue_number = int(issue_input) if issue_input else None

                    library.edit_publication(
                        index=index,
                        title=title if title else None,
                        author=author if author else None,
                        year=year,
                        genre=genre,
                        pages=pages,
                        issue_number=issue_number
                    )

                    print("Запис оновлено")

                case "0":
                    print("\nАвтоматичне збереження...")
                    library.save_system_state()
                    print("Роботу завершено")
                    sys.exit(0)

                case _:
                    print("Невірний пункт меню")

        except ValueError as e:
            print(f"\nПомилка введення: {e}")
            print("Перевірте правильність введених даних.")

        except IndexError as e:
            print(f"\nПомилка індексу: {e}")

        except Exception as e:
            print(f"\nНесподівана помилка: {e}")