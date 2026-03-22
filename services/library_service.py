from typing import List
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from repositories.book_repository import BaseBookRepository
from models.book import Book
from datetime import datetime


class LibraryService:
    def __init__(self, repo: BaseBookRepository):
        self._repo = repo
    
    def add_book(self, title: str, author: str, year: int) -> Book:
        if not title or not author:
            raise ValueError("Назва та автор обов'язкові")
        
        current_year = datetime.now().year
        if year < 1000 or year > current_year:
            raise ValueError("Неправильний рік")
        
        books = self._repo.get_all()
        new_id = max((book.id for book in books), default=0) + 1
        
        new_book = Book(id=new_id, title=title, author=author, year=year, is_read=False)
        books.append(new_book)
        self._repo.save(books)
        
        return new_book
    
    def delete_book(self, book_id: int) -> bool:
        return self._repo.delete(book_id)
    
    def find_by_title(self, query: str) -> List[Book]:
        query = query.lower().strip()
        return [book for book in self._repo.get_all() if query in book.title.lower()]
    
    def find_by_author(self, query: str) -> List[Book]:
        query = query.lower().strip()
        return [book for book in self._repo.get_all() if query in book.author.lower()]
    
    def get_all_books(self) -> List[Book]:
        return self._repo.get_all()
    
    def mark_as_read(self, book_id: int, is_read: bool) -> bool:
        books = self._repo.get_all()
        for book in books:
            if book.id == book_id:
                book.is_read = is_read
                self._repo.save(books)
                return True
        return False
    
    def get_statistics(self) -> dict:
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