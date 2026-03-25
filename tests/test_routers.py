import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from naver_dict_api import DictEntry, NetworkError
from main import app

client = TestClient(app)

SAMPLE_ENTRY = DictEntry(
    word="hello",
    reading="",
    meanings=["안녕, 인사, 여보세요"],
    entry_id="",
    dict_type="enko",
)


class TestListDictTypes:
    def test_returns_200(self):
        response = client.get("/dict/types")
        assert response.status_code == 200

    def test_returns_list(self):
        response = client.get("/dict/types")
        assert isinstance(response.json(), list)

    def test_items_have_name_and_value(self):
        response = client.get("/dict/types")
        for item in response.json():
            assert "name" in item
            assert "value" in item


class TestSearch:
    def test_valid_search_returns_200(self):
        with patch("routers.dict.lookup", return_value=SAMPLE_ENTRY):
            response = client.get("/dict/search?query=hello&dict_type=english")
        assert response.status_code == 200

    def test_response_contains_word_and_meanings(self):
        with patch("routers.dict.lookup", return_value=SAMPLE_ENTRY):
            response = client.get("/dict/search?query=hello&dict_type=english")
        data = response.json()
        assert data["word"] == "hello"
        assert "meanings" in data

    def test_missing_query_returns_422(self):
        response = client.get("/dict/search")
        assert response.status_code == 422

    def test_invalid_dict_type_returns_400(self):
        with patch("routers.dict.lookup", side_effect=ValueError("Unknown dict_type 'xyz'.")):
            response = client.get("/dict/search?query=hello&dict_type=xyz")
        assert response.status_code == 400

    def test_invalid_search_mode_returns_400(self):
        with patch("routers.dict.lookup", side_effect=ValueError("search_mode must be 'simple' or 'detailed'.")):
            response = client.get("/dict/search?query=hello&dict_type=english&search_mode=bad")
        assert response.status_code == 400

    def test_no_result_returns_404(self):
        with patch("routers.dict.lookup", side_effect=LookupError("No results found.")):
            response = client.get("/dict/search?query=xyzxyz&dict_type=english")
        assert response.status_code == 404

    def test_network_error_returns_502(self):
        with patch("routers.dict.lookup", side_effect=NetworkError("timeout")):
            response = client.get("/dict/search?query=hello&dict_type=english")
        assert response.status_code == 502

    def test_default_dict_type_is_hanja(self):
        with patch("routers.dict.lookup", return_value=SAMPLE_ENTRY) as mock:
            client.get("/dict/search?query=偀")
            mock.assert_called_once_with("偀", "hanja", "simple")

    def test_default_search_mode_is_simple(self):
        with patch("routers.dict.lookup", return_value=SAMPLE_ENTRY) as mock:
            client.get("/dict/search?query=hello&dict_type=english")
            mock.assert_called_once_with("hello", "english", "simple")
