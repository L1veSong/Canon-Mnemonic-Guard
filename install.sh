#!/bin/bash
# Canon-Mnemonic-Guard v5.6.0 — One-click install
set -e

SKILLS_DIR="$HOME/.hermes/skills/software-development"
PLUGINS_DIR="$HOME/.hermes/plugins"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Canon-Mnemonic-Guard v5.6.0 Installer"
echo "======================================"

# 1. PyYAML
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "[1/4] Installing PyYAML..."
    pip3 install pyyaml
else
    echo "[1/4] PyYAML already installed"
fi

# 2. Skills
echo "[2/4] Installing skills..."
mkdir -p "$SKILLS_DIR"
for skill in canon guard mnemonic canon-mnemonic-guard; do
    if [ -d "$SCRIPT_DIR/$skill" ]; then
        rm -rf "$SKILLS_DIR/$skill"
        cp -r "$SCRIPT_DIR/$skill" "$SKILLS_DIR/"
        echo "  ✓ $skill"
    fi
done

# 3. Plugins
echo "[3/4] Installing plugins..."
mkdir -p "$PLUGINS_DIR"
for plugin in skill-autoload cmg-guard; do
    if [ -d "$SCRIPT_DIR/$plugin" ]; then
        rm -rf "$PLUGINS_DIR/$plugin"
        cp -r "$SCRIPT_DIR/$plugin" "$PLUGINS_DIR/"
        echo "  ✓ $plugin"
    fi
done

# 4. Init
echo "[4/4] Running init..."
INIT="$SKILLS_DIR/canon-mnemonic-guard/scripts/init.py"
if [ -f "$INIT" ]; then
    python3 "$INIT"
fi

echo ""
echo "Installation complete. Restart Hermes to apply."
echo "Dashboard: cd $SCRIPT_DIR/canon-mnemonic-guard-dashboard && ./cmg dashboard"
