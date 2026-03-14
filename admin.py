#!/usr/bin/env python3
"""
Species Explorer - Plugin Administration Tool

Provides utilities for:
- Building plugin packages (zip files)
- Creating symlinks for development
- Cleaning build artifacts
- Displaying plugin metadata

Made with 💗 by Kartoza | https://kartoza.com
"""

import argparse
import configparser
import os
import shutil
import sys
import zipfile
from pathlib import Path


# Files and directories to exclude from the plugin package
EXCLUDE_PATTERNS = [
    ".git",
    ".github",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".flake8",
    ".bandit.yml",
    ".yamllint",
    ".cspell.json",
    ".envrc",
    ".exrc",
    ".nvim.lua",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".coverage",
    ".mypy_cache",
    ".tox",
    "htmlcov",
    "test",
    "tests",
    "scripts",
    "docs",
    "site",
    "build",
    "dist",
    "*.egg-info",
    "flake.nix",
    "flake.lock",
    "pyproject.toml",
    "mkdocs.yml",
    "Makefile",
    "SPECIFICATION.md",
    "PACKAGES.md",
    "PROMPT.log",
    "admin.py",
    "*.zip",
    "*.tar.gz",
    "*.log",
    "*~",
    "*.orig",
    "*.bak",
    ".DS_Store",
    "Thumbs.db",
    "help",  # Old sphinx docs
    ".travis.yml",
    ".venv",
    "venv",
    ".direnv",
    "node_modules",
    "plugin_upload.py",
    "pb_tool.cfg",
    "pyrightconfig.json",
    "pylintrc",
    "REQUIREMENTS.txt",
    "REQUIREMENTS_TESTING.txt",
]


def get_project_dir() -> Path:
    """Get the project root directory (where this script lives)."""
    return Path(__file__).parent.resolve()


def get_plugin_dir() -> Path:
    """Get the plugin directory (species_explorer subfolder)."""
    return get_project_dir() / "species_explorer"


def get_metadata() -> dict:
    """Read and parse metadata.txt."""
    plugin_dir = get_plugin_dir()
    metadata_file = plugin_dir / "metadata.txt"

    if not metadata_file.exists():
        print(f"Error: metadata.txt not found at {metadata_file}")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(metadata_file)

    return dict(config["general"])


def get_qgis_plugins_dir() -> Path:
    """Get the QGIS plugins directory for the current user."""
    home = Path.home()

    # Check common QGIS profile locations
    possible_paths = [
        home / ".local/share/QGIS/QGIS3/profiles/default/python/plugins",
        home / "Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins",
        home / "AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins",
    ]

    for path in possible_paths:
        if path.parent.exists():
            return path

    # Default to Linux path
    return possible_paths[0]


def should_exclude(path: Path, base_dir: Path) -> bool:
    """Check if a path should be excluded from the package."""
    rel_path = path.relative_to(base_dir)

    for pattern in EXCLUDE_PATTERNS:
        # Check exact match
        if rel_path.name == pattern:
            return True
        # Check parent directories
        for part in rel_path.parts:
            if part == pattern:
                return True
        # Check glob patterns
        if pattern.startswith("*") and rel_path.name.endswith(pattern[1:]):
            return True
        if pattern.endswith("*") and rel_path.name.startswith(pattern[:-1]):
            return True

    return False


