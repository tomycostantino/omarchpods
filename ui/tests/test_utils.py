from utils import is_connected, device_status_text, sort_by_connection


def test_is_connected():
    assert is_connected({"connected": True}) == True
    assert is_connected({"connected": False}) == False
    assert is_connected({}) == False


def test_device_status_text():
    assert device_status_text({"connected": True}) == "Connected"
    assert device_status_text({"connected": False}) == "Disconnected"


def test_sort_by_connection():
    devices = [
        {"name": "A", "connected": False},
        {"name": "B", "connected": True},
        {"name": "C", "connected": False},
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0]["name"] == "B"
    assert sorted_devices[1]["name"] == "A"
    assert sorted_devices[2]["name"] == "C"
