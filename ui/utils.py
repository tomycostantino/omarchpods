def is_connected(device: dict) -> bool:
    return device.get("connected", False)


def device_status_text(device: dict) -> str:
    return "Connected" if is_connected(device) else "Disconnected"


def sort_by_connection(devices: list[dict]) -> list[dict]:
    return sorted(devices, key=lambda d: (not is_connected(d), d.get("name", "")))