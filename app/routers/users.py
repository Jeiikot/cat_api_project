# FastAPI
from fastapi import APIRouter, Depends, Request, status

# Models
from app.models.common import PaginationParams, PaginatedResponse
from app.models.user import UserResponseModel, UserCreateModel, UserLoginModel

# Services
from app.services.user import UserService


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[UserResponseModel],
    summary="List all users",
    description="Retrieve a paginated list of all registered users.",
)
async def list_users(pagination: PaginationParams = Depends()):
    skip = pagination.page * pagination.limit
    return await UserService.list_users(
        limit=pagination.limit,
        skip=skip,
        page=pagination.page,
    )

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel,
    summary="Create a new user",
    description="Create a new user with a unique username automatically generated from the name and lastname. "
                "The password is securely hashed before storage.",
)
async def create_user(user: UserCreateModel):
    return await UserService.create_user(user)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
    summary="User login",
    description="Authenticate a user by verifying the provided username and password. "
                "Returns user data if credentials are valid."
)
async def login(login_data: UserLoginModel):
    return await UserService.login(login_data.username, login_data.password)
