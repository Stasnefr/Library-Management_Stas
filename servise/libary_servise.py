from repositories.book_repository import BaseBookRepository
from models.book import Book


class JsonBookRepository(BaseBookRepository):
    def __init__(self, file_path: str = "data/books.json"):
        self._file_path = file_path
    
    def get_all(self):
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Book(**item) for item in data]
    
    def get_by_id(self, book_id: int):
        books = self.get_all()
        for book in books:
            if book.id == book_id:
                return book
        return None
    
    def save(self, books):
        data = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "is_read": book.is_read
            }
            for book in books
        ]
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    
    def delete(self, book_id: int):
        books = self.get_all()
        original_len = len(books)
        books = [b for b in books if b.id != book_id]
        if len(books) < original_len:
            self.save(books)
            return True
        return False
    

    def add_book(self, title: str, author: str, year: int):
        if not title or not author:
            raise ValueError("Назва та автор обов'язкові")
        if year < 1000 or year > 2026:
            raise ValueError("Неправильний рік")
        
        books = self._repo.get_all()
        new_id = max((book.id for book in books), default=0) + 1
        
        new_book = Book(id=new_id, title=title, author=author, year=year, is_read=False)
        books.append(new_book)
        self._repo.save(books)
        
        return new_book


    def delete_book(self, book_id: int) -> bool:
      return self._repo.delete(book_id)


        def find_by_title(self, query: str):
        books = self._repo.get_all()
        query = query.lower()
        return [book for book in books if query in book.title.lower()]
    
    def find_by_author(self, query: str):
        books = self._repo.get_all()
        query = query.lower()
        return [book for book in books if query in book.author.lower()]


        def find_by_title(self, query: str):
        books = self._repo.get_all()
        query = query.lower()
        return [book for book in books if query in book.title.lower()]
    
    def find_by_author(self, query: str):
        books = self._repo.get_all()
        query = query.lower()
        return [book for book in books if query in book.author.lower()]


        def get_all_books(self):
        return self._repo.get_all()
    
    def mark_as_read(self, book_id: int, is_read: bool) -> bool:
        books = self._repo.get_all()
        for book in books:
            if book.id == book_id:
                book.is_read = is_read
                self._repo.save(books)
                return True
        return False
    
    def get_statistics(self):
        books = self._repo.get_all()
        total = len(books)
        read_count = sum(1 for book in books if book.is_read)
        
        from collections import Counter
        authors = [book.author for book in books]
        top_author = Counter(authors).most_common(1)
        
        return {
            "total": total,
            "read": read_count,
            "unread": total - read_count,
            "top_author": top_author[0][0] if top_author else None
        }