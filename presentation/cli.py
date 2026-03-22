import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.library_service import LibraryService
from models.book import Book

class LibraryCLI:
    def __init__(self, service: LibraryService):
        self._service = service
    
    def run(self):
        while True:
            self._print_menu()
            choice = input("\nВаш вибір: ").strip()
            
            if choice == "1":
                self._add_book()
            elif choice == "2":
                self._delete_book()
            elif choice == "3":
                self._find_by_title()
            elif choice == "4":
                self._find_by_author()
            elif choice == "5":
                self._show_all_books()
            elif choice == "6":
                self._mark_as_read()
            elif choice == "7":
                self._show_statistics()
            elif choice == "0":
                print("До побачення!")
                break
            else:
                print("Невідомий вибір. Спробуйте ще раз.")
            
            input("\nНатисніть Enter для продовження...")
    
    def _print_menu(self):
        print("\n" + "=" * 40)
        print("       БІБЛІОТЕКА")
        print("=" * 40)
        print("1. Додати книгу")
        print("2. Видалити книгу")
        print("3. Знайти за назвою")
        print("4. Знайти за автором")
        print("5. Показати всі книги")
        print("6. Позначити як прочитану/непрочитану")
        print("7. Статистика")
        print("0. Вихід")
        print("=" * 40)
    
    def _add_book(self):
        print("\n--- Додавання книги ---")
        
        title = input("Назва: ").strip()
        author = input("Автор: ").strip()
        year_input = input("Рік видання: ").strip()
        
        try:
            year = int(year_input)
        except ValueError:
            print("Помилка: рік має бути числом")
            return
        
        try:
            book = self._service.add_book(title, author, year)
            print(f"Книгу додано: ID={book.id}, '{book.title}'")
        except ValueError as e:
            print(f"Помилка: {e}")
    
    def _delete_book(self):
        print("\n--- Видалення книги ---")
        
        id_input = input("ID книги для видалення: ").strip()
        
        try:
            book_id = int(id_input)
        except ValueError:
            print("Помилка: ID має бути числом")
            return
        
        confirm = input(f"Видалити книгу ID={book_id}? (так/ні): ").strip().lower()
        if confirm not in ("так", "т", "yes", "y"):
            print("Видалення скасовано")
            return
        
        if self._service.delete_book(book_id):
            print(f"Книгу ID={book_id} видалено")
        else:
            print(f"Книгу ID={book_id} не знайдено")
    
    def _find_by_title(self):
        print("\n--- Пошук за назвою ---")
        
        query = input("Введіть частину назви: ").strip()
        if not query:
            print("Запит порожній")
            return
        
        books = self._service.find_by_title(query)
        self._print_books(books, f"Результати пошуку '{query}'")
    
    def _find_by_author(self):
        print("\n--- Пошук за автором ---")
        
        query = input("Введіть частину імені автора: ").strip()
        if not query:
            print("Запит порожній")
            return
        
        books = self._service.find_by_author(query)
        self._print_books(books, f"Результати пошуку '{query}'")
    
    def _show_all_books(self):
        books = self._service.get_all_books()
        self._print_books(books, "Всі книги")
    
    def _mark_as_read(self):
        print("\n--- Зміна статусу ---")
        
        id_input = input("ID книги: ").strip()
        try:
            book_id = int(id_input)
        except ValueError:
            print("Помилка: ID має бути числом")
            return
        
        status_input = input("Прочитана? (так/ні): ").strip().lower()
        is_read = status_input in ("так", "т", "yes", "y", "1")
        
        if self._service.mark_as_read(book_id, is_read):
            status_str = "прочитана" if is_read else "непрочитана"
            print(f"Книгу ID={book_id} позначено як {status_str}")
        else:
            print(f"Книгу ID={book_id} не знайдено")
    
    def _show_statistics(self):
        stats = self._service.get_statistics()
        
        print("\n--- Статистика ---")
        print(f"Всього книг:     {stats['total']}")
        print(f"Прочитано:       {stats['read']}")
        print(f"Непрочитано:     {stats['unread']}")
        
        top_author = stats['top_author']
        if top_author:
            print(f"Топ-автор:       {top_author}")
        else:
            print("Топ-автор:       —")
    
    def _print_books(self, books, title):
        print(f"\n--- {title} ---")
        
        if not books:
            print("Книг не знайдено")
            return
        
        print(f"{'ID':<4} {'Статус':<10} {'Рік':<6} {'Автор':<20} {'Назва'}")
        print("-" * 70)
        
        for book in books:
            status = "+" if book.is_read else "-"
            print(f"{book.id:<4} {status:<10} {book.year:<6} {book.author:<20} {book.title}")
        
        print(f"\nВсього: {len(books)} книг")