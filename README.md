# phzipcodes

Philippines zip codes package

## Installation

Ensure you have Python 3.9 or higher installed.

Install the package using pip:

```bash
pip install phzipcodes
```

## Usage

```python
import phzipcodes

# Get zip code information by zip code
zip_info = phzipcodes.get_by_zip("1000")
print(zip_info)
# Output: ZipCode(code='1000', city_municipality='Manila', province='Metro Manila', region='NCR')

# Search for zip codes
results = phzipcodes.search("Manila")
for result in results:
    print(result)

# Advanced search options
results = phzipcodes.search("Manila", fields=("city_municipality",), match_type="exact")
print([result.code for result in results])
# Output: ['1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008']

# Get all unique regions
regions = phzipcodes.get_regions()
print(regions[:3])
# Output: ['NCR', 'CAR', 'Region I']

# Get all provinces in a specific region
provinces = phzipcodes.get_provinces("NCR")
print(provinces)
# Output: ['Metro Manila']

# Get all cities/municipalities in a specific province
cities = phzipcodes.get_cities_municipalities("Metro Manila")
print(cities[:3])
# Output: ['Manila', 'Quezon City', 'Caloocan']

```

## API Reference

### `search(query: str, fields: tuple[str, ...] = DEFAULT_SEARCH_FIELDS, match_type: str = "contains") -> tuple[ZipCode, ...]`

Search for zip codes based on query and criteria.

- **Parameters:**
  - `query`: str - The search query
  - `fields`: tuple[str, ...] (optional) - Fields to search in (default: city, province, region)
  - `match_type`: str (optional) - Type of match to perform (default: "contains")
- **Returns:** tuple[ZipCode, ...] - Tuple of matching ZipCode objects

### `get_by_zip(zip_code: str) -> ZipCode | None`

Retrieve zip code information by zip code.

- **Parameters:**
  - `zip_code`: str - The zip code to look up
- **Returns:** ZipCode | None - ZipCode object if found, None otherwise

### `get_regions() -> list[str]`

Get all unique regions.

- **Returns:** list[str] - List of all unique regions

### `get_provinces(region: str) -> List[str]`

Get all provinces in a specific region.

- **Parameters:**
  - `region`: str - The region to get provinces for
- **Returns:** list[str] - List of provinces in the specified region

### `get_cities_municipalities(province: str) -> List[str]`

Get all cities/municipalities in a specific province.

- **Parameters:**
  - `province`: str - The province to get cities for
- **Returns:** list[str] - List of cities/municipalities in the specified province

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
