#!/usr/bin/env bash
# Species Explorer - Workspace cleanup script
# Removes build artifacts, caches, and temporary files

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🧹 Cleaning Species Explorer workspace...${NC}"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Python caches
echo "Removing Python caches..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*.pyd" -delete 2>/dev/null || true

# Test caches
echo "Removing test caches..."
rm -rf .pytest_cache 2>/dev/null || true
rm -rf .coverage 2>/dev/null || true
rm -rf htmlcov 2>/dev/null || true
rm -rf .tox 2>/dev/null || true
rm -rf .mypy_cache 2>/dev/null || true

# Build artifacts
echo "Removing build artifacts..."
rm -rf build 2>/dev/null || true
rm -rf dist 2>/dev/null || true
rm -rf *.egg-info 2>/dev/null || true

# Documentation build
echo "Removing documentation build..."
rm -rf site 2>/dev/null || true

# Core dumps
echo "Removing core dumps..."
find . -type f -name "core" -delete 2>/dev/null || true
find . -type f -name "core.*" -delete 2>/dev/null || true

# Temporary files
echo "Removing temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null || true
find . -type f -name "*.log" ! -name "PROMPT.log" -delete 2>/dev/null || true
find . -type f -name "*~" -delete 2>/dev/null || true

# Plugin packages
echo "Removing plugin packages..."
rm -f SpeciesExplorer-*.zip 2>/dev/null || true

echo ""
echo -e "${GREEN}✓ Workspace cleaned!${NC}"
echo ""
