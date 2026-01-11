/*
 * GhostyHub GPU DMA Latency Tuner
 * Reduces GPU interrupt latency for VR workloads.
 */

#include <linux/module.h>
#include <linux/pci.h>

void ghost_gpu_boost(struct pci_dev *pdev) {
    /*
     * Increase PCI latency timer to max for GPU.
     * This allows the GPU to hold the bus longer for transfers.
     */
    pci_write_config_byte(pdev, PCI_LATENCY_TIMER, 255);
}
