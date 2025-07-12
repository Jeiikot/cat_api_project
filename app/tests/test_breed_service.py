# FastAPI
from fastapi import HTTPException

import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock


# Models
from app.models.common import PaginationParams

# Services
from app.services.breed import BreedService



class DummyRequest(SimpleNamespace):
    @property
    def url(self):
        return "http://test/breeds?limit=1&page=0"


@pytest.mark.asyncio
class TestBreedService:

    @staticmethod
    def generate_mock_breeds(fake, count=1):
        return [{"id": fake.lexify(text="????"), "name": fake.word()} for _ in range(count)]

    @staticmethod
    def setup_mock_response(mock_httpx, data):
        mock_httpx.return_value.json = MagicMock(return_value=data)
        mock_httpx.return_value.raise_for_status = MagicMock()

    async def test_get_all_breeds_returns_expected_data(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=1)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=len(mock_data), page=0)
        data = await BreedService.get_all_breeds(pagination, DummyRequest())

        assert data.results[0].id == mock_data[0]["id"]
        assert data.results[0].name == mock_data[0]["name"]

    async def test_get_all_breeds_first_page_no_next_or_previous(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=2)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=2, page=0)
        data = await BreedService.get_all_breeds(pagination, DummyRequest())

        assert data.previous is None
        assert data.next is None

    async def test_get_all_breeds_middle_page_has_previous_no_next(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=2)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=1, page=1)
        data = await BreedService.get_all_breeds(pagination, DummyRequest())

        assert data.page == 1
        assert data.previous is not None
        assert data.next is None

    async def test_get_all_breeds_next_page_exists(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=3)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=2, page=0)
        data = await BreedService.get_all_breeds(pagination, DummyRequest())

        assert data.next is not None
        assert data.previous is None

    async def test_get_breed_by_id(self, mock_breed_httpx_get):
        mock_breed_httpx_get.return_value.json = MagicMock(
            return_value={"id": "beng", "name": "Bengal"}
        )
        mock_breed_httpx_get.return_value.status_code = 200
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock()

        data = await BreedService.get_breed_by_id("beng")

        assert data["name"] == "Bengal"
        assert data["id"] == "beng"

    async def test_get_breed_not_found(self, mock_breed_httpx_get):
        mock_breed_httpx_get.return_value.status_code = 404
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock()

        with pytest.raises(HTTPException) as exc:
            await BreedService.get_breed_by_id("nope")
        assert exc.value.status_code == 404


    async def test_search_breeds(self, mock_breed_httpx_get):
        mock_breed_httpx_get.return_value.json = MagicMock(
            return_value=[{"id": "beng", "name": "Bengal"}]
        )
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock()

        pag = PaginationParams(limit=10, page=0)
        data = await BreedService.search_breeds("beng", pag, DummyRequest())

        assert data.results[0].name == "Bengal"
        assert data.results[0].id == "beng"
