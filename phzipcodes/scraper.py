import asyncio
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import aiohttp
from bs4 import BeautifulSoup, Tag
from toolz import curry, groupby, pipe  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ZipCode:
    region: str
    province: str
    city_municipality: str
    zip_code: str


BASE_URL = "https://phlpost.gov.ph/zip-code-locator/"


async def fetch_page(url: str) -> str:
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        return await response.text()


def parse_html(html: str) -> list[list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None or not isinstance(table, Tag):
        return []
    return [
        [td.text.strip() for td in row.find_all("td")]
        for row in table.find_all("tr")[1:]
    ]


def row_to_zipcode(row: list[str]) -> ZipCode:
    return ZipCode(
        region=row[0], province=row[1], city_municipality=row[2], zip_code=row[3]
    )


@curry
def map_func(func: Callable, data: list) -> list:
    return list(map(func, data))


def organize_data(zip_codes: list[ZipCode]) -> dict:
    by_region = groupby(lambda zc: zc.region, zip_codes)
    return {
        region: {
            province: {
                city: [zc.zip_code for zc in city_codes]
                for city, city_codes in groupby(
                    lambda zc: zc.city_municipality, province_codes
                ).items()
            }
            for province, province_codes in groupby(
                lambda zc: zc.province, region_codes
            ).items()
        }
        for region, region_codes in by_region.items()
    }


def save_to_json(data: dict, filepath: str | Path | None = None):
    if filepath is None:
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        filepath = data_dir / "ph_zip_codes.json"
    else:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Data saved to {filepath}")


async def scrape_zip_codes() -> dict:
    html = await fetch_page(BASE_URL)
    return pipe(html, parse_html, map_func(row_to_zipcode), organize_data)


async def main(output_path: str | Path | None = None):
    zip_codes = await scrape_zip_codes()
    save_to_json(zip_codes, output_path)
    logger.info("Scraping completed.")


if __name__ == "__main__":
    asyncio.run(main())

# TODO: Make this a CLI tool
