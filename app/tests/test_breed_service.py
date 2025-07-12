import pytest
from types import SimpleNamespace
from unittest.mock import patch, AsyncMock, MagicMock


from app.services.breed import BreedService
from app.models.common import PaginationParams


class DummyRequest(SimpleNamespace):
    @property
    def url(self):
        return "http://test/breeds?limit=1&page=0"


@pytest.mark.asyncio
@patch("app.services.breed.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_all_breeds(mock_get):
    mock_get.return_value.json = MagicMock(
        return_value=[{"id": "beng", "name": "Bengal"}]
    )
    mock_get.return_value.raise_for_status = MagicMock()

    pag = PaginationParams(limit=1, page=0)
    data = await BreedService.get_all_breeds(pag, DummyRequest())

    assert data.results[0].name == "Bengal"
    assert data.results[0].id == "beng"


@pytest.mark.asyncio
@patch("app.services.breed.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_breed_by_id(mock_get):
    mock_get.return_value.json = MagicMock(
        return_value={"id": "beng", "name": "Bengal"}
    )
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status = MagicMock()

    data = await BreedService.get_breed_by_id("beng")

    assert data["name"] == "Bengal"
    assert data["id"] == "beng"


@pytest.mark.asyncio
@patch("app.services.breed.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_search_breeds(mock_get):
    mock_get.return_value.json = MagicMock(
        return_value=[{"id": "beng", "name": "Bengal"}]
    )
    mock_get.return_value.raise_for_status = MagicMock()

    pag = PaginationParams(limit=10, page=0)
    data = await BreedService.search_breeds("beng", pag, DummyRequest())

    assert data.results[0].name == "Bengal"
    assert data.results[0].id == "beng"
