# API Reference

Technical documentation for Species Explorer modules and classes.

## Module: species_explorer

### Class: SpeciesExplorer

Main plugin class that handles QGIS integration.

```python
class SpeciesExplorer:
    """QGIS Plugin for exploring species occurrence data from GBIF."""
```

#### Methods

##### `__init__(iface: QgisInterface)`

Initialize the plugin.

**Parameters:**

- `iface`: QGIS interface object

##### `initGui()`

Initialize the plugin GUI elements. Creates toolbar action and menu entry.

##### `run()`

Show the Species Explorer dialog.

##### `unload()`

Clean up plugin resources when unloading.

---

## Module: species_explorer_dialog

### Class: SpeciesExplorerDialog

Main dialog class with UI logic.

```python
class SpeciesExplorerDialog(QDialog):
    """Dialog for Species Explorer plugin."""
```

#### Methods

##### `__init__(parent: QWidget = None)`

Initialize the dialog.

**Parameters:**

- `parent`: Parent widget

##### `find()`

Search GBIF for species matching the search text.

**Behavior:**

1. Gets search text from input field
2. Queries GBIF name_match endpoint
3. Populates results list with matching taxa

##### `select()`

Handle species selection from results list.

**Behavior:**

1. Gets selected species key
2. Queries GBIF for taxonomic details
3. Displays taxonomy information

##### `fetch()`

Fetch occurrence data for selected species.

**Behavior:**

1. Gets selected species key
2. Downloads occurrence records from GBIF
3. Creates point layer in QGIS
4. Applies default styling

##### `create_fields() -> QgsFields`

Create the attribute field schema for occurrence layers.

**Returns:**

`QgsFields` object with defined attributes

**Fields Created:**

| Name | Type | Description |
|------|------|-------------|
| gbifID | LongLong | GBIF record identifier |
| scientificName | String | Full scientific name |
| decimalLatitude | Double | Latitude coordinate |
| decimalLongitude | Double | Longitude coordinate |
| eventDate | String | Observation date |
| basisOfRecord | String | Record type |
| countryCode | String | ISO country code |

---

## Module: gbifutils

Utilities for interacting with the GBIF API.

### Functions

##### `name_parser(name: str) -> dict`

Parse a scientific name using GBIF name parser.

**Parameters:**

- `name`: Scientific name to parse

**Returns:**

Dictionary with parsed name components:

```python
{
    'scientificName': 'Panthera leo',
    'canonicalName': 'Panthera leo',
    'genus': 'Panthera',
    'specificEpithet': 'leo',
    ...
}
```

##### `name_usage(key: int) -> dict`

Get species information by GBIF key.

**Parameters:**

- `key`: GBIF species key

**Returns:**

Dictionary with species details:

```python
{
    'key': 5219404,
    'scientificName': 'Panthera leo (Linnaeus, 1758)',
    'kingdom': 'Animalia',
    'phylum': 'Chordata',
    'class': 'Mammalia',
    'order': 'Carnivora',
    'family': 'Felidae',
    'genus': 'Panthera',
    'species': 'Panthera leo',
    ...
}
```

##### `gbif_GET(url: str, params: dict = None) -> dict`

Make a GET request to the GBIF API.

**Parameters:**

- `url`: API endpoint URL
- `params`: Query parameters

**Returns:**

JSON response as dictionary

**Raises:**

- `ConnectionError`: If request fails

---

## Constants

### GBIF API Base URL

```python
GBIF_BASE_URL = "https://api.gbif.org/v1"
```

### Default Coordinate Reference System

```python
DEFAULT_CRS = "EPSG:4326"
```

---

## Events and Signals

### Dialog Signals

The dialog emits Qt signals for various events:

| Signal | Description |
|--------|-------------|
| `searchStarted` | Emitted when search begins |
| `searchCompleted` | Emitted when search finishes |
| `fetchStarted` | Emitted when data fetch begins |
| `fetchCompleted` | Emitted when data fetch finishes |
| `errorOccurred` | Emitted on errors |

---

## Error Handling

### Exception Types

```python
class GBIFError(Exception):
    """Base exception for GBIF-related errors."""

class ConnectionError(GBIFError):
    """Raised when GBIF API is unreachable."""

class APIError(GBIFError):
    """Raised when GBIF API returns an error."""
```

### Error Display

Errors are displayed via QGIS message bar:

```python
iface.messageBar().pushMessage(
    "Species Explorer",
    "Error fetching data: {error}",
    level=Qgis.Critical
)
```

---

## Examples

### Basic Usage

```python
from species_explorer.gbifutils import name_usage

# Get species information
species = name_usage(5219404)
print(f"Species: {species['scientificName']}")
print(f"Family: {species['family']}")
```

### Creating a Layer Programmatically

```python
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY

# Create memory layer
layer = QgsVectorLayer("Point?crs=EPSG:4326", "Occurrences", "memory")

# Add features
for occ in occurrences:
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPointXY(
        QgsPointXY(occ['decimalLongitude'], occ['decimalLatitude'])
    ))
    feature.setAttributes([occ['gbifID'], occ['scientificName']])
    layer.dataProvider().addFeature(feature)
```

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
