# FastAPI
import httpx
from fastapi import HTTPException, status

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

    async def test_get_breed_by_id(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=1)
        mock_breed_httpx_get.return_value.json = MagicMock(return_value=mock_data[0])
        mock_breed_httpx_get.return_value.status_code = status.HTTP_200_OK
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock()

        data = await BreedService.get_breed_by_id("beng")

        assert data["id"] == mock_data[0]["id"]
        assert data["name"] == mock_data[0]["name"]

    async def test_get_breed_not_found(self, mock_breed_httpx_get, fake):
        mock_breed_httpx_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock()

        with pytest.raises(HTTPException) as exc:
            await BreedService.get_breed_by_id(fake.lexify(text="????"))
        assert exc.value.status_code == 404

    async def test_get_breed_by_id_unexpected_error(self, mock_breed_httpx_get, fake):
        mock_request = MagicMock()
        mock_response = MagicMock(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        mock_breed_httpx_get.return_value.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_breed_httpx_get.return_value.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Internal Server Error", request=mock_request, response=mock_response
            )
        )

        with pytest.raises(httpx.HTTPStatusError):
            await BreedService.get_breed_by_id(fake.lexify(text="????"))

    async def test_search_breeds_success(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=1)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=10, page=0)
        data = await BreedService.search_breeds(mock_data[0]["name"], pagination, DummyRequest())

        assert data.results[0].id == mock_data[0]["id"]
        assert data.results[0].name == mock_data[0]["name"]
        assert data.previous is None
        assert data.next is None

    async def test_search_breeds_not_found(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=0)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        pagination = PaginationParams(limit=5, page=0)
        with pytest.raises(HTTPException) as error:
            await BreedService.search_breeds("does-not-exist", pagination, DummyRequest())
        assert error.value.status_code == status.HTTP_404_NOT_FOUND

    async def test_search_breeds_pagination_links(self, mock_breed_httpx_get, fake):
        mock_data = self.generate_mock_breeds(fake, count=3)
        self.setup_mock_response(mock_breed_httpx_get, mock_data)

        page_number_0= PaginationParams(limit=2, page=0)
        response = await BreedService.search_breeds("query", page_number_0, DummyRequest())
        assert response.previous is None
        assert response.next.endswith("page=1")

        page_number_1 = PaginationParams(limit=2, page=1)
        response = await BreedService.search_breeds("query", page_number_1, DummyRequest())
        assert response.previous is not None
        assert response.next is None
