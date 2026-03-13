# Development Setup

This guide covers setting up your development environment for Species Explorer.

## Prerequisites

- **Git** for version control
- **QGIS 3.0+** or Nix for QGIS provision
- **Python 3.9+**
- **Nix** (recommended) for reproducible environment

## Setup with Nix (Recommended)

### 1. Install Nix

If you don't have Nix installed:

```bash
curl -L https://nixos.org/nix/install | sh
```

Enable flakes in your Nix configuration:

```bash
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

### 2. Clone the Repository

```bash
git clone https://github.com/kartoza/SpeciesExplorer.git
cd SpeciesExplorer
```

### 3. Enter Development Shell

```bash
nix develop
```

This provides:

- Python environment with all dependencies
- QGIS
- Code quality tools (black, flake8, isort, pylint)
- Testing tools (pytest, coverage)
- Documentation tools (mkdocs)
- Pre-commit hooks

### 4. Allow direnv (Optional)

If you use direnv:

```bash
direnv allow
```

The environment will activate automatically when entering the directory.

## Setup without Nix

### 1. Clone the Repository

```bash
git clone https://github.com/kartoza/SpeciesExplorer.git
cd SpeciesExplorer
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r REQUIREMENTS.txt
pip install -r REQUIREMENTS_TESTING.txt
```

### 4. Install QGIS

Install QGIS 3.x from your system package manager or [qgis.org](https://qgis.org).

## Plugin Symlink

To test the plugin in QGIS, create a symlink:

=== "Linux"
    ```bash
    ln -s $(pwd)/species_explorer ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/SpeciesExplorer
    ```

=== "macOS"
    ```bash
    ln -s $(pwd)/species_explorer ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/SpeciesExplorer
    ```

=== "Windows"
    ```powershell
    mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\SpeciesExplorer" "species_explorer"
    ```

Or use the Nix command:

```bash
nix run .#symlink
```

## IDE Setup

### Neovim

The repository includes `.exrc` and `.nvim.lua` for Neovim integration:

- WhichKey shortcuts under `<leader>p`
- LSP configuration with Pyright
- DAP debugging support

### VS Code

Recommended extensions:

- Python
- Pylance
- QGIS Plugin Development

Create `.vscode/settings.json`:

```json
{
  "python.analysis.extraPaths": [
    "/usr/share/qgis/python",
    "/usr/share/qgis/python/plugins"
  ],
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true
}
```

### PyCharm

1. Set Python interpreter to your QGIS Python
2. Add QGIS Python paths to project structure
3. Enable Black formatter

## Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Run checks manually:

```bash
pre-commit run --all-files
```

Or using Nix:

```bash
nix run .#checks
```

## Compile Resources

If you modify `resources.qrc`:

```bash
pyrcc5 -o species_explorer/resources.py species_explorer/resources.qrc
```

## Running Tests

```bash
# With Nix
nix run .#test

# Without Nix
pytest test/ -v --cov=species_explorer
```

## Building Documentation

```bash
# Serve locally
nix run .#docs-serve

# Build static site
nix run .#docs-build
```

## Troubleshooting

### QGIS Python Not Found

Add QGIS to your Python path:

```bash
export PYTHONPATH="/usr/share/qgis/python:$PYTHONPATH"
```

### Pre-commit Fails

- Ensure all tools are installed
- Run `pre-commit clean` and try again
- Check specific hook errors

### Tests Fail

- Ensure QGIS is properly configured
- Check that all dependencies are installed
- Run with `-v` for verbose output

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
