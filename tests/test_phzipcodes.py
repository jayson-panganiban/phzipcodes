from typing import Callable, Final

import pytest

from phzipcodes import (
    Cities,
    MatchType,
    Provinces,
    Regions,
    SearchResults,
    ZipCode,
    find_by_city_municipality,
    find_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)


class TestData:
    GMA: Final[ZipCode] = ZipCode(
        code="4117",
        city_municipality="Gen. Mariano Alvarez",
        province="Cavite",
        region="Region 4A (CALABARZON)",
    )


@pytest.fixture
def zipcode() -> ZipCode:
    return TestData.GMA


class TestZipCodeLookup:
    def test_find_valid_zip(self, zipcode: ZipCode) -> None:
        result = find_by_zip(zipcode.code)
        assert isinstance(result, ZipCode)
        assert result.city_municipality == zipcode.city_municipality
        assert result.province == zipcode.province
        assert result.region == zipcode.region

    def test_find_invalid_zip(self) -> None:
        assert find_by_zip("69420") is None

    def test_find_by_city(self, zipcode: ZipCode) -> None:
        results = find_by_city_municipality(zipcode.city_municipality)
        assert results and all(isinstance(r, dict) for r in results)
        assert all({"zip_code", "province", "region"} <= r.keys() for r in results)


class TestSearchFunctionality:
    @pytest.mark.parametrize(
        "query,match_type,validator",
        [
            (
                "Dasmariñas",
                MatchType.EXACT,
                lambda r, q: r.city_municipality.lower() == q.lower(),
            ),
            ("Sta.", MatchType.CONTAINS, lambda r, q: q in r.city_municipality),
            (
                "San",
                MatchType.STARTSWITH,
                lambda r, q: r.city_municipality.lower().startswith(q.lower()),
            ),
        ],
    )
    def test_search_with_match_types(
        self,
        query: str,
        match_type: MatchType,
        validator: Callable[[ZipCode, str], bool],
    ) -> None:
        results: SearchResults = search(query, match_type=match_type)
        assert results and all(isinstance(r, ZipCode) for r in results)
        assert all(validator(r, query) for r in results)

    def test_search_with_custom_fields(self) -> None:
        fields = ("city_municipality", "province")
        results = search("Cavite", fields=fields, match_type=MatchType.CONTAINS)
        assert results and all(isinstance(r, ZipCode) for r in results)
        assert any("Cavite" in r.province for r in results)

    def test_search_caching(self) -> None:
        query = "Mahatao"
        first_results = search(query)
        second_results = search(query)
        assert first_results is second_results


class TestGeographicData:
    def test_regions_list(self, zipcode: ZipCode) -> None:
        regions: Regions = get_regions()
        assert regions and zipcode.region in regions

    def test_provinces_in_region(self, zipcode: ZipCode) -> None:
        provinces: Provinces = get_provinces(zipcode.region)
        assert provinces and zipcode.province in provinces

    def test_cities_in_province(self, zipcode: ZipCode) -> None:
        cities: Cities = get_cities_municipalities(zipcode.province)
        assert cities and zipcode.city_municipality in cities


class TestErrorHandling:
    def test_invalid_match_type(self) -> None:
        with pytest.raises(ValueError):
            search("Manila", match_type="invalid_type")

    def test_case_insensitive_search(self) -> None:
        query = "manila"
        assert search(query) == search(query.upper())
