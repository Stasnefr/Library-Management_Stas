from dataclasses import dataclass

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    is_read: bool = False