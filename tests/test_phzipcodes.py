import pytest

import phzipcodes


class TestGetByZip:
    def test_valid_zip(self):
        zip_code = phzipcodes.get_by_zip("1000")
        assert zip_code is not None
        assert zip_code.code == "1000"
        assert zip_code.city_municipality == "Ermita"
        assert zip_code.province == "Metro Manila"
        assert zip_code.region == "NCR (National Capital Region)"

    def test_nonexistent_zip(self):
        assert phzipcodes.get_by_zip("99999") is None


class TestSearch:
    def test_basic_search(self):
        results = phzipcodes.search("Manila")
        assert len(results) > 0
        assert all(
            "Manila" in result.city_municipality
            or "Manila" in result.province
            or "Manila" in result.region
            for result in results
        )

    def test_empty_query(self):
        results = phzipcodes.search("")
        assert len(results) > 0

    def test_case_insensitive(self):
        results_lower = phzipcodes.search("manila")
        results_upper = phzipcodes.search("MANILA")
        assert results_lower == results_upper

    def test_exact_match(self):
        results = phzipcodes.search("Ermita", match_type="exact")
        assert len(results) > 0
        assert all(result.city_municipality == "Ermita" for result in results)
        assert any(result.code == "1000" for result in results)

    def test_partial_match(self):
        results = phzipcodes.search("Maka", fields=["city_municipality"])
        assert len(results) > 0
        assert all("Maka" in result.city_municipality for result in results)

    def test_startswith(self):
        results = phzipcodes.search(
            "San", fields=["city_municipality"], match_type="startswith"
        )
        assert len(results) > 1
        assert all(result.city_municipality.startswith("San") for result in results)

    def test_search_with_province(self):
        results = phzipcodes.search("Pangasinan", fields=["province"])
        assert len(results) > 0
        assert all(result.province == "Pangasinan" for result in results)

    def test_search_with_region(self):
        results = phzipcodes.search("NCR", fields=["region"])
        assert len(results) > 0
        assert all(
            result.region == "NCR (National Capital Region)" for result in results
        )

    def test_nonexistent_place(self):
        results = phzipcodes.search("NonexistentPlace")
        assert len(results) == 0

    def test_invalid_field(self):
        with pytest.raises(AttributeError):
            phzipcodes.search("Test", fields=["invalid_field"])

    def test_invalid_match_type(self):
        results = phzipcodes.search("Test", match_type="invalid_type")
        assert len(results) == 0


class TestGetRegions:
    def test_get_regions(self):
        regions = phzipcodes.get_regions()
        assert len(regions) > 0
        assert "NCR (National Capital Region)" in regions


class TestGetProvinces:
    def test_get_provinces(self):
        provinces = phzipcodes.get_provinces("NCR (National Capital Region)")
        assert "Metro Manila" in provinces

    def test_nonexistent_region(self):
        provinces = phzipcodes.get_provinces("Nonexistent Region")
        assert len(provinces) == 0


class TestGetCitiesMunicipalities:
    def test_get_cities_municipalities(self):
        cities_municipalities = phzipcodes.get_cities_municipalities("Metro Manila")
        assert "Ermita" in cities_municipalities
        assert "Makati CPO (Inc, Buendia Up To)" in cities_municipalities

    def test_nonexistent_province(self):
        cities_municipalities = phzipcodes.get_cities_municipalities(
            "Nonexistent Province"
        )
        assert len(cities_municipalities) == 0
