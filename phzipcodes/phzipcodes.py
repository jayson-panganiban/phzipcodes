import json
from functools import cache
from pathlib import Path
from typing import Callable

from pydantic import BaseModel


class ZipCode(BaseModel):
    code: str
    city_municipality: str
    province: str
    region: str


class PhZipCodes:
    def __init__(self) -> None:
        self.data: dict[str, ZipCode] = self._load_data()
        self._get_by_zip_cache = cache(self._get_by_zip_uncached)
        self._cached_search = cache(self._cached_search_uncached)

    def _load_data(self) -> dict[str, ZipCode]:
        data_file = Path(__file__).parent / "data" / "ph_zip_codes.json"
        with data_file.open() as f:
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

    def get_by_zip(self, zip_code: str) -> ZipCode | None:
        return self._get_by_zip_cache(zip_code)

    def _get_by_zip_uncached(self, zip_code: str) -> ZipCode | None:
        return self.data.get(zip_code)

    def _cached_search_uncached(
        self, query: str, fields: tuple[str, ...], match_type: str
    ) -> tuple[ZipCode, ...]:
        query = query.lower()
        match_func: Callable[[str, str], bool] = {
            "contains": lambda field, q: q in field.lower(),
            "startswith": lambda field, q: field.lower().startswith(q),
            "exact": lambda field, q: field.lower() == q,
        }.get(match_type, lambda field, q: q in field.lower())
        return tuple(
            zip_code
            for zip_code in self.data.values()
            if any(match_func(getattr(zip_code, field), query) for field in fields)
        )

    def search(
        self,
        query: str,
        fields: list[str] | None = None,
        match_type: str = "contains",
    ) -> list[ZipCode]:
        filtered_fields = tuple(fields or ["city_municipality", "province", "region"])
        return list(self._cached_search(query, filtered_fields, match_type))

    def get_regions(self) -> list[str]:
        return list({zip_code.region for zip_code in self.data.values()})

    def get_provinces(self, region: str) -> list[str]:
        return list(
            {
                zip_code.province
                for zip_code in self.data.values()
                if zip_code.region == region
            }
        )

    def get_cities_municipalities(self, province: str) -> list[str]:
        return list(
            {
                zip_code.city_municipality
                for zip_code in self.data.values()
                if zip_code.province == province
            }
        )


# TODO: Implement typer CLI
