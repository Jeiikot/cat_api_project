import pytest
from unittest.mock import AsyncMock, patch


PATCH_BREED_GET = "app.services.breed.httpx.AsyncClient.get"
PATCH_USER_GET  = "app.services.user.httpx.AsyncClient.get"


@pytest.fixture
def mock_breed_httpx_get():
    with patch(PATCH_BREED_GET, new_callable=AsyncMock) as mock_httpx_get:
        yield mock_httpx_get


@pytest.fixture
def mock_user_httpx_get():
    with patch(PATCH_USER_GET, new_callable=AsyncMock) as mock_httpx_get:
        yield mock_httpx_get
