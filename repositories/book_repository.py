import json
import os
import sys
from abc import ABC, abstractmethod
from typing import List, Optional

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.book import Book


class BaseBookRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass 
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def save(self, books: List[Book]) -> None:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass


class JsonBookRepository(BaseBookRepository):
    def __init__(self, file_path: str = "data/books.json"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    def get_all(self) -> List[Book]:
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не знайдено:(")
            return []
        return [Book(**item) for item in data]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        for book in self.get_all():
            if book.id == book_id:
                return book
        return None
    
    def save(self, books: List[Book]) -> None:
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
    
    def delete(self, book_id: int) -> bool:
        books = self.get_all()
        original_len = len(books)
        books = [b for b in books if b.id != book_id]
        if len(books) < original_len:
            self.save(books)
            return True
        return False