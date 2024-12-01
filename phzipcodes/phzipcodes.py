import json
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Callable, Final, Sequence

from cachetools import TTLCache, cached
from pydantic import BaseModel

# Constants
DATA_FILE_PATH: Final = Path(__file__).parent / "data" / "ph_zip_codes.json"
DEFAULT_SEARCH_FIELDS: Final = ("city_municipality", "province", "region")
CACHE: TTLCache = TTLCache(maxsize=1000, ttl=3600)


class MatchType(str, Enum):
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    EXACT = "exact"


class ZipCode(BaseModel):
    """Represents a zip code entry with associated location information."""

    code: str
    city_municipality: str
    province: str
    region: str


# Core/primitive functions
@lru_cache(maxsize=1)
def load_data() -> dict[str, ZipCode]:
    """
    Load and cache zip code data from JSON file.

    Returns:
        dict[str, ZipCode]: A dictionary mapping zip codes to ZipCode objects.
    """
    with DATA_FILE_PATH.open(encoding="utf-8") as f:
        raw_data = json.load(f)

    return {
        code: ZipCode(
            code=code,
            city_municipality=city_municipality,
            province=province,
            region=region,
        )
        for region, provinces in raw_data.items()
        for province, cities_municipalities in provinces.items()
        for city_municipality, zip_codes in cities_municipalities.items()
        for code in zip_codes
    }


def get_match_function(match_type: str) -> Callable[[str, str], bool]:
    """Get appropriate string matching function based on match type."""
    matchers = {
        MatchType.CONTAINS: lambda field, q: q in field.lower(),
        MatchType.STARTSWITH: lambda field, q: field.lower().startswith(q),
        MatchType.EXACT: lambda field, q: field.lower() == q,
    }

    try:
        return matchers[MatchType(match_type)]
    except KeyError:
        raise ValueError(f"Invalid match type: {match_type}")


# Derived lookup functions
@cached(CACHE)
def find_by_zip(zip_code: str) -> ZipCode | None:
    """Get location information by zip code.

    Args:
        zip_code (str): zip code.

    Returns:
        ZipCode | None: ZipCode object if found, None otherwise.
    """
    return load_data().get(zip_code)


@cached(CACHE)
def find_by_city_municipality(city_municipality: str) -> list[dict[str, str]]:
    """
    Get zip codes, province and region by city/municipality name.

    Args:
        city_municipality (str): city or municipality name.

    Returns:
        list[dict[str, str]]: List of dictionaries with zip code, province, and region.
    """
    return [
        {
            "zip_code": zip_code.code,
            "province": zip_code.province,
            "region": zip_code.region,
        }
        for zip_code in load_data().values()
        if zip_code.city_municipality.lower() == city_municipality.lower()
    ]


@cached(CACHE)
def search(
    query: str,
    fields: Sequence[str] = DEFAULT_SEARCH_FIELDS,
    match_type: str = MatchType.CONTAINS,
) -> tuple[ZipCode, ...]:
    """
    Search for zip codes based on query and criteria.

    Args:
        query (str): Search term.
        fields (Sequence[str], optional): Defaults to DEFAULT_SEARCH_FIELDS.
        match_type (str, optional):  Defaults to MatchType.CONTAINS.

    Returns:
        tuple[ZipCode, ...]: A tuple of ZipCode objects matching the query.
    """
    query = query.lower()
    match_func = get_match_function(match_type)

    return tuple(
        zip_code
        for zip_code in load_data().values()
        if any(match_func(getattr(zip_code, field), query) for field in fields)
    )


@cached(CACHE)
def get_regions() -> list[str]:
    """
    Get all unique regions in the Philippines.

    Returns:
        list[str]: A list of all unique regions.
    """
    return sorted(
        {zip_code.region for zip_code in load_data().values() if zip_code.region}
    )


@cached(CACHE)
def get_provinces(region: str) -> list[str]:
    """
    Get all provinces within a specific region.

    Args:
        region (str): Region to get provinces for.

    Returns:
        list[str]: A list of provinces in the specified region.
    """
    return sorted(
        {
            zip_code.province
            for zip_code in load_data().values()
            if zip_code.region == region
        }
    )


@cached(CACHE)
def get_cities_municipalities(province: str) -> list[str]:
    """
    Get all cities and municipalities within a specific province.

    Args:
        province (str): Province to get cities/municipalities for.

    Returns:
        list[str]: A list of cities/municipalities in the specified province.
    """
    return sorted(
        {
            zip_code.city_municipality
            for zip_code in load_data().values()
            if zip_code.province == province
        }
    )


# TODO: Implement typer CLI
