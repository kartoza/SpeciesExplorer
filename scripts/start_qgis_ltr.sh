#!/usr/bin/env bash
# Species Explorer - QGIS LTR launcher
# Uses Ivan Mincik's geospatial-nix.repo via flake

echo "🦎 Running QGIS LTR with the SpeciesExplorer profile:"
echo "--------------------------------"

# Change to project root
cd "$(dirname "$0")/.."

# Plugin configuration
PLUGIN_NAME="SpeciesExplorer"
QGIS_PROFILE="${QGIS_PROFILE:-SpeciesExplorer}"
SPECIES_EXPLORER_LOG=$HOME/SpeciesExplorer.log
SPECIES_EXPLORER_TEST_DIR="$(pwd)/test"

# Clear previous log
rm -f "$SPECIES_EXPLORER_LOG"

# Set up QGIS environment and plugin symlink
export QGIS_CUSTOM_CONFIG_PATH="$HOME/.local/share/QGIS/QGIS3/profiles/$QGIS_PROFILE"
PLUGIN_DIR="$QGIS_CUSTOM_CONFIG_PATH/python/plugins/$PLUGIN_NAME"
if [ ! -L "$PLUGIN_DIR" ] && [ ! -d "$PLUGIN_DIR" ]; then
    mkdir -p "$(dirname "$PLUGIN_DIR")"
    ln -s "$PWD/species_explorer" "$PLUGIN_DIR"
    echo "Created symlink: $PLUGIN_DIR"
fi

# Launch QGIS LTR via nix flake
# Uses geospatial-nix.repo for QGIS LTR version
SPECIES_EXPLORER_LOG=${SPECIES_EXPLORER_LOG} \
    SPECIES_EXPLORER_TEST_DIR=${SPECIES_EXPLORER_TEST_DIR} \
    RUNNING_ON_LOCAL=1 \
    nix run .#qgis-ltr -- --profile "$QGIS_PROFILE"
