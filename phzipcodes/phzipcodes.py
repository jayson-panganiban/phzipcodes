import json
from functools import cache, lru_cache
from pathlib import Path
from typing import Callable

from pydantic import BaseModel

# Constants
DATA_FILE_PATH = Path(__file__).parent / "data" / "ph_zip_codes.json"
DEFAULT_SEARCH_FIELDS = ("city_municipality", "province", "region")


class ZipCode(BaseModel):
    code: str
    city_municipality: str
    province: str
    region: str


@lru_cache(maxsize=1)
def load_data() -> dict[str, ZipCode]:
    """Load zip code data from JSON file and return as a dictionary."""
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


@cache
def get_by_zip(zip_code: str) -> ZipCode | None:
    """Retrieve zip code information by zip code."""
    return load_data().get(zip_code)


def get_match_function(match_type: str) -> Callable[[str, str], bool]:
    """Return the appropriate match function based on the match type."""
    return {
        "contains": lambda field, q: q in field.lower(),
        "startswith": lambda field, q: field.lower().startswith(q),
        "exact": lambda field, q: field.lower() == q,
    }.get(match_type, lambda field, q: q in field.lower())


@cache
def search(
    query: str,
    fields: tuple[str, ...] = DEFAULT_SEARCH_FIELDS,
    match_type: str = "contains",
) -> tuple[ZipCode, ...]:
    """Search for zip codes based on query and criteria."""
    lowered_query = query.lower()
    match_func = get_match_function(match_type)
    return tuple(
        zip_code
        for zip_code in load_data().values()
        if any(match_func(getattr(zip_code, field), lowered_query) for field in fields)
    )


def get_unique_values(attribute: str) -> list[str]:
    """Get unique values for a given attribute from all zip codes."""
    return list({getattr(zip_code, attribute) for zip_code in load_data().values()})


def get_regions() -> list[str]:
    """Get all unique regions."""
    return get_unique_values("region")


def get_provinces(region: str) -> list[str]:
    """Get all provinces in a specific region."""
    return list(
        {
            zip_code.province
            for zip_code in load_data().values()
            if zip_code.region == region
        }
    )


def get_cities_municipalities(province: str) -> list[str]:
    """Get all cities/municipalities in a specific province."""
    return list(
        {
            zip_code.city_municipality
            for zip_code in load_data().values()
            if zip_code.province == province
        }
    )


# TODO: Implement typer CLI
