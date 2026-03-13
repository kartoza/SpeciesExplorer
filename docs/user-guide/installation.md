# Installation

This guide covers how to install Species Explorer in QGIS.

## Requirements

- **QGIS 3.0** or later
- **Internet connection** (for fetching data from GBIF)

## Installation Methods

### Method 1: QGIS Plugin Manager (Recommended)

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Search for "Species Explorer"
4. Click **Install Plugin**

![Plugin Manager](../assets/install-plugin-manager.png)

### Method 2: Install from ZIP

1. Download the latest release from [GitHub Releases](https://github.com/kartoza/SpeciesExplorer/releases)
2. Open QGIS
3. Go to **Plugins** → **Manage and Install Plugins**
4. Click **Install from ZIP**
5. Select the downloaded ZIP file
6. Click **Install Plugin**

### Method 3: Manual Installation

1. Download or clone the repository:
   ```bash
   git clone https://github.com/kartoza/SpeciesExplorer.git
   ```

2. Copy the `species_explorer` folder to your QGIS plugins directory:

    === "Linux"
        ```bash
        cp -r species_explorer ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
        ```

    === "Windows"
        ```powershell
        Copy-Item -Recurse species_explorer "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\"
        ```

    === "macOS"
        ```bash
        cp -r species_explorer ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/
        ```

3. Restart QGIS
4. Enable the plugin in **Plugins** → **Manage and Install Plugins**

## Verify Installation

After installation:

1. Check that Species Explorer appears in the **Plugins** menu
2. Look for the Species Explorer icon in the toolbar
3. Click the icon to open the plugin dialog

## Troubleshooting

### Plugin Not Showing

- Make sure the plugin is enabled in Plugin Manager
- Try restarting QGIS
- Check the QGIS log for errors (View → Log Messages)

### Network Issues

- Ensure you have an active internet connection
- Check if GBIF (gbif.org) is accessible
- Corporate firewalls may block the connection

### Python Errors

- Ensure your QGIS installation has the required Python packages
- Check the Python console for detailed error messages

## Next Steps

Once installed, proceed to the [Quick Start](quickstart.md) guide to begin using Species Explorer.

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
