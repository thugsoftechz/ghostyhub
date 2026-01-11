#!/bin/bash

set -e -u -x

# Set timezone
ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Set locale
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Network configuration
echo "turbolinux" > /etc/hostname

# Create user 'gamer'
groupadd -f gamers
useradd -m -G wheel,rfkill,video,audio,input,storage,gamers -s /bin/zsh gamer
echo "gamer:gamer" | chpasswd
echo "root:root" | chpasswd

# Configure sudo
echo "%wheel ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel

# Enable Services
systemctl enable NetworkManager
systemctl enable bluetooth
systemctl enable sddm
systemctl enable ghost-ai.service

# Setup Emulation Defaults in /etc/skel
mkdir -p /etc/skel/.config/retroarch
cat <<EOF > /etc/skel/.config/retroarch/retroarch.cfg
video_driver = "vulkan"
audio_driver = "alsathread"
menu_driver = "xmb"
input_joypad_driver = "udev"
video_vsync = "true"
video_frame_delay = "0"
video_hard_sync = "true"
video_hard_sync_frames = "0"
EOF
mkdir -p /etc/skel/Games/ROMs/{NES,SNES,N64,GC,Wii,Switch,PS1,PS2,PS3}
chown -R root:root /etc/skel

# Fix permissions
chmod +x /usr/local/bin/hardware_detect.py
chmod +x /usr/local/bin/optimize.sh
rm /usr/local/bin/setup_emulation.sh # Removed as logic is now in customize_airootfs

# Initialize pacman keys (archlinux-keyring should be installed)
pacman-key --init
pacman-key --populate archlinux

# Note: chaotic-aur keyring would need to be installed here if enabled
# pacman-key --recv-key ...
# pacman-key --lsign-key ...
