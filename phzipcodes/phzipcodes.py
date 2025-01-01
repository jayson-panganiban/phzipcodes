"""
Philippines zip codes package.

This package provides functionality to work with Philippines zip codes,
including searching, retrieving information, and listing regions,
provinces, and cities/municipalities.
"""

import json
from collections.abc import Callable, Sequence
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Final, TypeAlias

from cachetools import TTLCache, cached
from pydantic import BaseModel, ConfigDict

# Constants Configuration
DATA_FILE_PATH: Final = Path(__file__).parent / "data" / "ph_zip_codes.json"
DEFAULT_SEARCH_FIELDS: Final = ("city_municipality", "province", "region")

# Cache Configuration
CACHE_CONFIG = {
    "zip_lookup": {
        "maxsize": 2000,  # Common postal code lookups
        "ttl": float("inf"),  # Static data rarely changes
    },
    "city_lookup": {
        "maxsize": 500,  # Frequent city searches
        "ttl": 604800,  # 7 days, for potential city name updates
    },
    "search": {
        "maxsize": 1000,  # High volume search queries
        "ttl": 3600,  # 1 hour for dynamic searches
    },
}

ZIP_CACHE = TTLCache(**CACHE_CONFIG["zip_lookup"])
CITY_CACHE = TTLCache(**CACHE_CONFIG["city_lookup"])
SEARCH_CACHE = TTLCache(**CACHE_CONFIG["search"])


class MatchType(str, Enum):
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    EXACT = "exact"


class ZipCode(BaseModel):
    model_config = ConfigDict(frozen=True, slots=True)

    code: str
    city_municipality: str
    province: str
    region: str


# Type aliases
ZipResult: TypeAlias = ZipCode | None
SearchResults: TypeAlias = tuple[ZipCode, ...]
CityMunicipalityResults: TypeAlias = list[dict[str, str]]
Cities: TypeAlias = list[str]
Regions: TypeAlias = list[str]
Provinces: TypeAlias = list[str]
MatchFunction: TypeAlias = Callable[[str, str], bool]


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


def get_match_function(match_type: str | MatchType) -> MatchFunction:
    """Get appropriate string matching function based on match type."""
    matchers: dict[MatchType, MatchFunction] = {
        MatchType.CONTAINS: lambda field, q: q in field.lower(),
        MatchType.STARTSWITH: lambda field, q: field.lower().startswith(q),
        MatchType.EXACT: lambda field, q: field.lower() == q,
    }

    match_type_enum = (
        MatchType(match_type) if isinstance(match_type, str) else match_type
    )
    return matchers[match_type_enum]


@cached(ZIP_CACHE)
def find_by_zip(zip_code: str) -> ZipResult:
    """
    Get location information by zip code.
    Args:
        zip_code (str): zip code.
    Returns:
        ZipResult: ZipCode object or None if not found.
    """
    return load_data().get(zip_code)


@cached(CITY_CACHE)
def find_by_city_municipality(city_municipality: str) -> CityMunicipalityResults:
    """
    Get zip codes, province and region by city/municipality name.
    Args:
        city_municipality (str): city or municipality name.
    Returns:
        CityMunicipalityResults: List of dictionaries with zip code, province, and region.
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


@cached(SEARCH_CACHE)
def search(
    query: str,
    fields: Sequence[str] = DEFAULT_SEARCH_FIELDS,
    match_type: str | MatchType = MatchType.CONTAINS,
) -> SearchResults:
    """
    Search for zip codes based on query and criteria.
    Args:
        query (str): Search term.
        fields (Sequence[str], optional): Defaults to DEFAULT_SEARCH_FIELDS.
        match_type (str, optional):  Defaults to MatchType.CONTAINS.
    Returns:
        SearchResults: A tuple of ZipCode objects matching the query.
    """
    query = query.lower()
    match_func = get_match_function(match_type)

    return tuple(
        zip_code
        for zip_code in load_data().values()
        if any(match_func(getattr(zip_code, field), query) for field in fields)
    )


@cached(CITY_CACHE)
def get_regions() -> Regions:
    """
    Get all unique regions in the Philippines.
    Returns:
        Regions: A list of unique regions.
    """
    return sorted(
        {zip_code.region for zip_code in load_data().values() if zip_code.region}
    )


@cached(CITY_CACHE)
def get_provinces(region: str) -> Provinces:
    """
    Get all provinces within a specific region.
    Args:
        region (str): Region to get provinces for.
    Returns:
        Provinces: A list of provinces in the specified region.
    """
    return sorted(
        {
            zip_code.province
            for zip_code in load_data().values()
            if zip_code.region == region
        }
    )


@cached(CITY_CACHE)
def get_cities_municipalities(province: str) -> Cities:
    """
    Get all cities and municipalities within a specific province.
    Args:
        province (str): Province to get cities/municipalities for.
    Returns:
        Cities: A list of cities and municipalities in the specified province.
    """
    return sorted(
        {
            zip_code.city_municipality
            for zip_code in load_data().values()
            if zip_code.province == province
        }
    )
