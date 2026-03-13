# Species Explorer

<div align="center">
  <img src="assets/icon.svg" alt="Species Explorer" width="128">
  <p><strong>QGIS Plugin for Exploring Biodiversity Data from GBIF</strong></p>
</div>

---

[![CI](https://github.com/kartoza/SpeciesExplorer/actions/workflows/ci.yml/badge.svg)](https://github.com/kartoza/SpeciesExplorer/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/kartoza/SpeciesExplorer)](https://github.com/kartoza/SpeciesExplorer/releases)
[![License](https://img.shields.io/github/license/kartoza/SpeciesExplorer)](https://github.com/kartoza/SpeciesExplorer/blob/master/LICENSE)
[![QGIS](https://img.shields.io/badge/QGIS-3.0%2B-green)](https://qgis.org)

## Overview

Species Explorer is a QGIS plugin that allows you to quickly fetch and visualize species occurrence data from the [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/).

With Species Explorer, you can:

- **Search** for species by scientific or common name
- **Fetch** occurrence records from GBIF's extensive database
- **Visualize** species distributions directly in QGIS
- **Analyze** biodiversity patterns with powerful GIS tools

## Quick Start

1. **Install the plugin** from the QGIS Plugin Manager
2. **Open Species Explorer** from the Plugins menu
3. **Search** for a species by name
4. **Click Fetch** to download occurrence data
5. **Explore** the data in QGIS!

[Get Started :material-arrow-right:](user-guide/quickstart.md){ .md-button .md-button--primary }

## Features

<div class="grid cards" markdown>

-   :material-magnify:{ .lg .middle } **Species Search**

    ---

    Search for species using scientific names, common names, or taxonomic hierarchy.

-   :material-download:{ .lg .middle } **GBIF Integration**

    ---

    Direct integration with GBIF's REST API to fetch occurrence records.

-   :material-map-marker:{ .lg .middle } **Point Layer Creation**

    ---

    Automatically creates point layers with occurrence locations and attributes.

-   :material-palette:{ .lg .middle } **Styled Visualization**

    ---

    Includes default styling with clustered point visualization.

</div>

## Screenshots

![Species Explorer Dialog](assets/screenshot-dialog.png)

## Documentation

- [**User Guide**](user-guide/index.md) - Learn how to use Species Explorer
- [**Developer Guide**](developer/index.md) - Contribute to development
- [**API Reference**](developer/api.md) - Technical documentation

## Support

- [**GitHub Issues**](https://github.com/kartoza/SpeciesExplorer/issues) - Report bugs or request features
- [**GitHub Discussions**](https://github.com/kartoza/SpeciesExplorer/discussions) - Ask questions

---

<div align="center">
  <p>Made with 💗 by <a href="https://kartoza.com">Kartoza</a> | <a href="https://github.com/sponsors/timlinux">Donate</a> | <a href="https://github.com/kartoza/SpeciesExplorer">GitHub</a></p>
</div>
