# Species Explorer

<div align="center">
  <img src="species_explorer/icon.svg" alt="Species Explorer" width="128">
  <p><strong>QGIS Plugin for Exploring Biodiversity Data from GBIF</strong></p>
</div>

---

[![CI](https://github.com/kartoza/SpeciesExplorer/actions/workflows/ci.yml/badge.svg)](https://github.com/kartoza/SpeciesExplorer/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/kartoza/SpeciesExplorer)](https://github.com/kartoza/SpeciesExplorer/releases)
[![License](https://img.shields.io/github/license/kartoza/SpeciesExplorer)](LICENSE)
[![QGIS](https://img.shields.io/badge/QGIS-3.0%2B-green)](https://qgis.org)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://kartoza.github.io/SpeciesExplorer)

## Overview

Species Explorer is a QGIS plugin for quickly retrieving and visualizing species occurrence data from [GBIF](https://www.gbif.org/) (Global Biodiversity Information Facility).

[![Video Demo](http://img.youtube.com/vi/La2ml0yDW6M/0.jpg)](http://www.youtube.com/watch?v=La2ml0yDW6M "Species Explorer Demo")

## Features

- **Search Species** - Find species by scientific or common name
- **View Taxonomy** - Display full taxonomic hierarchy
- **Fetch Occurrences** - Download occurrence records from GBIF
- **Visualize Data** - Create point layers directly in QGIS
- **Analyze** - Use QGIS tools for spatial analysis

## Quick Start

1. **Install** from QGIS Plugin Manager (search "Species Explorer")
2. **Open** via Plugins menu or toolbar
3. **Search** for a species by name
4. **Fetch** occurrence data
5. **Explore** on the map!

![Screenshot](https://user-images.githubusercontent.com/178003/45607302-ced24380-ba4b-11e8-8d86-b6020d109b87.png)

## Installation

### From Plugin Manager (Recommended)

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Search for "Species Explorer"
4. Click **Install Plugin**

### From ZIP

1. Download latest release from [Releases](https://github.com/kartoza/SpeciesExplorer/releases)
2. In QGIS: **Plugins** → **Manage and Install Plugins** → **Install from ZIP**

## Documentation

- [User Guide](https://kartoza.github.io/SpeciesExplorer/user-guide/)
- [Developer Guide](https://kartoza.github.io/SpeciesExplorer/developer/)
- [API Reference](https://kartoza.github.io/SpeciesExplorer/developer/api/)

## Development

### Setup with Nix (Recommended)

```bash
git clone https://github.com/kartoza/SpeciesExplorer.git
cd SpeciesExplorer
nix develop
```

### Common Commands

```bash
nix run .#qgis      # Launch QGIS with plugin
nix run .#test      # Run tests
nix run .#format    # Format code
nix run .#lint      # Lint code
nix run .#docs-serve  # Serve documentation
```

### Neovim

The repository includes `.exrc` and `.nvim.lua` for integrated development. All project commands are available under `<leader>p`.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](https://kartoza.github.io/SpeciesExplorer/developer/contributing/).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run checks (`nix run .#checks`)
4. Commit your changes
5. Push to the branch
6. Open a Pull Request

## Support

- [Report Issues](https://github.com/kartoza/SpeciesExplorer/issues)
- [Request Features](https://github.com/kartoza/SpeciesExplorer/issues/new?template=feature_request.md)
- [GitHub Discussions](https://github.com/kartoza/SpeciesExplorer/discussions)

## License

This project is licensed under the GPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [GBIF](https://www.gbif.org/) - Global Biodiversity Information Facility
- [pygbif](https://github.com/gbif/pygbif) - Python client for GBIF (Scott Chamberlain)
- [QGIS](https://qgis.org/) - Open Source Geographic Information System

---

<div align="center">
  <p>Made with :heart: by <a href="https://kartoza.com">Kartoza</a> | <a href="https://github.com/sponsors/timlinux">Donate</a> | <a href="https://github.com/kartoza/SpeciesExplorer">GitHub</a></p>
</div>
