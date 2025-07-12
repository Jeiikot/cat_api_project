# FastAPI
from fastapi import APIRouter, Depends, Request, status

# Models
from app.models.breed import BreedModel
from app.models.common import PaginationParams, PaginatedResponse

# Services
from app.services.breed import BreedService


router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[BreedModel],
    status_code=status.HTTP_200_OK,
    summary="List all breeds",
    description="Retrieve a list of all available cat breeds using TheCatAPI. Supports pagination."
)
async def get_all_breeds(pagination: PaginationParams = Depends(), request: Request = None):
    return await BreedService.get_all_breeds(pagination, request)


@router.get(
    "/search",
    response_model=PaginatedResponse[BreedModel],
    status_code=status.HTTP_200_OK,
    summary="Search cat breeds by name",
    description="Search cat breeds by name using a query string. Supports pagination."
)
async def search_breeds(query: str, pagination: PaginationParams = Depends(), request: Request = None):
    return await BreedService.search_breeds(query=query, pagination=pagination, request=request)


@router.get(
    "/{breed_id}",
    response_model=BreedModel,
    status_code=status.HTTP_200_OK,
    summary="Get breed by ID",
    description="Retrieve detailed information of a specific cat breed by its unique ID."
)
async def get_breed_by_id(breed_id: str):
    return await BreedService.get_breed_by_id(breed_id)
