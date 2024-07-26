#!/bin/bash

# Check if requirements.txt exists
if [ ! -f libs.txt ]; then
    echo "libs.txt not found!"
    exit 1
fi

# Install dependencies
pip install -r libs.txt

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/src.py"

SHORTCUT_NAME="ScreenShoot OCR"
SHORTCUT_COMMAND="python3 $SCRIPT_PATH"
SHORTCUT_BINDING="<Ctrl><Shift>S"

# Get the current list of custom keybindings
CUSTOM_KEYBINDINGS=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)

# Create a new keybinding path
if [ "$CUSTOM_KEYBINDINGS" == "@as []" ]; then
    NEW_BINDING_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/"
    CUSTOM_KEYBINDINGS="['$NEW_BINDING_PATH']"
else
    # Remove the last character (which is ])
    CUSTOM_KEYBINDINGS="${CUSTOM_KEYBINDINGS%?}, "

    # Find the highest index number
    LAST_INDEX=$(echo "$CUSTOM_KEYBINDINGS" | grep -o 'custom[0-9]*' | sed 's/custom//' | sort -n | tail -1)

    # Increment the index number for the new binding
    NEXT_INDEX=$((LAST_INDEX + 1))

    NEW_BINDING_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$NEXT_INDEX/"
    CUSTOM_KEYBINDINGS="$CUSTOM_KEYBINDINGS'$NEW_BINDING_PATH']"
fi

# Set the new list of custom keybindings
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$CUSTOM_KEYBINDINGS"

# Set the name, command, and binding for the new shortcut
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$NEW_BINDING_PATH name "$SHORTCUT_NAME"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$NEW_BINDING_PATH command "$SHORTCUT_COMMAND"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$NEW_BINDING_PATH binding "$SHORTCUT_BINDING"

echo "Shortcut added: $SHORTCUT_NAME ($SHORTCUT_BINDING) -> $SHORTCUT_COMMAND"