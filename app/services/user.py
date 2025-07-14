# FastAPI
from fastapi import HTTPException, status

# Models
from app.models.common import PaginatedResponse
from app.models.user import UserCreateModel, UserResponseModel

# MongoDB
from app.db.mongodb import users_collection

# Utils
from app.utils.security import hash_password


class UserService:
    @staticmethod
    async def _generate_username(name: str, lastname: str):
        """
        Generate a unique username using the name and lastname.

        Args:
            - name (str): User's first name.
            - lastname (str): User's last name.

        Returns:
            - str: Unique username.
        """
        base = (name + lastname).lower().replace(" ", "")
        suffix = 1
        username = base

        while await users_collection.find_one({"username": username}):
            username = f"{base}{suffix}"
            suffix += 1
        return username

    @staticmethod
    async def list_users(limit: int, skip: int, page: int):
        """
            Retrieve a paginated list of users.

            Args:
                - limit (int): Number of users per page.
                - skip (int): Number of users to skip.
                - page (int): Current page number.

            Returns:
                - PaginatedResponse: Paginated list of user data.
            """
        cursor = users_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
        users = [user async for user in cursor]
        return PaginatedResponse(
            results=users,
            limit=limit,
            page=page,
            next=None,
            previous=None
        )

    @staticmethod
    async def create_user(user: UserCreateModel) -> UserResponseModel:
        """
        Create a new user with unique username and hashed password.

        Args:
            - user (UserCreateModel): User creation input model.

        Returns:
            - UserResponseModel: Created user data (without password).
        """
        username = await UserService._generate_username(user.name, user.lastname)
        hashed_password = hash_password(user.password)

        user_data = {
            "name": user.name,
            "lastname": user.lastname,
            "username": username,
            "password": hashed_password
        }
        await users_collection.insert_one(user_data)

        return UserResponseModel(
            name=user.name,
            lastname=user.lastname,
            username=username
        )

    @staticmethod
    async def login(username: str, password: str) -> UserResponseModel:
        """
        Authenticate a user by verifying the username and hashed password.

        Args:
            - username (str): Provided username.
            - password (str): Provided plain password.

        Returns:
            - UserResponseModel: Authenticated user data (without password).

        Raises:
            - HTTPException: 401 if credentials are invalid.
        """
        hashed_password = hash_password(password)
        user = await users_collection.find_one(
            {"username": username, "password": hashed_password},
            {"_id": 0, "password": 0}
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return UserResponseModel(**user)
