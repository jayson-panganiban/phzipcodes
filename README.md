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

# Get zip code information
zip_info = phzipcodes.find_by_zip("4117")
print(zip_info)
# Output: ZipCode(code='4117', city_municipality='Gen. Mariano Alvarez', province='Cavite', region='Region 4A (CALABARZON)')

# Get location details by city/municipality
location_details = phzipcodes.find_by_city_municipality("Gen. Mariano Alvarez")
print(location_details)
# Output: [{'zip_code': '4117', 'province': 'Cavite', 'region': 'Region 4A (CALABARZON)'}]

# Search with specific match type
results = phzipcodes.search("Manila", match_type=phzipcodes.MatchType.CONTAINS)
for result in results:
    print(result)

# Search with custom fields and exact matching
results = phzipcodes.search(
    "Dasmariñas", 
    fields=["city_municipality"], 
    match_type=phzipcodes.MatchType.EXACT
)
print(results)

# Get geographic data
regions = phzipcodes.get_regions()
provinces = phzipcodes.get_provinces("Region 4A (CALABARZON)")
cities = phzipcodes.get_cities_municipalities("Cavite")

```

## API Reference

### Types

#### `MatchType`
```python
class MatchType(str, Enum):
    CONTAINS    # Match if query exists within field
    STARTSWITH  # Match if field starts with query
    EXACT       # Match if field equals query exactly
```
#### `ZipCode`
```python
class ZipCode(BaseModel):
    code: str
    city_municipality: str
    province: str
    region: str
```
### Functions
### `find_by_zip`
```python
def find_by_zip(zip_code: str) -> ZipResult
```
Get location information by zip code.
- **Parameters:**
  - `zip_code`: Zip code to search for.
- **Returns:** 
  - `ZipCode | None` - ZipCode object or None if not found.


### `find_by_city_municipality`
```python
def find_by_city_municipality(city_municipality: str) -> CityMunicipalityResults
```
Get zip codes, province and region by city/municipality name.

- **Parameters:**
  - `city_municipality`: city or municipality name.
- **Returns**: 
  - `CityMunicipalityResults`: List of dictionaries with zip code, province, and region.

### `search`
```python
def search(
    query: str,
    fields: Sequence[str] = DEFAULT_SEARCH_FIELDS,
    match_type: MatchType = MatchType.CONTAINS
) -> SearchResults
```
Search for zip codes based on query and criteria.
- **Parameters:**
  - `query`: Search term
  - `fields`: Fields to search in (default: city_municipality, province, region)
  - `match_type`: Type of match to perform (default: CONTAINS)
- **Returns:** 
  - `SearchResults`: A tuple of ZipCode objects matching the query.

### `get_regions`
```python
def get_regions() -> Regions
```
Get all unique regions in the Philippines.
- **Returns:** `Regions`: A list of unique regions.

### `get_provinces`
```python
def get_provinces(region: str) -> Provinces
```
Get all provinces within a specific region.

- **Parameters:**
  - `region`: str - Region to get provinces for
- **Returns:**
  - `Provinces`: A list of provinces in the specified region

### `get_cities_municipalities`
```python
def get_cities_municipalities(province: str) -> CitiesMunicipalities
```
Get all cities/municipalities within a specific province.
- **Parameters:**
  - `province`: str - Province to get cities/municipalities for
- **Returns:**
  - `CitiesMunicipalities`: A list of cities/municipalities in the specified province

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
