"""Philippines zip codes package.

This package provides functionality to work with Philippines zip codes,
including searching, retrieving information, and listing regions, provinces, and cities.
"""

from .phzipcodes import PhZipCodes, ZipCode

_ph_zip_codes = PhZipCodes()


def get_by_zip(zip_code: str) -> ZipCode | None:
    """Retrieve zip code information by zip code."""
    return _ph_zip_codes.get_by_zip(zip_code)


def search(
    query: str, fields: list[str] | None = None, match_type: str = "contains"
) -> list[ZipCode]:
    """Search for zip codes based on query and criteria."""
    return _ph_zip_codes.search(query, fields, match_type)


def get_regions() -> list[str]:
    """Get all unique regions."""
    return _ph_zip_codes.get_regions()


def get_provinces(region: str) -> list[str]:
    """Get all provinces in a specific region."""
    return _ph_zip_codes.get_provinces(region)


def get_cities_municipalities(province: str) -> list[str]:
    """Get all cities/municipalities in a specific province."""
    return _ph_zip_codes.get_cities_municipalities(province)


__all__ = [
    "PhZipCodes",
    "ZipCode",
    "get_by_zip",
    "search",
    "get_regions",
    "get_provinces",
    "get_cities_municipalities",
]
