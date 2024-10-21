import json
from functools import lru_cache
from pathlib import Path
from typing import Callable

from cachetools import TTLCache, cached
from pydantic import BaseModel

# Constants
DATA_FILE_PATH = Path(__file__).parent / "data" / "ph_zip_codes.json"
DEFAULT_SEARCH_FIELDS = ("city_municipality", "province", "region")

# Cache configuration
cache: TTLCache = TTLCache(maxsize=1000, ttl=3600)  # Cache up to 1000 items for 1 hour


class ZipCode(BaseModel):
    """Represents a zip code entry with associated location information."""

    code: str
    city_municipality: str
    province: str
    region: str


@lru_cache(maxsize=1)
def load_data() -> dict[str, ZipCode]:
    """
    Load and cache zip code data from JSON file.

    Returns:
        dict[str, ZipCode]: A dictionary mapping zip codes to ZipCode objects.
    """
    with DATA_FILE_PATH.open() as f:
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


@cached(cache)
def get_by_zip(zip_code: str) -> ZipCode | None:
    """Retrieve zip code information by code. Returns None if not found."""
    return load_data().get(zip_code)


def get_match_function(match_type: str) -> Callable[[str, str], bool]:
    """
    Return a match function based on type.

    Args:
        match_type: The type of match to perform ('contains', 'startswith', or 'exact').

    Returns:
        Callable[[str, str], bool]: takes two strings and returns a boolean.
    """
    return {
        "contains": lambda field, q: q in field.lower(),
        "startswith": lambda field, q: field.lower().startswith(q),
        "exact": lambda field, q: field.lower() == q,
    }.get(match_type, lambda field, q: q in field.lower())


@cached(cache)
def search(
    query: str,
    fields: tuple[str, ...] = DEFAULT_SEARCH_FIELDS,
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
    lowered_query = query.lower()
    match_func = get_match_function(match_type)
    return tuple(
        zip_code
        for zip_code in load_data().values()
        if any(match_func(getattr(zip_code, field), lowered_query) for field in fields)
    )


@cached(cache)
def get_unique_values(attribute: str) -> list[str]:
    """
    Get unique values for a given attribute across all zip codes.

    Args:
        attribute: The attribute to get unique values for.

    Returns:
        list[str]: A list of unique values for the given attribute.

    Example:
        >>> regions = get_unique_values("region")
        >>> print(regions[:3])
        ['NCR', 'CAR', 'Region I']
    """
    return list({getattr(zip_code, attribute) for zip_code in load_data().values()})


def get_regions() -> list[str]:
    """
    Retrieve all unique regions in the Philippines.

    Returns:
        list[str]: A list of all unique regions.

    Example:
        >>> regions = get_regions()
        >>> print(regions[1:3])
        ['Region 1 (Ilocos Region)', 'Region 8 (Eastern Visayas)']
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
        >>> provinces = get_provinces("NCR (National Capital Region)")
        >>> print(provinces)
        ['Metro Manila']
    """
    return list(
        {
            zip_code.province
            for zip_code in load_data().values()
            if zip_code.region == region
        }
    )


def get_cities_municipalities(province: str) -> list[str]:
    """
    Retrieve all cities/municipalities within a specific province.

    Args:
        province: The province to get cities/municipalities for.

    Returns:
        list[str]: A list of cities/municipalities in the specified province.

    Example:
        >>> cities = get_cities_municipalities("Metro Manila")
        >>> print(cities[:3])
        ['Rembo (West)', 'Gatchalian Subdivision', 'Guadalupe Viejo (Inc. Palm Vil)']
    """
    return list(
        {
            zip_code.city_municipality
            for zip_code in load_data().values()
            if zip_code.province == province
        }
    )


# TODO: Implement typer CLI
