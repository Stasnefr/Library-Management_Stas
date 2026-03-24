from repositories.csv_book_repository import CsvBookRepository
from repositories.book_repository import JsonBookRepository
from services.library_service import LibraryService
from presentation.cli import LibraryCLI

def main():
    use_json = False 

    if use_json:
        repo = JsonBookRepository("data/books.json")
    else:
        repo = CsvBookRepository("data/books.csv")

    service = LibraryService(repo)
    cli = LibraryCLI(service)
    cli.run()

if __name__ == "__main__":
    main()