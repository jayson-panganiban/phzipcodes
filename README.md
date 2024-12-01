# phzipcodes

Philippines zip codes package

## Installation

Ensure you have Python 3.11 or higher installed.

Install the package using pip:

```bash
pip install phzipcodes
```

## Usage

```python
import phzipcodes

# Get zip code information by zip code
zip_info = phzipcodes.find_by_zip("4117")
print(zip_info)
# Output: ZipCode(code='4117', city_municipality='Gen. Mariano Alvarez', province='Cavite', region='Region 4A (CALABARZON)')

# Get location details by city/municipality
location_details = phzipcodes.find_by_city_municipality("Gen. Mariano Alvarez")
print(location_details)
# Output: [{'zip_code': '4117', 'province': 'Cavite', 'region': 'Region 4A (CALABARZON)'}]

# Basic search for zip codes
results = phzipcodes.search("Manila")
for result in results:
    print(result)

# Advanced search with specific field and exact matching
results = phzipcodes.search(
    "Dasmariñas", 
    fields=["city_municipality"], 
    match_type="exact"
)
print(results)
# Output: (ZipCode(code='4114', city_municipality='Dasmariñas', province='Cavite', region='Region 4A (CALABARZON)'),)

# Get all unique regions in the Philippines
regions = phzipcodes.get_regions()
print(regions[:2])
# Output: ['CAR (Cordillera Administrative Region)', 'NCR (National Capital Region)']

# Get all provinces in a specific region
provinces = phzipcodes.get_provinces("Region 4A (CALABARZON)")
print(provinces[:2])
# Output: ['Batangas', 'Cavite']

# Get all cities/municipalities in a specific province
cities_municipalities = phzipcodes.get_cities_municipalities("Cavite")
print(cities_municipalities[:2])
# Output: ['Alfonso', 'Amadeo']
```

## API Reference

### `find_by_zip(zip_code: str) -> ZipCode | None`

Get location information by zip code.

- **Parameters:**
  - `zip_code`: str - The zip code to look up
- **Returns:** ZipCode | None - ZipCode object if found, None otherwise

### `find_by_city_municipality(city_municipality: str) -> list[dict[str, str]]`

Get zip codes, province and region by city/municipality name.

- **Parameters:**
  - `city_municipality`: str - Name of the city/municipality to look up
- **Returns**: list[dict[str, str]] - List of dictionaries containing zip_code, province and region

### `search(query: str, fields: Sequence[str] = DEFAULT_SEARCH_FIELDS, match_type: str = MatchType.CONTAINS) -> tuple[ZipCode, ...]`

Search for zip codes based on query and criteria.

- **Parameters:**
  - `query`: str - The search query
  - `fields`: Sequence[str] (optional) - Fields to search in (default: city_municipality, province, region)
  - `match_type`: str (optional) - Type of match to perform (default: "contains")
- **Returns:** tuple[ZipCode, ...] - Tuple of matching ZipCode objects

### `get_regions() -> list[str]`

Get all unique regions in the Philippines.

- **Returns:** list[str] - A list of all unique regions

### `get_provinces(region: str) -> list[str]`

Get all provinces within a specific region.

- **Parameters:**
  - `region`: str - Region to get provinces for
- **Returns:** list[str] - A list of provinces in the specified region

### `get_cities_municipalities(province: str) -> list[str]`

Get all cities and municipalities within a specific province.

- **Parameters:**
  - `province`: str - Province to get cities/municipalities for
- **Returns:** list[str] - A list of cities/municipalities in the specified province


## Data Structure

The package uses a `ZipCode` class with the following attributes:

```python
class ZipCode(BaseModel):
    code: str
    city_municipality: str
    province: str
    region: str
```

## Data Source and Collection

The zip code data used in this package is sourced from [PHLPost](https://phlpost.gov.ph/) (Philippine Postal Corporation), the official postal service of the Philippines.

To keep data current, use custom scraper tool (`scraper.py`).

## Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/jayson-panganiban/phzipcodes.git
   cd phzipcodes
   ```

2. **Install Poetry if you haven't already**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**

   ```bash
   poetry install
   ```

   Or using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests**

   ```bash
   poetry run pytest
   ```

5. **Run linter**

   ```bash
   poetry run ruff check .
   ```

6. **Run formatter**

   ```bash
   poetry run ruff format .
   ```

7. **Run type checker**

   ```bash
   poetry run mypy phzipcodes
   ```

8. **To update the zip codes data, run the scraper**

   ```bash
   poetry run python phzipcodes/scraper.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
