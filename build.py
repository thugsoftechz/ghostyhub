#!/usr/bin/env python3
"""
Ultra-Performance Gaming Distro Build System
Wraps `archiso` to build a live gaming Linux distribution.
"""

import os
import sys
import argparse
import subprocess
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROFILE_DIR = Path("config/archiso")
WORK_DIR = Path("work")
OUT_DIR = Path("out")

def check_dependencies():
    """Checks if required tools are installed."""
    required_tools = ["mkarchiso", "pacman"]
    for tool in required_tools:
        if not shutil.which(tool):
            logger.error(f"Required tool '{tool}' not found. Please install 'archiso'.")
            sys.exit(1)

    if os.geteuid() != 0:
        logger.error("This script must be run as root (required by archiso).")
        sys.exit(1)

def clean_build():
    """Cleans up work and output directories."""
    logger.info("Cleaning build directories...")
    if WORK_DIR.exists():
        try:
            # We use subprocess rm -rf because python's shutil.rmtree can struggle with
            # root-owned files created by archiso inside the work dir.
            subprocess.run(["rm", "-rf", str(WORK_DIR)], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clean work dir: {e}")
            sys.exit(1)

    if OUT_DIR.exists():
        logger.info(f"Note: Keeping output directory {OUT_DIR} (use manual deletion if needed).")

def run_build(profile_path, verbose=False):
    """Runs the mkarchiso build process."""
    cmd = ["mkarchiso", "-v" if verbose else "", "-w", str(WORK_DIR), "-o", str(OUT_DIR), str(profile_path)]
    # Filter out empty strings if verbose is False
    cmd = [c for c in cmd if c]

    logger.info(f"Starting build with command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        logger.info("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Build failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Build the Gaming Linux Distro ISO")
    parser.add_argument("--build", action="store_true", help="Start the build process")
    parser.add_argument("--clean", action="store_true", help="Clean work directory before building")
    parser.add_argument("--debug", action="store_true", help="Enable verbose output")
    # parser.add_argument("--kernel-source", help="Path to kernel source to compile (Not fully implemented)")

    args = parser.parse_args()

    if not args.build and not args.clean:
        parser.print_help()
        sys.exit(0)

    if args.clean:
        if os.geteuid() != 0:
             logger.warning("Cleaning usually requires root permissions due to archiso artifacts.")
             # We let it proceed, check_dependencies checks root for build anyway.
        clean_build()

    if args.build:
        check_dependencies()
        if not PROFILE_DIR.exists():
            logger.error(f"Profile directory {PROFILE_DIR} does not exist.")
            sys.exit(1)

        run_build(PROFILE_DIR, verbose=args.debug)

if __name__ == "__main__":
    main()
