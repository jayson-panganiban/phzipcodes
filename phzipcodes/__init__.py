"""
Philippines zip codes package.

This package provides functionality to work with Philippines zip codes,
including searching, retrieving information, and listing regions,
provinces, and cities/municipalities.
"""

from .phzipcodes import (
    ZipCode,
    find_by_city_municipality,
    find_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)

__all__ = [
    "ZipCode",
    "find_by_zip",
    "find_by_city_municipality",
    "search",
    "get_regions",
    "get_provinces",
    "get_cities_municipalities",
]

__version__ = "0.1.5"
