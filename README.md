# phzipcodes

Philippines zip codes package

## API Reference

### `search(query: str, fields: List[str] = None, match_type: str = "contains") -> List[ZipCode]`

Search for zip codes based on query and criteria.

- **Parameters:**
  - `query`: str - The search query
  - `fields`: List[str] (optional) - List of fields to search in (default: ["city", "province", "region"])
  - `match_type`: str (optional) - Type of match to perform (default: "contains")
- **Returns:** List[ZipCode] - List of matching ZipCode objects

### `get_by_zip(zip_code: str) -> Optional[ZipCode]`

Retrieve zip code information by zip code.

- **Parameters:**
  - `zip_code`: str - The zip code to look up
- **Returns:** Optional[ZipCode] - ZipCode object if found, None otherwise

### `get_regions() -> List[str]`

Get all unique regions.

- **Returns:** List[str] - List of all unique regions

### `get_provinces(region: str) -> List[str]`

Get all provinces in a specific region.

- **Parameters:**
  - `region`: str - The region to get provinces for
- **Returns:** List[str] - List of provinces in the specified region

### `get_cities_municipalities(province: str) -> List[str]`

Get all cities/municipalities in a specific province.

- **Parameters:**
  - `province`: str - The province to get cities for
- **Returns:** List[str] - List of cities in the specified province

## Data Structure

The package uses a `ZipCode` class with the following attributes:

```python
class ZipCode(BaseModel):
    region: str
    province: str
    city_municipality: str
    code: str
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
2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Run Tests**
   ```bash
   poetry run pytest
   ```
