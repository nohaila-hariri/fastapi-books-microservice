from pydantic import BaseModel, Field


class Book(BaseModel):
    """Represents a book with its details.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        published_year (int): The year the book was published.
    """
    title: str = Field(..., description="The title of the book")
    author: str = Field(..., description="The author of the book")
    published_year: int = Field(..., ge=0, description="The year the book was published (must be non-negative)")

    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "published_year": 1925,
            }
        }
