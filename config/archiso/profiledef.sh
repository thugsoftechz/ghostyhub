iso_name="turbolinux"
iso_label="TURBOLINUX_$(date +%Y%m)"
iso_publisher="Jules <jules@example.com>"
iso_application="TurboLinux Gaming Live"
iso_version="$(date +%Y.%m.%d)"
install_dir="arch"
buildmodes=('iso')
bootmodes=('bios.syslinux.mbr' 'bios.syslinux.eltorito'
           'uefi-ia32.grub.esp' 'uefi-x64.grub.esp'
           'uefi-ia32.grub.eltorito' 'uefi-x64.grub.eltorito')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd' '-Xcompression-level' '15' '-b' '1M')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/etc/sudoers"]="0:0:440"
  ["/usr/local/bin/hardware_detect.py"]="0:0:755"
  ["/usr/local/bin/optimize.sh"]="0:0:755"
)
