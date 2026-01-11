#!/bin/bash
# Wrapper to build GhostyHub ISO inside Docker
# This allows building on Ubuntu, Fedora, macOS (with Docker), etc.

set -e

echo "Building GhostyHub Docker Builder Image..."
docker build -t ghostyhub-builder .

echo "Running Build in Docker..."
# --privileged is required for loop mounting in mkarchiso
docker run --privileged --rm -v "$(pwd):/app" -w /app ghostyhub-builder python3 build.py --build

echo "Build Complete! Check 'out/' directory for the ISO."
