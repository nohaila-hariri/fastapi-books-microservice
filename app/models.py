from bson import ObjectId

from .database import MongoDBClient
from .schemas import Book


class BookModel:

    @staticmethod
    async def get_all_books():
        """Retrieve all books from the database.

        Returns:
            List[dict]: A list of book records, each containing its details.

        Note:
            This method fetches all book entries from the 'books_db' database.
        """
        books = []
        async with MongoDBClient() as client:
            database = client["books_db"]
            # Now you can use `database` to interact with collections
            async for book in database.books.find():
                book["_id"] = str(book["_id"])  # Convert ObjectId to str
                books.append(book)
            return books

    @staticmethod
    async def get_book(book_id: str):
        """Retrieve a single book by its ID.

        Args:
            book_id (str): The ID of the book to retrieve.

        Returns:
            dict: The requested book record, or None if not found.

        Note:
            This method fetches a specific book based on the provided ID.
        """
        async with MongoDBClient() as client:
            database = client["books_db"]
            book = await database.books.find_one({"_id": ObjectId(book_id)})
            if book:
                book["_id"] = str(book["_id"])  # Convert ObjectId to str
            return book

    @staticmethod
    async def add_book(book: Book):
        """Add a new book record to the database.

        Args:
            book (Book): The book data to create.

        Returns:
            str: The ID of the newly created book.

        Note:
            This method inserts a new book into the 'books_db' database.
        """
        async with MongoDBClient() as client:
            new_book = book.dict()
            database = client["books_db"]
            result = await database.books.insert_one(new_book)
            return str(result.inserted_id)

    @staticmethod
    async def update_book(book_id: str, book: Book):
        """Update an existing book record.

        Args:
            book_id (str): The ID of the book to update.
            book (Book): The updated book data.

        Note:
            This method modifies the existing book record based on the provided ID.
        """
        async with MongoDBClient() as client:
            database = client["books_db"]
            await database.books.update_one({"_id": ObjectId(book_id)}, {"$set": book.dict()})

    @staticmethod
    async def delete_book(book_id: str):
        """Delete a book record by its ID.

        Args:
            book_id (str): The ID of the book to delete.

        Note:
            This method removes the book record from the 'books_db' database.
        """
        async with MongoDBClient() as client:
            database = client["books_db"]
            await database.books.delete_one({"_id": ObjectId(book_id)})
