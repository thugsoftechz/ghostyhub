#!/usr/bin/env python3
"""
Kernel Build Helper
This script automates fetching and building a custom kernel (e.g., Linux Zen or TKG).
Note: This is a heavy process and should be run on a powerful host.
"""

import os
import subprocess
import sys
import argparse

KERNEL_SOURCE_URL = "https://github.com/zen-kernel/zen-kernel.git"
BUILD_DIR = "kernel_build"

def clone_kernel(url, branch="v6.6-zen1"):
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    target_dir = os.path.join(BUILD_DIR, "src")
    if os.path.exists(target_dir):
        print(f"Kernel source already exists at {target_dir}")
        return

    print(f"Cloning kernel source from {url}...")
    subprocess.run(["git", "clone", "--depth", "1", "-b", branch, url, target_dir], check=True)

def configure_kernel():
    print("Configuring kernel...")
    # Copy current config if available or use default
    src_dir = os.path.join(BUILD_DIR, "src")
    if os.path.exists("/proc/config.gz"):
        subprocess.run(f"zcat /proc/config.gz > {src_dir}/.config", shell=True)
    else:
        print("No /proc/config.gz found, using default defconfig")
        subprocess.run(["make", "defconfig"], cwd=src_dir, check=True)

def compile_kernel(threads):
    print(f"Compiling kernel with {threads} threads...")
    src_dir = os.path.join(BUILD_DIR, "src")
    try:
        subprocess.run(["make", f"-j{threads}"], cwd=src_dir, check=True)
        print("Compilation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Build Custom Gaming Kernel")
    parser.add_argument("--branch", default="v6.6-zen1", help="Kernel branch/tag")
    parser.add_argument("--jobs", "-j", type=int, default=os.cpu_count(), help="Number of build threads")

    args = parser.parse_args()

    clone_kernel(KERNEL_SOURCE_URL, args.branch)
    configure_kernel()
    compile_kernel(args.jobs)

    print("Kernel build finished. Install modules and bzImage manually to airootfs.")

if __name__ == "__main__":
    main()
