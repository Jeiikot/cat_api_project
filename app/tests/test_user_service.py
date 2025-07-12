import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from app.models.user import UserCreateModel
from app.services.user import UserService

from app.utils.security import hash_password


@pytest.mark.asyncio
@patch("app.services.user.users_collection")
async def test_create_user(mock_users):
    mock_users.find_one = AsyncMock(return_value=None)
    mock_users.insert_one = AsyncMock()

    body = UserCreateModel(name="John", lastname="Doe", password="1234")
    result = await UserService.create_user(body)

    assert result.username.startswith("johndoe")
    mock_users.insert_one.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.user.users_collection")
async def test_login_success(mock_users):
    hashed = hash_password("1234")
    mock_users.find_one = AsyncMock(return_value={
        "name": "John", "lastname": "Doe",
        "username": "johndoe", "password": hash_password("1234")
    })

    result = await UserService.login("johndoe", "1234")
    assert result.username == "johndoe"


@pytest.mark.asyncio
@patch("app.services.user.users_collection")
async def test_login_failure(mock_users):
    mock_users.find_one = AsyncMock(return_value=None)
    with pytest.raises(HTTPException):
        await UserService.login("wrong", "wrong")
