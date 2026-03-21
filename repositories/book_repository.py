from abc import ABC, abstractmethod


class BaseBookRepository(ABC): 
    
    @abstractmethod
    def get_all(self):
        """Get all"""
        pass 
    
    @abstractmethod
    def get_by_id(self, book_id: int):
        """Get by ID"""
        pass
    
    @abstractmethod
    def save(self, books):
        """Save book"""
        pass
    
    @abstractmethod
    def delete(self, book_id: int):
        """delete book ID"""
        pass
