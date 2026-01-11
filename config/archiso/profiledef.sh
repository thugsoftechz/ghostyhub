iso_name="ghostyhub"
iso_label="GHOSTYHUB_$(date +%Y%m)"
iso_publisher="GhostyHub Team <team@ghostyhub.io>"
iso_application="GhostyHub Gaming Platform"
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
