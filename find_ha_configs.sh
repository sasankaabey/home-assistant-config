#!/bin/bash
# Find all Home Assistant config folders on your Mac

echo "=== Searching for Home Assistant configuration folders ==="
echo ""

# Find all folders that look like HA configs (contain configuration.yaml)
echo "1. Folders containing configuration.yaml:"
find ~ /Volumes -name "configuration.yaml" 2>/dev/null | while read config; do
    dir=$(dirname "$config")
    echo "  📁 $dir"

    # Check if it's a git repo
    if [ -d "$dir/.git" ]; then
        echo "     ✓ GIT REPO"
        cd "$dir"
        remote=$(git remote get-url origin 2>/dev/null || echo "No remote")
        echo "     └─ Remote: $remote"
        branch=$(git branch --show-current 2>/dev/null)
        echo "     └─ Branch: $branch"
    else
        echo "     ✗ NOT a git repo"
    fi
    echo ""
done

echo ""
echo "2. Folders with names matching HA config patterns:"
find ~ /Volumes -type d \( -name "*ha-config*" -o -name "*home-assistant*config*" -o -name "homeassistant" \) 2>/dev/null | grep -v "/Library/" | grep -v "/.venv/" | while read dir; do
    echo "  📁 $dir"
    if [ -f "$dir/configuration.yaml" ]; then
        echo "     ✓ Contains configuration.yaml"
    else
        echo "     ✗ No configuration.yaml found"
    fi
    if [ -d "$dir/.git" ]; then
        echo "     ✓ GIT REPO"
    fi
    echo ""
done

echo ""
echo "3. Mounted volumes (like network shares):"
ls -la /Volumes/ 2>/dev/null | grep -v "Macintosh HD" | tail -n +4
