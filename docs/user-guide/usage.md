# Usage Guide

This guide covers all features and functionality of Species Explorer.

## Interface Overview

The Species Explorer dialog has three main sections:

1. **Search Area** - Enter species names and search
2. **Results List** - Browse matching species
3. **Action Buttons** - Fetch data or clear results

## Searching for Species

### Scientific Names

Enter the full or partial scientific name:

- Full name: `Panthera leo`
- Genus only: `Panthera`
- Partial: `leo`

### Common Names

Many species can be found by common name:

- `lion`
- `african elephant`
- `blue whale`

### Search Tips

!!! tip "Best Practices"
    - Scientific names provide more accurate results
    - GBIF may have multiple entries for synonyms
    - Check the taxonomy to verify you have the correct species

## Fetching Occurrence Data

### Process

When you click **Fetch**:

1. Species Explorer queries the GBIF API
2. Occurrence records are downloaded
3. A point layer is created in QGIS
4. Default styling is applied

### Data Limits

GBIF may return thousands of records. Consider:

- Large datasets may take time to download
- Memory usage increases with record count
- You can filter data later in QGIS

## Working with Results

### Layer Structure

Each occurrence layer includes:

| Field | Type | Description |
|-------|------|-------------|
| gbifID | Integer | Unique identifier |
| scientificName | String | Full scientific name |
| decimalLatitude | Float | Latitude |
| decimalLongitude | Float | Longitude |
| eventDate | String | Observation date |
| basisOfRecord | String | Record type |
| countryCode | String | ISO country code |
| institutionCode | String | Data provider |

### Styling

The default style uses:

- Point markers with species-appropriate colors
- Clustering for dense areas
- Labels on hover

You can customize styling using standard QGIS tools.

### Filtering

Filter your data using:

- **Attribute Table** filters
- **Select by Expression**
- **Definition Queries**

Example expression to filter recent records:
```sql
"eventDate" > '2020-01-01'
```

### Export Options

Export occurrence data to:

- **Shapefile** - For GIS compatibility
- **GeoPackage** - Modern, recommended format
- **CSV** - For spreadsheet analysis
- **GeoJSON** - For web applications

## Advanced Usage

### Combining with Other Data

Species occurrence data works well with:

- **Protected Areas** - Assess species within reserves
- **Climate Data** - Model species distributions
- **Land Cover** - Analyze habitat preferences
- **Elevation** - Understand altitudinal ranges

### Spatial Analysis

Use QGIS tools for:

- **Heatmaps** - Visualize occurrence density
- **Kernel Density** - Estimate species density
- **Point Pattern Analysis** - Analyze distribution patterns
- **Species Richness** - Count species per area

## Troubleshooting

### No Results Found

- Check spelling of species name
- Try alternative names or synonyms
- Use scientific name instead of common name

### Missing Coordinates

Some GBIF records lack coordinates. These are filtered out during import.

### Slow Downloads

- Large datasets take time
- Check internet connection
- GBIF API may be under high load

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
