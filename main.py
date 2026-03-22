import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from repositories.book_repository import JsonBookRepository
from services.library_service import LibraryService
from presentation.cli import LibraryCLI


def main():
    repo = JsonBookRepository("data/books.json")
    service = LibraryService(repo)
    cli = LibraryCLI(service)
    cli.run()


if __name__ == "__main__":
    main()