"""Utility functions for device management and display."""
from typing import List, Dict, Any


def is_connected(device: Dict[str, Any]) -> bool:
    """
    Args:
        device: Device dictionary

    Returns:
        True if connected, False otherwise
    """
    return device.get("connected", False)


def device_status_text(device: Dict[str, Any]) -> str:
    """
    Args:
        device: Device dictionary

    Returns:
        "Connected" or "Disconnected"
    """
    return "Connected" if is_connected(device) else "Disconnected"


def sort_by_connection(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort devices with connected devices first, then alphabetically by name.

    Args:
        devices: List of device dictionaries

    Returns:
        Sorted list of devices
    """
    return sorted(devices, key=lambda d: (not is_connected(d), d.get("name", "")))
