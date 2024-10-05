from fastapi import FastAPI, HTTPException

from .models import BookModel
from .schemas import Book


app = FastAPI()


@app.get("/books")
async def read_books():
    """Retrieve a list of all books.

    Returns:
        List[Book]: A list of book records.

    Note:
        This endpoint fetches all the books stored in the database.
    """
    return await BookModel.get_all_books()


@app.get("/books/{book_id}")
async def read_book(book_id: str):
    """Retrieve a single book by its ID.

    Args:
        book_id (str): The ID of the book to retrieve.

    Raises:
        HTTPException: If the book is not found, raises a 404 error.

    Returns:
        Book: The requested book record.

    Note:
        This endpoint fetches a specific book based on the provided ID.
    """
    book = await BookModel.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books")
async def create_book(book: Book):
    """Create a new book record.

    Args:
        book (Book): The book data to create.

    Returns:
        Book: The created book record.

    Note:
        This endpoint adds a new book to the database.
    """
    return await BookModel.add_book(book)


@app.put("/books/{book_id}")
async def modify_book(book_id: str, book: Book):
    """Update an existing book record.

    Args:
        book_id (str): The ID of the book to update.
        book (Book): The updated book data.

    Returns:
        dict: A message indicating the book has been updated.

    Note:
        This endpoint modifies the existing book record based on the provided ID.
    """
    await BookModel.update_book(book_id, book)
    return {"message": "Book updated"}


@app.delete("/books/{book_id}")
async def remove_book(book_id: str):
    """Delete a book record by its ID.

    Args:
        book_id (str): The ID of the book to delete.

    Returns:
        dict: A message indicating the book has been deleted.

    Note:
        This endpoint removes the book record from the database.
    """
    await BookModel.delete_book(book_id)
    return {"message": "Book deleted"}
