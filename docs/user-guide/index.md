# User Guide

Welcome to the Species Explorer User Guide! This guide will help you get started with exploring biodiversity data in QGIS.

## What is Species Explorer?

Species Explorer is a QGIS plugin that connects to the [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/) to fetch and visualize species occurrence data. GBIF is the world's largest biodiversity database, containing over 2 billion occurrence records from around the globe.

## Getting Started

<div class="grid cards" markdown>

-   [**Installation**](installation.md)

    Learn how to install Species Explorer in QGIS

-   [**Quick Start**](quickstart.md)

    Get up and running in 5 minutes

-   [**Usage Guide**](usage.md)

    Detailed guide on all features

-   [**FAQ**](faq.md)

    Frequently asked questions

</div>

## Key Concepts

### Species Occurrence Data

An **occurrence record** is a documented observation of a species at a specific location and time. This can include:

- Museum specimen collections
- Field observations
- Citizen science records
- Research survey data

### GBIF Integration

Species Explorer uses the [GBIF REST API](https://www.gbif.org/developer/summary) to:

1. Search for species by name
2. Retrieve taxonomic information
3. Download occurrence records
4. Create point layers in QGIS

### Data Attributes

Each occurrence point includes attributes such as:

| Attribute | Description |
|-----------|-------------|
| `gbifID` | Unique GBIF identifier |
| `scientificName` | Full scientific name |
| `decimalLatitude` | Latitude coordinate |
| `decimalLongitude` | Longitude coordinate |
| `eventDate` | Date of observation |
| `basisOfRecord` | Type of record (specimen, observation, etc.) |
| `countryCode` | ISO country code |

## Need Help?

- Check the [FAQ](faq.md) for common questions
- Report issues on [GitHub](https://github.com/kartoza/SpeciesExplorer/issues)
- Contact [Kartoza](https://kartoza.com) for commercial support

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
