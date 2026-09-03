#!/usr/bin/env bash
set -e

echo "🎮 Installing Joy-Con Mouse & Universal Media Remote for Linux..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN="$HOME/.local/bin/joycon-mouse"

# Ensure ~/.local/bin exists
mkdir -p "$HOME/.local/bin"

# Symlink main script
ln -sf "$SCRIPT_DIR/joycon-mouse.py" "$TARGET_BIN"
chmod +x "$SCRIPT_DIR/joycon-mouse.py"
chmod +x "$TARGET_BIN"

echo "✓ Created symlink at $TARGET_BIN"

# Check group permissions
if ! groups "$USER" | grep -q '\binput\b'; then
    echo "⚠️  User '$USER' is not in the 'input' group."
    echo "   Running: sudo usermod -aG input $USER"
    sudo usermod -aG input "$USER" || echo "Please add yourself to the 'input' group manually: sudo usermod -aG input \$USER"
    echo "   (Note: You may need to log out and log back in for group permissions to apply)."
else
    echo "✓ User '$USER' is already a member of the 'input' group."
fi

# Ensure uinput module is active
if ! lsmod | grep -q '\buinput\b'; then
    echo "⚠️  Loading uinput kernel module..."
    sudo modprobe uinput || true
fi

echo ""
echo "🎉 Installation complete!"
echo "   Run 'joycon-mouse -l' to list connected controllers."
echo "   Run 'joycon-mouse' to start the driver."
echo "   Run 'joycon-mouse --install-service' for auto-start on boot."
