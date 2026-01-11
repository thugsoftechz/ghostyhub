#!/usr/bin/env python3
"""
Hardware Detection & Configuration Script
Run at boot to detect GPU and apply environment variables.
"""

import subprocess
import os
import sys

def get_gpu_vendor():
    try:
        lspci = subprocess.check_output(["lspci"], text=True)
        if "NVIDIA" in lspci:
            return "nvidia"
        elif "AMD" in lspci or "Advanced Micro Devices" in lspci:
            return "amd"
        elif "Intel" in lspci:
            return "intel"
    except Exception as e:
        print(f"Error detecting GPU: {e}")
    return "unknown"

def configure_nvidia():
    print("Configuring NVIDIA GPU...")
    # Generate xorg.conf if needed or set env vars
    with open("/etc/environment", "a") as f:
        f.write("\n__NV_PRIME_RENDER_OFFLOAD=1\n")
        f.write("__GLX_VENDOR_LIBRARY_NAME=nvidia\n")
        f.write("GBM_BACKEND=nvidia-drm\n")
        f.write("WLR_NO_HARDWARE_CURSORS=1\n") # Often needed for Wayland on Nvidia

def configure_amd():
    print("Configuring AMD GPU...")
    with open("/etc/environment", "a") as f:
        f.write("\nRADV_PERFTEST=aco\n")
        f.write("AMD_VULKAN_ICD=radv\n")

def configure_intel():
    print("Configuring Intel GPU...")
    with open("/etc/environment", "a") as f:
        f.write("\nMESA_LOADER_DRIVER_OVERRIDE=iris\n")

def main():
    print("Starting Hardware Detection...")
    vendor = get_gpu_vendor()
    print(f"Detected GPU Vendor: {vendor}")

    if vendor == "nvidia":
        configure_nvidia()
    elif vendor == "amd":
        configure_amd()
    elif vendor == "intel":
        configure_intel()

    # Generic optimizations
    try:
        # Set CPU governor to performance
        subprocess.run("echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor", shell=True)
    except Exception as e:
        print(f"Failed to set CPU governor: {e}")

if __name__ == "__main__":
    main()
