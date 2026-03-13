# Contributing

Thank you for your interest in contributing to Species Explorer! This guide explains how to contribute to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all backgrounds and experience levels.

## Ways to Contribute

### Report Bugs

Found a bug? Please [open an issue](https://github.com/kartoza/SpeciesExplorer/issues/new?template=bug_report.md) with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- QGIS and plugin versions
- Screenshots if applicable

### Suggest Features

Have an idea? [Open a feature request](https://github.com/kartoza/SpeciesExplorer/issues/new?template=feature_request.md) with:

- Clear description of the feature
- Use case and benefits
- Possible implementation approach

### Improve Documentation

Documentation improvements are always welcome:

- Fix typos and errors
- Add examples and tutorials
- Improve explanations
- Translate documentation

### Submit Code

Ready to code? Follow these steps:

## Development Workflow

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/SpeciesExplorer.git
cd SpeciesExplorer
git remote add upstream https://github.com/kartoza/SpeciesExplorer.git
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Use descriptive branch names:

- `feature/add-export-csv`
- `fix/handle-empty-results`
- `docs/improve-installation`

### 3. Set Up Environment

```bash
nix develop
pre-commit install
```

### 4. Make Changes

Write your code following our standards:

- **Format** with black: `nix run .#format`
- **Lint** with flake8: `nix run .#lint`
- **Test** your changes: `nix run .#test`

### 5. Commit Changes

Write clear commit messages:

```bash
git commit -m "Add CSV export functionality

- Add export_to_csv() function
- Add Export button to dialog
- Update documentation"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then [open a Pull Request](https://github.com/kartoza/SpeciesExplorer/compare) on GitHub.

## Code Standards

### Python Style

- **Python 3.9+** compatibility
- **120 character** line length
- **Black** formatting (automatic with pre-commit)
- **isort** for imports (automatic with pre-commit)

### Docstrings

Use Google-style docstrings:

```python
def fetch_species(name: str, limit: int = 100) -> list:
    """Fetch species occurrences from GBIF.

    Args:
        name: Scientific or common name to search.
        limit: Maximum number of records to fetch.

    Returns:
        List of occurrence dictionaries.

    Raises:
        ConnectionError: If GBIF API is unreachable.
    """
```

### Type Hints

Use type hints for function signatures:

```python
def create_layer(
    name: str,
    occurrences: list[dict],
    crs: str = "EPSG:4326"
) -> QgsVectorLayer:
    ...
```

### Testing

- Write tests for new functionality
- Maintain or improve code coverage
- Tests should be independent and repeatable

```python
def test_fetch_species_returns_list():
    """Test that fetch_species returns a list."""
    result = fetch_species("Panthera leo")
    assert isinstance(result, list)
```

## Pull Request Guidelines

### Before Submitting

- [ ] Code passes all linting checks
- [ ] Tests pass and coverage is maintained
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear

### PR Description

Include in your PR description:

- Summary of changes
- Related issue numbers (fixes #123)
- Screenshots for UI changes
- Testing instructions

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, it will be merged
4. You'll be credited in the release notes

## Release Process

Releases are managed by maintainers:

1. Update version in `metadata.txt`
2. Update CHANGELOG
3. Create and push version tag
4. GitHub Actions builds and publishes release

## Getting Help

- **Questions:** Open a [Discussion](https://github.com/kartoza/SpeciesExplorer/discussions)
- **Bugs:** Open an [Issue](https://github.com/kartoza/SpeciesExplorer/issues)
- **Chat:** Contact [Kartoza](https://kartoza.com)

## Recognition

Contributors are recognized in:

- Release notes
- README credits section
- This documentation

Thank you for contributing to Species Explorer!

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
