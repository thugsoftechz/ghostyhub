#!/bin/bash
# Setup Emulation Defaults

echo "Setting up Emulation Environment..."

RETROARCH_CFG="$HOME/.config/retroarch/retroarch.cfg"
mkdir -p "$HOME/.config/retroarch"

# Basic RetroArch Optimizations
cat <<EOF > "$RETROARCH_CFG"
video_driver = "vulkan"
audio_driver = "alsathread"
menu_driver = "xmb"
input_joypad_driver = "udev"
video_vsync = "true"
video_frame_delay = "0"
video_hard_sync = "true"
video_hard_sync_frames = "0"
EOF

# Create ROMs directory structure
mkdir -p "$HOME/Games/ROMs"/{NES,SNES,N64,GC,Wii,Switch,PS1,PS2,PS3}

echo "Emulation setup complete."
