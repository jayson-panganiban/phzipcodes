import pytest

from phzipcodes import (
    find_by_city_municipality,
    find_by_zip,
    get_cities_municipalities,
    get_provinces,
    get_regions,
    search,
)


@pytest.fixture
def valid_zip_code():
    return "4114"


@pytest.fixture
def valid_region():
    return "Region 4A (CALABARZON)"


@pytest.fixture
def valid_province():
    return "Cavite"


@pytest.fixture
def valid_city_municipality():
    return "Dasmariñas"


class TestFindByZip:
    def test_valid_zip(self, valid_zip_code):
        zip_code = find_by_zip(valid_zip_code)
        assert zip_code is not None
        assert zip_code.code == valid_zip_code
        assert zip_code.city_municipality == "Dasmariñas"
        assert zip_code.province == "Cavite"
        assert zip_code.region == "Region 4A (CALABARZON)"

    def test_nonexistent_zip(self):
        assert find_by_zip("99999") is None


class TestFindByCityMunicipality:
    def test_valid_city_municipality(self, valid_city_municipality):
        results = find_by_city_municipality(valid_city_municipality)
        assert results
        assert all(
            isinstance(result, dict)
            and "zip_code" in result
            and "province" in result
            and "region" in result
            for result in results
        )
        expected = {
            "zip_code": "4114",
            "province": "Cavite",
            "region": "Region 4A (CALABARZON)",
        }
        assert expected in results

    def test_nonexistent_city_municipality(self):
        assert not find_by_city_municipality("NonexistentPlace")


class TestSearch:
    @pytest.mark.parametrize(
        "query, expected_substring",
        [
            ("Dasmariñas", "Dasmariñas"),
            ("dasmariñas", "Dasmariñas"),
            ("DASMARIÑAS", "Dasmariñas"),
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
            ("Dasmariñas", "exact", "city_municipality", "Dasmariñas"),
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
        results = search("Region 4A (CALABARZON)", fields=("region",))
        assert results
        assert all(result.region == "Region 4A (CALABARZON)" for result in results)

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
    assert "Region 4A (CALABARZON)" in regions


def test_get_provinces(valid_region):
    provinces = get_provinces(valid_region)
    assert "Cavite" in provinces


def test_get_cities_municipalities(valid_province):
    cities_municipalities = get_cities_municipalities(valid_province)
    assert "Dasmariñas Resettlement Area" in cities_municipalities
    assert "Gen. Mariano Alvarez" in cities_municipalities


def test_nonexistent_region():
    assert not get_provinces("Nonexistent Region")


def test_nonexistent_province():
    assert not get_cities_municipalities("Nonexistent Province")
