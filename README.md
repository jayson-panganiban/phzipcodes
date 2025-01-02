# phzipcodes
[![PyPI version](https://badge.fury.io/py/phzipcodes.svg)](https://badge.fury.io/py/phzipcodes)

`phzipcodes` is a Python package for accessing and searching Philippine zip codes. It provides functionalities to find zip codes by city, search with specific match types, and retrieve regions and provinces. This package is designed to be simple and easy to use, making it a valuable tool for developers working with Philippine address data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Installation

Ensure you have Python 3.11 or higher installed.

Install the package using pip:

```bash
pip install phzipcodes
```

## Usage

```python
import phzipcodes
```


#### 1) Find by Zip Code
```python
zip_info = phzipcodes.find_by_zip("4117")
print(zip_info)
# Output (object): ZipCode(code='4117', city_municipality='Gen. Mariano Alvarez', province='Cavite', region='Region 4A (CALABARZON)')
```

#### 2) Find by City/Municipality
```python
location_info = phzipcodes.find_by_city_municipality("Gen. Mariano Alvarez")
print(location_details)
# Output (list): [{'zip_code': '4117', 'province': 'Cavite', 'region': 'Region 4A (CALABARZON)'}]
```

#### 3) Search with Match Type
```python
results = phzipcodes.search("Silang", match_type=phzipcodes.MatchType.CONTAINS)
# Check API Reference for MatchTypes (CONTAINS, STARTSWITH, EXACT)

# Output (tuple): 
# (ZipCode(code='1119', city_municipality='Bagong Silangan', province='Metro Manila', region='NCR (National Capital Region)'), 
# ZipCode(code='1428', city_municipality='Bagong Silang', province='Metro Manila', region='NCR (National Capital Region)'), 
# ZipCode(code='4118', city_municipality='Silang', province='Cavite', region='Region 4A (CALABARZON)'))
```

#### 4) Search in Specific Fields
```python
results = phzipcodes.search(
    "Dasmariñas", 
    fields=["city_municipality"], 
    match_type=phzipcodes.MatchType.EXACT
)
print(results)
```

#### 5) Get Regions, Provinces, Cities/Municipalities
```python
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
#### `find_by_zip()`
```python
def find_by_zip(zip_code: str) -> ZipResult
```
Get location information by zip code.
- **Parameters:**
  - `zip_code`: Zip code to search for.
- **Returns:** 
  - `ZipCode | None` - ZipCode object or None if not found.


#### `find_by_city_municipality()`
```python
def find_by_city_municipality(city_municipality: str) -> CityMunicipalityResults
```
Get zip codes, province and region by city/municipality name.

- **Parameters:**
  - `city_municipality`: city or municipality name.
- **Returns**: 
  - `CityMunicipalityResults`: List of dictionaries with zip code, province, and region.

#### `search()`
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

#### `get_regions()`
```python
def get_regions() -> Regions
```
Get all unique regions in the Philippines.
- **Returns:** `Regions`: A list of unique regions.

#### `get_provinces()`
```python
def get_provinces(region: str) -> Provinces
```
Get all provinces within a specific region.

- **Parameters:**
  - `region`: str - Region to get provinces for
- **Returns:**
  - `Provinces`: A list of provinces in the specified region

#### `get_cities_municipalities()`
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.