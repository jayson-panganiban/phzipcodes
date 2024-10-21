import pytest

from phzipcodes import (
    get_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)


@pytest.fixture
def valid_zip_code():
    return "1000"


@pytest.fixture
def valid_region():
    return "NCR (National Capital Region)"


@pytest.fixture
def valid_province():
    return "Metro Manila"


class TestGetByZip:
    def test_valid_zip(self, valid_zip_code):
        zip_code = get_by_zip(valid_zip_code)
        assert zip_code is not None
        assert zip_code.code == valid_zip_code
        assert zip_code.city_municipality == "Ermita"
        assert zip_code.province == "Metro Manila"
        assert zip_code.region == "NCR (National Capital Region)"

    def test_nonexistent_zip(self):
        assert get_by_zip("99999") is None


class TestSearch:
    @pytest.mark.parametrize(
        "query, expected_substring",
        [
            ("Manila", "Manila"),
            ("manila", "Manila"),
            ("MANILA", "Manila"),
        ],
    )
    def test_basic_search(self, query, expected_substring):
        results = search(query=query)
        assert results
        assert all(
            expected_substring in result.city_municipality
            or expected_substring in result.province
            or expected_substring in result.region
            for result in results
        )

    def test_empty_query(self):
        results = search("")
        assert results

    @pytest.mark.parametrize(
        "query, match_type, expected_field, expected_value",
        [
            ("Ermita", "exact", "city_municipality", "Ermita"),
            ("Maka", "contains", "city_municipality", "Maka"),
            ("San", "startswith", "city_municipality", "San"),
        ],
    )
    def test_search_variations(self, query, match_type, expected_field, expected_value):
        results = search(query, fields=(expected_field,), match_type=match_type)
        assert results
        assert all(
            getattr(result, expected_field).startswith(expected_value)
            for result in results
        )

    def test_search_with_province(self):
        results = search("Pangasinan", fields=("province",))
        assert results
        assert all(result.province == "Pangasinan" for result in results)

    def test_search_with_region(self):
        results = search("NCR", fields=("region",))
        assert results
        assert all(
            result.region == "NCR (National Capital Region)" for result in results
        )

    def test_nonexistent_place(self):
        assert not search("NonexistentPlace")

    def test_invalid_field(self):
        with pytest.raises(AttributeError):
            search("Test", fields=("invalid_field",))

    def test_invalid_match_type(self):
        assert not search("Test", match_type="invalid_type")


def test_get_regions():
    regions = get_regions()
    assert regions
    assert "NCR (National Capital Region)" in regions


def test_get_provinces(valid_region):
    provinces = get_provinces(valid_region)
    assert "Metro Manila" in provinces


def test_get_cities_municipalities(valid_province):
    cities_municipalities = get_cities_municipalities(valid_province)
    assert "Ermita" in cities_municipalities
    assert "Makati CPO (Inc, Buendia Up To)" in cities_municipalities


def test_nonexistent_region():
    assert not get_provinces("Nonexistent Region")


def test_nonexistent_province():
    assert not get_cities_municipalities("Nonexistent Province")
