from naver_dict_api import search_dict, DictType, SearchMode, NaverDictError, DictEntry

DICT_TYPE_MAP = {d.name.lower(): d for d in DictType}
SEARCH_MODE_MAP = {m.name.lower(): m for m in SearchMode}


def get_dict_types() -> list[dict]:
    return [{"name": d.name.lower(), "value": d.value} for d in DictType]


def lookup(query: str, dict_type: str, search_mode: str) -> DictEntry:
    dt = DICT_TYPE_MAP.get(dict_type.lower())
    if dt is None:
        raise ValueError(f"Unknown dict_type '{dict_type}'.")

    sm = SEARCH_MODE_MAP.get(search_mode.lower())
    if sm is None:
        raise ValueError("search_mode must be 'simple' or 'detailed'.")

    entry = search_dict(query, dt, sm)
    if entry is None:
        raise LookupError("No results found.")

    return entry
