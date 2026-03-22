from repositories.book_repository import BaseBookRepository
from models.book import Book
import csv
import os
from typing import List, Optional

class CsvBookRepository(BaseBookRepository):
    def __init__(self, file_path: str = "data/books.csv"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def get_all(self) -> List[Book]:
        books = []
        try:
            with open(self._file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    books.append(Book(
                        id=int(row["id"]),
                        title=row["title"],
                        author=row["author"],
                        year=int(row["year"]),
                        is_read=row["is_read"].lower() in ("true", "1", "yes", "так")
                    ))
        except FileNotFoundError:
            return []
        return books

    def get_by_id(self, book_id: int) -> Optional[Book]:
        for book in self.get_all():
            if book.id == book_id:
                return book
        return None

    def save(self, books: List[Book]) -> None:
        with open(self._file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "title", "author", "year", "is_read"])
            writer.writeheader()
            for book in books:
                writer.writerow({
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "is_read": str(book.is_read)
                })

    def delete(self, book_id: int) -> bool:
        books = self.get_all()
        new_books = [b for b in books if b.id != book_id]
        if len(new_books) == len(books):
            return False
        self.save(new_books)
        return True