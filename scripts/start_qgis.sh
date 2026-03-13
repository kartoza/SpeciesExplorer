#!/usr/bin/env bash
# Species Explorer - QGIS launcher
# Interactive launcher for QGIS with Species Explorer plugin

set -e

# Change to project root
cd "$(dirname "$0")/.."

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Plugin configuration
PLUGIN_NAME="SpeciesExplorer"
QGIS_PROFILE="${QGIS_PROFILE:-SpeciesExplorer}"

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}║   🦎 Species Explorer - QGIS Launcher                    ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Set up QGIS environment
export QGIS_CUSTOM_CONFIG_PATH="$HOME/.local/share/QGIS/QGIS3/profiles/$QGIS_PROFILE"

# Create symlink to plugin if needed
PLUGIN_DIR="$QGIS_CUSTOM_CONFIG_PATH/python/plugins/$PLUGIN_NAME"
if [ ! -L "$PLUGIN_DIR" ] && [ ! -d "$PLUGIN_DIR" ]; then
    mkdir -p "$(dirname "$PLUGIN_DIR")"
    ln -s "$PWD/species_explorer" "$PLUGIN_DIR"
    echo -e "${GREEN}✓ Created symlink: $PLUGIN_DIR${NC}"
fi

# Check if gum is available for interactive menu
if command -v gum &> /dev/null; then
    echo -e "${YELLOW}Select launch mode:${NC}"
    echo ""

    MODE=$(gum choose \
        "Normal - Standard QGIS launch" \
        "Debug - Enable debug logging" \
        "Verbose - Maximum logging" \
        "Attach Debugger - Enable debugpy for remote debugging")

    case "$MODE" in
        "Normal"*)
            export QGIS_DEBUG=0
            ;;
        "Debug"*)
            export QGIS_DEBUG=1
            export QGIS_LOG_FILE="$HOME/$PLUGIN_NAME.log"
            echo -e "${BLUE}Debug log: $QGIS_LOG_FILE${NC}"
            ;;
        "Verbose"*)
            export QGIS_DEBUG=2
            export QGIS_LOG_FILE="$HOME/$PLUGIN_NAME.log"
            echo -e "${BLUE}Debug log: $QGIS_LOG_FILE${NC}"
            ;;
        "Attach"*)
            export QGIS_DEBUG=1
            export QGIS_LOG_FILE="$HOME/$PLUGIN_NAME.log"
            export PYDEVD_DISABLE_FILE_VALIDATION=1
            echo -e "${YELLOW}Debugger will listen on port 5678${NC}"
            echo -e "${BLUE}Attach your debugger to localhost:5678${NC}"

            # Inject debugpy startup
            DEBUGPY_INIT=$(cat << 'PYEOF'
import debugpy
debugpy.listen(("localhost", 5678))
print("Waiting for debugger to attach on port 5678...")
# Uncomment to wait for debugger before continuing
# debugpy.wait_for_client()
PYEOF
)
            export PYQGIS_STARTUP="$DEBUGPY_INIT"
            ;;
    esac
else
    # No gum, just launch normally
    echo -e "${YELLOW}Launching QGIS (install 'gum' for interactive menu)${NC}"
    export QGIS_DEBUG=0
fi

echo ""
echo -e "${BLUE}Profile: $QGIS_PROFILE${NC}"
echo -e "${BLUE}Plugin:  $PLUGIN_DIR${NC}"
echo ""

# Find QGIS executable
if command -v qgis &> /dev/null; then
    QGIS_BIN="qgis"
elif [ -f "/usr/bin/qgis" ]; then
    QGIS_BIN="/usr/bin/qgis"
elif [ -f "/Applications/QGIS.app/Contents/MacOS/QGIS" ]; then
    QGIS_BIN="/Applications/QGIS.app/Contents/MacOS/QGIS"
else
    echo -e "${YELLOW}QGIS not found in PATH. Trying nix...${NC}"
    if command -v nix &> /dev/null; then
        exec nix run .#qgis
    else
        echo "Error: QGIS not found. Please install QGIS or use 'nix develop'."
        exit 1
    fi
fi

echo -e "${GREEN}Launching QGIS...${NC}"
echo ""

exec "$QGIS_BIN" --profile "$QGIS_PROFILE" "$@"
