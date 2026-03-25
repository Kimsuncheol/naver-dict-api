import pytest
from unittest.mock import patch
from naver_dict_api import DictEntry, DictType, SearchMode, NetworkError, ParseError
from services.dict import get_dict_types, lookup


SAMPLE_ENTRY = DictEntry(
    word="hello",
    reading="",
    meanings=["안녕, 인사, 여보세요"],
    entry_id="",
    dict_type="enko",
)


class TestGetDictTypes:
    def test_returns_all_types(self):
        result = get_dict_types()
        assert len(result) == len(list(DictType))

    def test_each_item_has_name_and_value(self):
        result = get_dict_types()
        for item in result:
            assert "name" in item
            assert "value" in item

    def test_names_are_lowercase(self):
        result = get_dict_types()
        for item in result:
            assert item["name"] == item["name"].lower()

    def test_contains_expected_types(self):
        result = get_dict_types()
        names = {item["name"] for item in result}
        assert "korean" in names
        assert "english" in names
        assert "japanese" in names
        assert "hanja" in names


class TestLookup:
    def test_valid_search_returns_entry(self):
        with patch("services.dict.search_dict", return_value=SAMPLE_ENTRY):
            result = lookup("hello", "english", "simple")
        assert result.word == "hello"
        assert result.meanings == ["안녕, 인사, 여보세요"]

    def test_invalid_dict_type_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown dict_type"):
            lookup("hello", "invalid_lang", "simple")

    def test_invalid_search_mode_raises_value_error(self):
        with pytest.raises(ValueError, match="search_mode"):
            lookup("hello", "english", "invalid_mode")

    def test_no_result_raises_lookup_error(self):
        with patch("services.dict.search_dict", return_value=None):
            with pytest.raises(LookupError, match="No results found"):
                lookup("xyzxyz", "english", "simple")

    def test_dict_type_case_insensitive(self):
        with patch("services.dict.search_dict", return_value=SAMPLE_ENTRY) as mock:
            lookup("hello", "ENGLISH", "simple")
            args = mock.call_args.args
            assert args[1] == DictType.ENGLISH

    def test_search_mode_case_insensitive(self):
        with patch("services.dict.search_dict", return_value=SAMPLE_ENTRY) as mock:
            lookup("hello", "english", "DETAILED")
            args = mock.call_args.args
            assert args[2] == SearchMode.DETAILED

    def test_network_error_propagates(self):
        with patch("services.dict.search_dict", side_effect=NetworkError("timeout")):
            with pytest.raises(NetworkError):
                lookup("hello", "english", "simple")

    def test_parse_error_propagates(self):
        with patch("services.dict.search_dict", side_effect=ParseError("bad json")):
            with pytest.raises(ParseError):
                lookup("hello", "english", "simple")
