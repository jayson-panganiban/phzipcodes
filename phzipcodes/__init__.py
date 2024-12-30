"""
Philippines zip codes package.

This package provides functionality to work with Philippines zip codes,
including searching, retrieving information, and listing regions,
provinces, and cities/municipalities.
"""

from .phzipcodes import (
    DEFAULT_SEARCH_FIELDS,
    Cities,
    MatchFunction,
    MatchType,
    Provinces,
    Regions,
    SearchResults,
    ZipCode,
    ZipResult,
    find_by_city_municipality,
    find_by_zip,
    get_cities_municipalities,
    get_match_function,
    get_provinces,
    get_regions,
    load_data,
    search,
)

__all__ = [
    # Core types
    "ZipCode",
    "ZipResult",
    "SearchResults",
    "Cities",
    "Provinces",
    "Regions",
    # Search functionality
    "MatchType",
    "MatchFunction",
    "DEFAULT_SEARCH_FIELDS",
    # Core functions
    "find_by_zip",
    "find_by_city_municipality",
    "search",
    "get_regions",
    "get_provinces",
    "get_cities_municipalities",
    "get_match_function",
    "load_data",
]
