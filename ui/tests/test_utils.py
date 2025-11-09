from utils import is_connected, device_status_text, sort_by_connection

DEVICE_CONNECTED = {"connected": True}
DEVICE_DISCONNECTED = {"connected": False}
DEVICE_EMPTY = {}
DEVICE_CONNECTED_1 = {"connected": 1}
DEVICE_CONNECTED_YES = {"connected": "yes"}
DEVICE_CONNECTED_NONE = {"connected": None}
DEVICE_A_DISCONNECTED = {"name": "A", "connected": False}
DEVICE_B_CONNECTED = {"name": "B", "connected": True}
DEVICE_C_DISCONNECTED = {"name": "C", "connected": False}
DEVICE_ZEBRA_DISCONNECTED = {"name": "Zebra Pods", "connected": False}
DEVICE_ALPHA_DISCONNECTED = {"name": "Alpha Pods", "connected": False}
DEVICE_BETA_DISCONNECTED = {"name": "Beta Pods", "connected": False}
DEVICE_AIRPODS_CONNECTED = {"name": "AirPods", "connected": True}
DEVICE_ZEBRA_CONNECTED = {"name": "Zebra Pods", "connected": True}
DEVICE_ALPHA_CONNECTED = {"name": "Alpha Pods", "connected": True}
DEVICE_DISCONNECTED_PODS = {"name": "Disconnected Pods", "connected": False}
DEVICE_NO_NAME_CONNECTED = {"connected": True}
DEVICE_AIRPOOLS_DISCONNECTED = {"name": "airpods", "connected": False}
DEVICE_AIRPODS_PRO_DISCONNECTED = {"name": "AirPods Pro", "connected": False}


def test_is_connected():
    assert is_connected(DEVICE_CONNECTED) == True
    assert is_connected(DEVICE_DISCONNECTED) == False
    assert is_connected(DEVICE_EMPTY) == False


def test_is_connected_none_value():
    result = is_connected(DEVICE_CONNECTED_NONE)
    assert result is None
    assert not result


def test_is_connected_truthy_value():
    assert is_connected(DEVICE_CONNECTED_1) == 1
    assert is_connected(DEVICE_CONNECTED_YES) == "yes"


def test_device_status_text():
    assert device_status_text(DEVICE_CONNECTED) == "Connected"
    assert device_status_text(DEVICE_DISCONNECTED) == "Disconnected"


def test_device_status_text_empty():
    assert device_status_text(DEVICE_EMPTY) == "Disconnected"


def test_device_status_text_with_none():
    assert device_status_text(DEVICE_CONNECTED_NONE) == "Disconnected"


def test_sort_by_connection():
    devices = [
        DEVICE_A_DISCONNECTED,
        DEVICE_B_CONNECTED,
        DEVICE_C_DISCONNECTED,
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0]["name"] == "B"
    assert sorted_devices[1]["name"] == "A"
    assert sorted_devices[2]["name"] == "C"


def test_sort_by_connection_empty_list():
    devices = []
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices == []


def test_sort_by_connection_single_device():
    devices = [DEVICE_AIRPODS_CONNECTED]
    sorted_devices = sort_by_connection(devices)
    assert len(sorted_devices) == 1
    assert sorted_devices[0]["name"] == "AirPods"


def test_sort_by_connection_alphabetical():
    devices = [
        DEVICE_ZEBRA_DISCONNECTED,
        DEVICE_ALPHA_DISCONNECTED,
        DEVICE_BETA_DISCONNECTED,
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0]["name"] == "Alpha Pods"
    assert sorted_devices[1]["name"] == "Beta Pods"
    assert sorted_devices[2]["name"] == "Zebra Pods"


def test_sort_by_connection_multiple_connected():
    devices = [
        DEVICE_ZEBRA_CONNECTED,
        DEVICE_ALPHA_CONNECTED,
        DEVICE_DISCONNECTED_PODS,
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0]["name"] == "Alpha Pods"
    assert sorted_devices[1]["name"] == "Zebra Pods"
    assert sorted_devices[2]["name"] == "Disconnected Pods"


def test_sort_by_connection_missing_name():
    devices = [
        DEVICE_A_DISCONNECTED,
        DEVICE_NO_NAME_CONNECTED,
        DEVICE_B_CONNECTED,
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0].get("name", "") == ""
    assert sorted_devices[0]["connected"] == True
    assert sorted_devices[1]["name"] == "B"
    assert sorted_devices[2]["name"] == "A"


def test_sort_by_connection_case_sensitive():
    devices = [
        DEVICE_AIRPOOLS_DISCONNECTED,
        DEVICE_AIRPODS_PRO_DISCONNECTED,
    ]
    sorted_devices = sort_by_connection(devices)
    assert sorted_devices[0]["name"] == "AirPods Pro"
    assert sorted_devices[1]["name"] == "airpods"
