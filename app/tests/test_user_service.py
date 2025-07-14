# FastAPI
from fastapi import HTTPException, status

# Models
from app.models.user import UserCreateModel

# Services
from app.services.user import UserService

# Utils
from app.utils.security import hash_password
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
class TestUserService:

    @staticmethod
    def setup_mock_user(mock_collection, user_data):
        mock_collection.find_one = AsyncMock(return_value=user_data)
        mock_collection.insert_one = AsyncMock()

    async def test_create_user_success(self, mock_user_httpx_get, fake):
        with patch("app.services.user.users_collection") as mock_users:
            mock_users.find_one = AsyncMock(return_value=None)
            mock_users.insert_one = AsyncMock()

            user_data = UserCreateModel(
                name=fake.first_name(),
                lastname=fake.last_name(),
                password=fake.password()
            )

            result = await UserService.create_user(user_data)

            assert result.username.startswith(user_data.name.lower())
            mock_users.insert_one.assert_awaited_once()

    async def test_login_success(self, fake):
        with patch("app.services.user.users_collection") as mock_users:
            password = fake.password()
            hashed = hash_password(password)

            data_mock = {
                "name": fake.first_name(),
                "lastname": fake.last_name(),
                "password": hashed,
            }
            data_mock["username"] = f"{data_mock['name']}{data_mock['lastname']}".lower()

            self.setup_mock_user(mock_users, data_mock)

            result = await UserService.login(data_mock["username"], password)

            assert result.username == data_mock["username"]

    async def test_login_failure_invalid_credentials(self, fake):
        with patch("app.services.user.users_collection") as mock_users:
            self.setup_mock_user(mock_users, None)

            with pytest.raises(HTTPException) as exc:
                await UserService.login(fake.first_name(), fake.password())

            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
