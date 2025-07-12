# FastAPI
from fastapi import Query

# Config
from app.core.config import DEFAULT_PAGINATION_LIMIT, MAX_PAGINATION_LIMIT

# External
from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel


T = TypeVar("T")


class PaginationParams:
    """
    Pagination parameters for query strings.
        - limit: Number of items per page.
        - page: Page number (starts from 0).
    """
    def __init__(
        self,
        limit: int = Query(DEFAULT_PAGINATION_LIMIT, ge=1, le=MAX_PAGINATION_LIMIT),
        page: int = Query(0, ge=0)
    ):
        self.limit = limit
        self.page = page

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response schema.
        - results: List of items of type T.
        - limit: Items per page.
        - page: Current page number.
        - next: URL for the next page (if any).
        - previous: URL for the previous page (if any).
    """
    results: List[T]
    limit: int
    page: int
    next: Optional[str]
    previous: Optional[str]
