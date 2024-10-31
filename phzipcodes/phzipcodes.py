import json
from functools import lru_cache
from pathlib import Path
from typing import Callable, Sequence

from cachetools import TTLCache, cached
from pydantic import BaseModel

# Constants
DATA_FILE_PATH = Path(__file__).parent / "data" / "ph_zip_codes.json"
DEFAULT_SEARCH_FIELDS = ("city_municipality", "province", "region")
CACHE: TTLCache = TTLCache(maxsize=1000, ttl=3600)  # Cache up to 1000 items for 1 hour


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
    """
    Get appropriate string matching function based on match type.

    Args:
        match_type: The type of match to perform ('contains', 'startswith', or 'exact').

    Returns:
        Callable[[str, str], bool]: takes two strings and returns a boolean.
    """
    matchers = {
        "contains": lambda field, q: q in field.lower(),
        "startswith": lambda field, q: field.lower().startswith(q),
        "exact": lambda field, q: field.lower() == q,
    }

    return matchers.get(match_type, matchers["contains"])


@cached(CACHE)
def get_unique_values(field: str) -> list[str]:
    """Get unique values for a given field across all zip codes."""
    return sorted(
        {
            value
            for value in (getattr(zip_code, field) for zip_code in load_data().values())
            if value
        }
    )


# Derived lookup functions
@cached(CACHE)
def find_by_zip(zip_code: str) -> ZipCode | None:
    """Get location information by zip code."""
    return load_data().get(zip_code)


@cached(CACHE)
def find_by_city_municipality(city_municipality: str) -> list[dict[str, str]]:
    """Get zip codes, province and region by city/municipality name."""
    return [
        {
            "zip_code": zip_code.code,
            "province": zip_code.province,
            "region": zip_code.region,
        }
        for zip_code in load_data().values()
        if zip_code.city_municipality.lower() == city_municipality.lower()
    ]


# Search and filter functions
@cached(CACHE)
def search(
    query: str,
    fields: Sequence[str] = DEFAULT_SEARCH_FIELDS,
    match_type: str = "contains",
) -> tuple[ZipCode, ...]:
    """
    Search for zip codes based on query and criteria.

    Args:
        query: Search term
        fields: Fields to search in (default: city, province, region)
        match_type: Type of match to perform (default: contains)

    Example:
        >>> results = search("Manila", fields=("city_municipality",),
        ...                  match_type="exact")
        >>> [result.code for result in results]
        ['1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008']
    """
    query = query.lower()
    match_func = get_match_function(match_type)

    return tuple(
        zip_code
        for zip_code in load_data().values()
        if any(match_func(getattr(zip_code, field), query) for field in fields)
    )


# Getter functions for hierarchical data
def get_regions() -> list[str]:
    """
    Get all unique regions in the Philippines.

    Returns:
        list[str]: A list of all unique regions.

    Example:
        >>> regions = get_regions()
        >>> print(regions[:2])
        ['CAR (Cordillera Administrative Region)', 'NCR (National Capital Region)']
    """
    return get_unique_values("region")


def get_provinces(region: str) -> list[str]:
    """
    Get all provinces within a specific region.

    Args:
        region: The region to get provinces for.

    Returns:
        list[str]: A list of provinces in the specified region.

    Example:
        >>> provinces = get_provinces("Region 4A (CALABARZON)")
        >>> print(provinces[:2])
        ['Batangas', 'Cavite']
    """
    return sorted(
        {
            zip_code.province
            for zip_code in load_data().values()
            if zip_code.region == region
        }
    )


def get_cities_municipalities(province: str) -> list[str]:
    """
    Get all cities and municipalities within a specific province.

    Args:
        province: The province to get cities/municipalities for.

    Returns:
        list[str]: A list of cities/municipalities in the specified province.

    Example:
        >>> cities_municipalities = get_cities_municipalities("Cavite")
        >>> print(cities_municipalities[:2])
        ['Alfonso', 'Amadeo']
    """
    return sorted(
        {
            zip_code.city_municipality
            for zip_code in load_data().values()
            if zip_code.province == province
        }
    )


# TODO: Implement typer CLI
