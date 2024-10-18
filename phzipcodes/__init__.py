"""Philippines zip codes package.

This package provides functionality to work with Philippines zip codes,
including searching, retrieving information, and listing regions, provinces, and cities.
"""

from .phzipcodes import (
    ZipCode,
    get_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)

__all__ = [
    "ZipCode",
    "get_by_zip",
    "search",
    "get_regions",
    "get_provinces",
    "get_cities_municipalities",
]

__version__ = "0.0.3"
