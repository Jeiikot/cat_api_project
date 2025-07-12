# FastAPI
from fastapi import HTTPException, Request, status

# Models
from app.models.breed import BreedModel
from app.models.common import PaginationParams, PaginatedResponse

# Config
from app.core.config import CAT_API_KEY, CAT_API_URL

# External
import httpx


headers = {"x-api-key": CAT_API_KEY}


class BreedService:
    @staticmethod
    async def get_all_breeds(pagination: PaginationParams, request: Request) -> PaginatedResponse[BreedModel]:
        """
        Retrieve a paginated list of all cat breeds.

        Args:
            - pagination (PaginationParams): Pagination parameters (limit and page).
            - request (Request): FastAPI request object to build pagination URLs.

        Returns:
            - PaginatedResponse[Breed]: A paginated response with breed data.
        """
        params = {"limit": pagination.limit, "page": pagination.page}

        # Fetch and paginate all cat breeds
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAT_API_URL}/breeds", headers=headers, params=params)
            response.raise_for_status()
            breeds = response.json()

        # Build pagination
        base_url = str(request.url).split("?")[0]
        query = f"limit={pagination.limit}&page={{}}"

        start = pagination.page * pagination.limit
        end = start + pagination.limit


        return PaginatedResponse[BreedModel](
            results=breeds,
            limit=pagination.limit,
            page=pagination.page,
            next=f"{base_url}?{query.format(pagination.page + 1)}" if end < len(breeds) else None,
            previous=f"{base_url}?{query.format(pagination.page - 1)}" if pagination.page > 0 else None,
        )

    @staticmethod
    async def get_breed_by_id(breed_id: str) -> BreedModel:
        """
        Retrieve a specific cat breed by its ID.

        Args:
            - breed_id (str): The unique identifier of the breed.

        Returns:
            - Breed: The breed that matches the given ID.

        Raises:
            - HTTPException: If no breed is found with the provided ID.
        """
        # Retrieve a specific cat breed filtered by ID
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAT_API_URL}/breeds/{breed_id}", headers=headers)

            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Breed not found")

            response.raise_for_status()
            return response.json()


    @staticmethod
    async def search_breeds(query: str, pagination: PaginationParams, request: Request) -> PaginatedResponse[BreedModel]:
        """
        Search for cat breeds by name and return a paginated result.

        Args:
            - query (str): The search term to match breed names.
            - pagination (PaginationParams): Pagination parameters (limit and page).
            - request (Request): FastAPI request object to build pagination URLs.

        Returns:
            - PaginatedResponse[Breed]: A paginated list of matched breeds.

        Raises:
            - HTTPException: If no breeds are found for the search query.
        """
        params = {
            "q": query,
            "attach_image": 1
        }
        # Search breeds by name and paginate the results
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CAT_API_URL}/breeds/search", headers=headers, params=params)
            response.raise_for_status()
            breeds = response.json()

        if not breeds:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Breed not found")

        # Build pagination
        start = pagination.page * pagination.limit
        end = start + pagination.limit
        paginated = breeds[start:end]
        base_url = str(request.url).split("?")[0]
        query_params = f"query={query}&limit={pagination.limit}&page={{}}"

        return PaginatedResponse[BreedModel](
            results=paginated,
            limit=pagination.limit,
            page=pagination.page,
            next=f"{base_url}?{query_params.format(pagination.page + 1)}" if end < len(breeds) else None,
            previous=f"{base_url}?{query_params.format(pagination.page - 1)}" if pagination.page > 0 else None,
        )