def cmd_build(args):
    """Build a plugin package (zip file)."""
    project_dir = get_project_dir()
    plugin_dir = get_plugin_dir()
    metadata = get_metadata()

    name = metadata.get("name", "SpeciesExplorer").replace(" ", "")
    version = metadata.get("version", "0.0.0")

    output_dir = Path(args.output) if args.output else project_dir
    output_file = output_dir / f"{name}-{version}.zip"

    print(f"Building plugin package: {output_file}")
    print(f"  Name: {metadata.get('name')}")
    print(f"  Version: {version}")
    print(f"  QGIS Version: {metadata.get('qgisminimumversion', metadata.get('qgisMinimumVersion'))} - {metadata.get('qgismaximumversion', metadata.get('qgisMaximumVersion', 'any'))}")
    print()

    # Create zip file
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(plugin_dir):
            root_path = Path(root)

            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d, plugin_dir)]

            for file in files:
                file_path = root_path / file
                if not should_exclude(file_path, plugin_dir):
                    # Archive path: SpeciesExplorer/path/to/file
                    arc_name = Path("SpeciesExplorer") / file_path.relative_to(plugin_dir)
                    zf.write(file_path, arc_name)
                    if args.verbose:
                        print(f"  Adding: {arc_name}")

    print(f"\n✓ Plugin package created: {output_file}")
    print(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")


def cmd_symlink(args):
    """Create a symlink in the QGIS plugins directory."""
    plugin_dir = get_plugin_dir()  # species_explorer subfolder
    qgis_plugins_dir = get_qgis_plugins_dir()

    # Allow custom profile
    if args.profile:
        profile_base = qgis_plugins_dir.parent.parent.parent
        qgis_plugins_dir = profile_base / args.profile / "python/plugins"

    symlink_path = qgis_plugins_dir / "SpeciesExplorer"

    print(f"Creating symlink for development:")
    print(f"  Source: {plugin_dir}")
    print(f"  Target: {symlink_path}")

    # Create plugins directory if needed
    qgis_plugins_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing symlink or directory
    if symlink_path.is_symlink():
        symlink_path.unlink()
        print("  Removed existing symlink")
    elif symlink_path.exists():
        if args.force:
            shutil.rmtree(symlink_path)
            print("  Removed existing directory (--force)")
        else:
            print(f"Error: {symlink_path} exists and is not a symlink.")
            print("  Use --force to remove it, or remove it manually.")
            sys.exit(1)

    # Create symlink
    symlink_path.symlink_to(plugin_dir)
    print(f"\n✓ Symlink created successfully!")
    print(f"  Restart QGIS to load the plugin.")


def cmd_unlink(args):
    """Remove the symlink from the QGIS plugins directory."""
    qgis_plugins_dir = get_qgis_plugins_dir()

    if args.profile:
        profile_base = qgis_plugins_dir.parent.parent.parent
        qgis_plugins_dir = profile_base / args.profile / "python/plugins"

    symlink_path = qgis_plugins_dir / "SpeciesExplorer"

    if symlink_path.is_symlink():
        symlink_path.unlink()
        print(f"✓ Symlink removed: {symlink_path}")
    elif symlink_path.exists():
        print(f"Warning: {symlink_path} exists but is not a symlink.")
        print("  Not removing. Please remove manually if needed.")
    else:
        print(f"No symlink found at {symlink_path}")


def cmd_clean(args):
    """Clean build artifacts."""
    project_dir = get_project_dir()

    print("Cleaning build artifacts...")

    patterns_to_clean = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        ".mypy_cache",
        ".tox",
        "build",
        "dist",
        "*.egg-info",
        "site",
    ]

    if args.all:
        patterns_to_clean.extend([
            "*.zip",
            "*.tar.gz",
        ])

    for pattern in patterns_to_clean:
        for path in project_dir.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed directory: {path.relative_to(project_dir)}")
            elif path.is_file():
                path.unlink()
                print(f"  Removed file: {path.relative_to(project_dir)}")

    print("\n✓ Clean complete!")


def cmd_info(args):
    """Display plugin metadata."""
    metadata = get_metadata()

    print("Species Explorer - Plugin Metadata")
    print("=" * 40)
    for key, value in sorted(metadata.items()):
        if key == "changelog":
            print(f"\n{key}:")
            for line in value.strip().split("\n"):
                print(f"  {line.strip()}")
        elif key == "about":
            print(f"\n{key}:")
            # Word wrap
            words = value.split()
            line = "  "
            for word in words:
                if len(line) + len(word) > 70:
                    print(line)
                    line = "  "
                line += word + " "
            if line.strip():
                print(line)
        else:
            print(f"{key}: {value}")


def cmd_version(args):
    """Display or set the plugin version."""
    metadata_file = get_plugin_dir() / "metadata.txt"

    if args.set:
        # Update version in metadata.txt
        with open(metadata_file, "r") as f:
            content = f.read()

        import re
        new_content = re.sub(
            r"^version=.*$",
            f"version={args.set}",
            content,
            flags=re.MULTILINE
        )

        with open(metadata_file, "w") as f:
            f.write(new_content)

        print(f"✓ Version updated to {args.set}")
    else:
        metadata = get_metadata()
        print(metadata.get("version", "unknown"))


def main():
    parser = argparse.ArgumentParser(
        description="Species Explorer - Plugin Administration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python admin.py build              Build plugin package
  python admin.py symlink            Create dev symlink in QGIS
  python admin.py unlink             Remove dev symlink
  python admin.py clean              Clean build artifacts
  python admin.py info               Show plugin metadata
  python admin.py version            Show current version
  python admin.py version --set 1.0  Set version to 1.0

Made with 💗 by Kartoza | https://kartoza.com
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # build command
    build_parser = subparsers.add_parser("build", help="Build plugin package (zip)")
    build_parser.add_argument("-o", "--output", help="Output directory for the zip file")
    build_parser.add_argument("-v", "--verbose", action="store_true", help="List files being added")
    build_parser.set_defaults(func=cmd_build)

    # symlink command
    symlink_parser = subparsers.add_parser("symlink", help="Create symlink in QGIS plugins dir")
    symlink_parser.add_argument("--profile", help="QGIS profile name (default: default)")
    symlink_parser.add_argument("--force", action="store_true", help="Force overwrite if directory exists")
    symlink_parser.set_defaults(func=cmd_symlink)

    # unlink command
    unlink_parser = subparsers.add_parser("unlink", help="Remove symlink from QGIS plugins dir")
    unlink_parser.add_argument("--profile", help="QGIS profile name (default: default)")
    unlink_parser.set_defaults(func=cmd_unlink)

    # clean command
    clean_parser = subparsers.add_parser("clean", help="Clean build artifacts")
    clean_parser.add_argument("--all", action="store_true", help="Also remove zip packages")
    clean_parser.set_defaults(func=cmd_clean)

    # info command
    info_parser = subparsers.add_parser("info", help="Display plugin metadata")
    info_parser.set_defaults(func=cmd_info)

    # version command
    version_parser = subparsers.add_parser("version", help="Display or set version")
    version_parser.add_argument("--set", help="Set version to this value")
    version_parser.set_defaults(func=cmd_version)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
