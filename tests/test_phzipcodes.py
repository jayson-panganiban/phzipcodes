from collections.abc import Callable

import pytest

from phzipcodes import (
    Cities,
    MatchType,
    Provinces,
    Regions,
    SearchResults,
    ZipCode,
    ZipResult,
    find_by_city_municipality,
    find_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)

# Test data
valid_zip = "4114"
test_city = "Dasmariñas"
test_province = "Cavite"
test_region = "Region 4A (CALABARZON)"


class TestCoreFunctions:
    def test_find_by_zip_valid(self) -> None:
        result: ZipResult = find_by_zip(valid_zip)
        assert isinstance(result, ZipCode)
        assert result.city_municipality == test_city
        assert result.province == test_province
        assert result.region == test_region

    def test_find_by_zip_invalid(self) -> None:
        assert find_by_zip("99999") is None

    def test_find_by_city_municipality(self) -> None:
        results = find_by_city_municipality(test_city)
        assert isinstance(results, list) and results
        assert all(isinstance(r, dict) for r in results)
        assert all(
            all(key in r for key in ("zip_code", "province", "region")) for r in results
        )


class TestSearchFunctionality:
    @pytest.mark.parametrize(
        "query,match_type,expected_check",
        [
            (test_city, MatchType.EXACT, lambda r, q: r.city_municipality == q),
            ("Maka", MatchType.CONTAINS, lambda r, q: q in r.city_municipality),
            (
                "San",
                MatchType.STARTSWITH,
                lambda r, q: r.city_municipality.startswith(q),
            ),
        ],
    )
    def test_search_with_different_match_types(
        self,
        query: str,
        match_type: MatchType,
        expected_check: Callable[[ZipCode, str], bool],
    ) -> None:
        results: SearchResults = search(query, match_type=match_type)
        assert isinstance(results, tuple) and results
        assert all(isinstance(r, ZipCode) and expected_check(r, query) for r in results)

    def test_search_basic(self) -> None:
        results: SearchResults = search("Manila")
        assert isinstance(results, tuple)
        assert all(isinstance(r, ZipCode) for r in results)

    def test_search_with_fields(self) -> None:
        fields = ("city_municipality", "province")
        assert isinstance(search("test", fields=fields), tuple)


class TestGeographicHierarchy:
    def test_get_regions(self) -> None:
        regions: Regions = get_regions()
        assert isinstance(regions, list) and regions
        assert "NCR (National Capital Region)" in regions

    def test_get_provinces(self) -> None:
        provinces: Provinces = get_provinces("NCR (National Capital Region)")
        assert isinstance(provinces, list)
        assert all(isinstance(p, str) for p in provinces)

    def test_get_cities_municipalities(self) -> None:
        cities: Cities = get_cities_municipalities("Metro Manila")
        assert isinstance(cities, list) and cities
        assert "Quezon City" in cities


class TestErrorAndEdgeCases:
    def test_invalid_match_type(self) -> None:
        with pytest.raises(ValueError):
            search("Manila", match_type="invalid_type")

    def test_case_insensitivity(self) -> None:
        query = "manila"
        assert search(query) == search(query.upper())
