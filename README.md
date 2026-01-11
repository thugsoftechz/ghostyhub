# Ultra-Performance Gaming Linux Distro

This project provides a complete build system for a custom, high-performance Linux gaming distribution. It is designed to run live from RAM with persistence or be installed to disk.

## Features

- **Base**: Arch Linux (Rolling Release)
- **Kernel**: Optimized for Gaming (Zen / CachyOS) with PREEMPT, high tick rate.
- **UI**:
  - **Desktop Mode**: Minimal KDE Plasma.
  - **Game Mode**: Gamescope session (Steam Big Picture / Pegasus).
- **Gaming Stack**: Steam, Lutris, Heroic, Wine-Staging, Proton-GE, DXVK, VKD3D.
- **Emulation**: RetroArch, Dolphin, PCSX2, RPCS3, and more pre-installed.
- **Live Boot**: Complete OS loads into RAM (tmpfs) for zero I/O latency.

## Prerequisites

- A Linux host system (Arch Linux recommended for `archiso` tools).
- Python 3.10+
- `archiso` package installed (`pacman -S archiso`).
- ~15GB free space for the build process.
- Root privileges (required by `archiso`).

## Building the ISO

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```

2. **Run the build script**:
   ```bash
   sudo python3 build.py --clean --build
   ```

   Options:
   - `--clean`: Clean up previous build artifacts.
   - `--build`: Start the build process.
   - `--debug`: Enable verbose logging.
   - `--kernel-source`: (Optional) Compile kernel from source instead of using pre-built.

3. **Burn to USB**:
   The output ISO will be in `out/`. Use Etcher or `dd`:
   ```bash
   sudo dd if=out/turbo-linux-v1.0.iso of=/dev/sdX bs=4M status=progress
   ```

## Architecture

- **`build.py`**: The main orchestrator. Wraps `mkarchiso`.
- **`config/archiso`**: The Archiso profile definition.
- **`scripts/`**: Helper scripts for hardware detection, kernel building, and runtime optimization.

## Post-Boot

- The system auto-detects GPU (Nvidia/AMD/Intel) and loads appropriate drivers.
- "Game Mode" is available at the login screen.
- Emulators are pre-configured in `~/.config/retroarch`.

## Performance Benchmarking Methodology

To ensure zero-lag performance, we recommend the following benchmarking tools:
1. **MangoHUD**: Enabled by default. Press `Shift_R+F12` to toggle.
2. **vkMark**: Run `vkmark` to stress test the Vulkan driver stack.
3. **LatencyTop**: Use `latencytop` to visualize kernel latencies.

## Troubleshooting Guide

### Build Fails on Keyring
If the build fails with signature errors, ensure your host has up-to-date Arch keys:
```bash
sudo pacman -S archlinux-keyring
```

### Nvidia Drivers Not Loading
If booting on a hybrid laptop, ensure you are not in "Integrated Only" mode in BIOS.
The `hardware_detect.py` script logs to `systemctl status gaming-optimize`.

## Future Roadmap

- **v1.1**: Full `chaotic-aur` integration for CachyOS kernels.
- **v1.2**: Custom installer (Calamares) for permanent disk installation.
- **v2.0**: Handheld mode UI (Steam Deck clone interface).
