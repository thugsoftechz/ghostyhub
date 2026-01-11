#!/bin/bash
# Runtime Optimization Script
# Called by systemd or user session

echo "Applying Gaming Optimizations..."

# 1. CPU Governor
if [ -d /sys/devices/system/cpu/cpu0/cpufreq ]; then
    for governor in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
        echo performance > "$governor"
    done
fi

# 2. GPU Power Management (Generic)
# AMD
if [ -d /sys/class/drm/card0/device/power_dpm_state ]; then
    echo performance > /sys/class/drm/card0/device/power_dpm_state
fi

# 3. Disable unnecessary services for gaming
systemctl stop cups || true
systemctl stop bluetooth || true # Only if not using controllers

# 4. Kernel compacting
echo 1 > /proc/sys/vm/compact_memory

echo "Optimizations Applied."
