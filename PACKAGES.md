# Species Explorer - Package Documentation

## Overview

This document provides an annotated list of all packages and modules in the Species Explorer software architecture.

---

## Package Structure

```
SpeciesExplorer/
├── species_explorer/          # Main plugin package
│   ├── __init__.py           # Plugin entry point
│   ├── species_explorer.py   # Main plugin class
│   ├── species_explorer_dialog.py      # Dialog UI logic
│   ├── species_explorer_dialog_base.ui # Qt Designer UI
│   ├── gbifutils.py          # GBIF API utilities
│   ├── resources.py          # Compiled Qt resources
│   ├── resources.qrc         # Qt resource definitions
│   └── icon.png              # Plugin icon
├── test/                      # Test suite
├── docs/                      # MkDocs documentation
├── scripts/                   # Helper scripts
└── metadata.txt              # QGIS plugin metadata
```

---

## Core Modules

### `species_explorer/__init__.py`

**Purpose:** Plugin entry point for QGIS plugin loading.

**Key Functions:**
- `classFactory(iface)` - Creates plugin instance

**Dependencies:**
- `.species_explorer.SpeciesExplorer`

---

### `species_explorer/species_explorer.py`

**Purpose:** Main plugin class handling QGIS integration.

**Class:** `SpeciesExplorer`

**Responsibilities:**
- Initialize plugin GUI (toolbar, menu)
- Manage plugin lifecycle
- Show/hide dialog

**Key Methods:**

| Method | Description |
|--------|-------------|
| `__init__(iface)` | Initialize with QGIS interface |
| `initGui()` | Create toolbar action and menu entry |
| `run()` | Show the Species Explorer dialog |
| `unload()` | Clean up on plugin unload |

**Dependencies:**
- `qgis.PyQt.QtWidgets`
- `qgis.PyQt.QtGui`
- `qgis.core`

---

### `species_explorer/species_explorer_dialog.py`

**Purpose:** Main dialog with all user interaction logic.

**Class:** `SpeciesExplorerDialog` (extends QDialog)

**Responsibilities:**
- Handle user input
- Execute GBIF searches
- Create occurrence layers

**Key Methods:**

| Method | Description |
|--------|-------------|
| `find()` | Search GBIF for species matching input |
| `select(item)` | Display taxonomy for selected species |
| `fetch()` | Download occurrences and create layer |
| `create_fields(layer, record)` | Define attribute schema |

**UI Elements:**
- `search_text` - Line edit for species name
- `search_button` - Triggers find()
- `results_list` - List widget for search results
- `taxonomy_list` - List widget for taxonomy display
- `fetch_button` - Triggers fetch()

**Dependencies:**
- `qgis.PyQt.QtWidgets`
- `qgis.PyQt.QtCore`
- `qgis.PyQt.QtGui`
- `qgis.core` (QgsVectorLayer, QgsFeature, QgsField, etc.)
- `.gbifutils`

---

### `species_explorer/gbifutils.py`

**Purpose:** Utilities for GBIF REST API interaction.

**Origin:** Adapted from [pygbif](https://github.com/gbif/pygbif) by Scott Chamberlain

**Key Functions:**

| Function | Description |
|----------|-------------|
| `gbif_GET(url, args)` | Make HTTP GET request to GBIF |
| `name_parser(name)` | Parse scientific name |
| `name_usage(key, ...)` | Get species details |

**Helper Functions:**

| Function | Description |
|----------|-------------|
| `bn(x)` | Return value or None |
| `check_data(x, y)` | Validate data choices |
| `len2(x)` | Length handling for strings |
| `get_meta(x)` | Extract pagination metadata |
| `has_meta(x)` | Check for pagination metadata |

**Constants:**
- `gbif_baseurl` - GBIF API base URL

**Dependencies:**
- `requests` (imported but currently uses QgsFileDownloader)
- `qgis.PyQt.QtCore`
- `qgis.core.QgsFileDownloader`
- `json`
- `tempfile`

---

### `species_explorer/resources.py`

**Purpose:** Compiled Qt resources (auto-generated).

**Generated From:** `resources.qrc`

**Contains:**
- Plugin icons
- Other static assets

**Compilation:**
```bash
pyrcc5 -o resources.py resources.qrc
```

---

## UI Files

### `species_explorer/species_explorer_dialog_base.ui`

**Purpose:** Qt Designer UI definition for main dialog.

**Format:** XML (Qt Designer)

**Widgets Defined:**
- QDialog container
- QLineEdit (search_text)
- QPushButton (search_button, fetch_button)
- QListWidget (results_list, taxonomy_list)

---

## Test Suite

### `test/`

**Purpose:** Unit and integration tests.

**Framework:** pytest / nosetests

**Test Files:**

| File | Description |
|------|-------------|
| `test_init.py` | Plugin initialization tests |
| `test_suite.py` | Test suite aggregator |
| `test_resources.py` | Resource compilation tests |
| `test_qgis_environment.py` | QGIS environment tests |
| `test_gbifutils.py` | GBIF utilities tests |

**Running Tests:**
```bash
# With Nix
nix run .#test

# With pytest
pytest test/ -v --cov=species_explorer
```

---

## Configuration Files

### `metadata.txt`

**Purpose:** QGIS plugin metadata.

**Key Fields:**
- `name` - Plugin display name
- `version` - Current version
- `author` - Author/organization
- `qgisMinimumVersion` - Minimum QGIS version
- `description` - Short description
- `about` - Long description
- `tracker` - Issue tracker URL
- `repository` - Source repository URL

### `pyproject.toml`

**Purpose:** Modern Python project configuration.

**Contains:**
- Project metadata
- Black formatter settings
- isort import settings
- pytest configuration
- mypy type checking settings
- pylint configuration

### `flake.nix`

**Purpose:** Nix flake for reproducible development environment.

**Provides:**
- Development shell with all tools
- QGIS with Python bindings
- Convenience apps (test, format, lint, etc.)

---

## Scripts

### `scripts/`

**Helper Scripts:**

| Script | Description |
|--------|-------------|
| `checks.sh` | Run pre-commit checks |
| `clean.sh` | Clean workspace |
| `start_qgis.sh` | Launch QGIS with plugin |
| `encoding_check.sh` | Check Python file encodings |
| `compile-strings.sh` | Compile translations |
| `update-strings.sh` | Update translation strings |
| `release.sh` | Build release package |

---

## Documentation

### `docs/`

**System:** MkDocs with Material theme

**Structure:**
- `index.md` - Home page
- `user-guide/` - User documentation
- `developer/` - Developer documentation
- `about/` - License and credits

**Building:**
```bash
# Serve locally
nix run .#docs-serve

# Build static site
nix run .#docs-build
```

---

## Dependencies

### Runtime Dependencies

| Package | Purpose |
|---------|---------|
| QGIS | Core GIS functionality |
| PyQt5 | Qt bindings for Python |
| requests | HTTP library (legacy) |

### Development Dependencies

| Package | Purpose |
|---------|---------|
| pytest | Testing framework |
| pytest-cov | Coverage reporting |
| black | Code formatting |
| flake8 | Linting |
| isort | Import sorting |
| mypy | Type checking |
| mkdocs | Documentation |
| pre-commit | Git hooks |

---

## Version History

| Version | Changes |
|---------|---------|
| 0.1 | Initial release |
| 0.2.0 | Modernized tooling, documentation, CI/CD |

---

Made with :heart: by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
