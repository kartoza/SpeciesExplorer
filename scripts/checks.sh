#!/usr/bin/env bash
# Species Explorer - Pre-commit checks runner
# Run all code quality checks

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}║   🦎 Species Explorer - Code Quality Checks              ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Clean pre-commit cache if requested
if [[ "$1" == "--clean" ]]; then
    echo -e "${YELLOW}Cleaning pre-commit cache...${NC}"
    pre-commit clean
    echo ""
fi

# Install hooks if not already installed
if [[ ! -f ".git/hooks/pre-commit" ]]; then
    echo -e "${YELLOW}Installing pre-commit hooks...${NC}"
    pre-commit install
    echo ""
fi

# Run pre-commit on all files
echo -e "${BLUE}Running pre-commit checks on all files...${NC}"
echo ""

if pre-commit run --all-files; then
    echo ""
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}✗ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    exit 1
fi

echo -e "${BLUE}Made with 💗 by Kartoza | https://kartoza.com${NC}"
echo ""
