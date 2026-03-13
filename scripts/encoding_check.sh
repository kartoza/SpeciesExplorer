#!/usr/bin/env bash
# Check Python files for UTF-8 encoding declarations
# This script ensures all Python files have proper encoding declarations

set -e

errors=0

for file in "$@"; do
    if [[ -f "$file" ]]; then
        # Check if file contains non-ASCII characters
        if grep -qP '[^\x00-\x7F]' "$file" 2>/dev/null; then
            # Check for encoding declaration in first two lines
            head -n 2 "$file" | grep -qE '^#.*coding[:=]\s*(utf-?8|UTF-?8)' || {
                echo "ERROR: $file contains non-ASCII characters but no UTF-8 encoding declaration"
                errors=$((errors + 1))
            }
        fi
    fi
done

if [[ $errors -gt 0 ]]; then
    echo ""
    echo "Found $errors file(s) with encoding issues."
    echo "Add '# -*- coding: utf-8 -*-' to the first or second line of these files."
    exit 1
fi

exit 0
