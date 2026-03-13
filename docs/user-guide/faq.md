# Frequently Asked Questions

## General Questions

### What is GBIF?

The [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/) is an international network and data infrastructure that provides open access to biodiversity data. It hosts over 2 billion occurrence records from thousands of institutions worldwide.

### Is Species Explorer free?

Yes! Species Explorer is free and open-source software, licensed under the GPL-2.0 license. GBIF data is also freely accessible.

### What QGIS versions are supported?

Species Explorer supports QGIS 3.0 and later. We recommend using the latest stable or LTR version for best compatibility.

## Data Questions

### How current is the GBIF data?

GBIF data is continuously updated as data providers publish new records. When you fetch data, you're getting the latest available records from GBIF.

### Can I use this data commercially?

GBIF data is open data, but individual datasets may have specific licenses. Always check the data citation requirements and respect the licenses of individual publishers.

### Why are some coordinates missing?

Some GBIF records don't include coordinates for various reasons:

- Historical records without GPS
- Sensitive species locations obscured
- Data quality issues

Species Explorer only imports records with valid coordinates.

### What's the data accuracy?

Data accuracy varies by source:

- Museum specimens: Generally high accuracy
- Citizen science: Variable accuracy
- Historical records: May have lower precision

Check the `coordinateUncertaintyInMeters` field for precision information.

## Technical Questions

### Why is my download slow?

Large datasets can take time to download. Factors include:

- Number of records (millions for common species)
- Internet connection speed
- GBIF server load

### Can I limit the number of records?

Currently, Species Explorer fetches all available records. You can filter results after import using QGIS tools.

### Does it work offline?

No, Species Explorer requires an internet connection to fetch data from GBIF. However, once downloaded, the data is stored locally in your QGIS project.

### How do I report a bug?

Report bugs on our [GitHub Issues](https://github.com/kartoza/SpeciesExplorer/issues) page. Please include:

- QGIS version
- Plugin version
- Steps to reproduce
- Error messages

## Troubleshooting

### Plugin won't load

1. Check QGIS version (3.0+ required)
2. Verify plugin is enabled in Plugin Manager
3. Check for Python errors in View → Log Messages

### No results for my species

- Try the scientific name
- Check spelling
- Some species have limited GBIF records

### Data not displaying correctly

- Check CRS settings
- Ensure coordinates are valid (lat/lon)
- Try zooming to layer extent

---

Still have questions? [Open an issue](https://github.com/kartoza/SpeciesExplorer/issues) or contact us at [info@kartoza.com](mailto:info@kartoza.com).

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
