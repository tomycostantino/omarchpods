import pytest
from main import Omarchpods


def MOCK_CONNECT(self): return None
def MOCK_SEND(self, data): return None


TEST_DEVICE_CONNECTED = {"name": "Test AirPods",
                         "address": "00:11:22:33:44:55", "connected": True}
TEST_DEVICE_DISCONNECTED = {"name": "Test AirPods",
                            "address": "00:11:22:33:44:55", "connected": False}
TEST_DEVICE_1 = {"name": "AirPods 1",
                 "address": "AA:BB:CC:DD:EE:FF", "connected": True}
TEST_DEVICE_2 = {"name": "AirPods 2",
                 "address": "11:22:33:44:55:66", "connected": True}
TEST_ADDRESS = "AA:BB:CC:DD:EE:FF"
TEST_DEVICE_BASE = {"name": "Test", "address": TEST_ADDRESS}
TEST_DEVICE_LIST_DISCONNECTED = [
    {"name": "Test", "address": TEST_ADDRESS, "connected": False}]
TEST_DEVICE_LIST_CONNECTED = [
    {"name": "Test", "address": TEST_ADDRESS, "connected": True}]
TEST_ADDRESS = "AA:BB:CC:DD:EE:FF"


def test_app_instantiation(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()
    assert app is not None
    assert app.websocket_client is not None


def test_select_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()
    monkeypatch.setattr(app, '_update_device', lambda: None)
    app.select_device(TEST_DEVICE_CONNECTED)
    assert app._selected_device == TEST_DEVICE_CONNECTED


def test_select_device_invalid(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app.select_device(None)
    assert app._selected_device is None

    app.select_device({"name": "Test"})
    assert app._selected_device is None


def test_select_device_same_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()

    update_count = [0]

    def mock_update():
        update_count[0] += 1

    monkeypatch.setattr(app, '_update_device', mock_update)

    app.select_device(TEST_DEVICE_CONNECTED)
    assert update_count[0] == 1

    app.select_device(TEST_DEVICE_CONNECTED)
    assert update_count[0] == 1


def test_select_device_different_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()

    monkeypatch.setattr(app, '_update_device', lambda: None)

    app.select_device(TEST_DEVICE_1)
    assert app._selected_device == TEST_DEVICE_1

    app.select_device(TEST_DEVICE_2)
    assert app._selected_device == TEST_DEVICE_2


def test_toggle_connection(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()
    monkeypatch.setattr(app, '_update_device', lambda: None)
    app.select_device(TEST_DEVICE_CONNECTED)

    monkeypatch.setattr(app.websocket_client,
                        'disconnect_device', lambda addr: None)
    app.toggle_device_connection(TEST_DEVICE_CONNECTED)


def test_toggle_connection_disconnected_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()

    connect_called = [False]

    def mock_connect(addr):
        connect_called[0] = True

    monkeypatch.setattr(app.websocket_client, 'connect_device', mock_connect)
    app.toggle_device_connection(TEST_DEVICE_DISCONNECTED)
    assert connect_called[0]


def test_toggle_connection_invalid_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app.toggle_device_connection(None)

    app.toggle_device_connection({"name": "Test"})


def test_set_anc_mode(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    monkeypatch.setattr('websocket_client.WebSocketClient._send', MOCK_SEND)
    app = Omarchpods()

    capabilities_sent = []

    def mock_set_capabilities(addr, caps):
        capabilities_sent.append((addr, caps))

    monkeypatch.setattr(app.websocket_client,
                        'set_capabilities', mock_set_capabilities)

    test_capabilities = {"anc": {"mode": "NoiseCancellation"}}

    app.set_anc_mode(TEST_ADDRESS, test_capabilities)
    assert capabilities_sent == [(TEST_ADDRESS, test_capabilities)]


def test_selected_device_disconnected_true(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = TEST_DEVICE_CONNECTED.copy()
    app._selected_device["address"] = TEST_ADDRESS

    device_list = TEST_DEVICE_LIST_DISCONNECTED

    assert app._selected_device_disconnected(device_list) is True


def test_selected_device_disconnected_false_if_not_in_list(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = TEST_DEVICE_CONNECTED.copy()
    app._selected_device["address"] = TEST_ADDRESS

    device_list = [
        {"name": "Other", "address": "11:22:33:44:55:66", "connected": False}]

    assert app._selected_device_disconnected(device_list) is False


def test_selected_device_disconnected_false_if_no_selected(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = None
    device_list = TEST_DEVICE_LIST_DISCONNECTED

    assert app._selected_device_disconnected(device_list) is False


def test_selected_device_disconnected_false_if_still_connected(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = {"name": "Test",
                            "address": "AA:BB:CC:DD:EE:FF", "connected": True}

    device_list = TEST_DEVICE_LIST_CONNECTED

    assert app._selected_device_disconnected(device_list) is False


def test_merge_info_data(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = TEST_DEVICE_BASE
    monkeypatch.setattr(app, '_update_device', lambda: None)

    info = {"address": "AA:BB:CC:DD:EE:FF",
            "capabilities": {"battery": {"left": 85}}}
    app._merge_info_data(info)

    assert "capabilities" in app._selected_device
    assert app._selected_device["capabilities"]["battery"]["left"] == 85
    assert app._selected_device["name"] == "Test"


def test_handle_websocket_message_headphones(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    update_called = [False]

    def mock_update_list(devices):
        update_called[0] = True

    def mock_call_from_thread(callback, *args, **kwargs):
        callback(*args, **kwargs)

    monkeypatch.setattr(app, 'call_from_thread', mock_call_from_thread)
    monkeypatch.setattr(app, '_update_device_list', mock_update_list)

    message = {"headphones": [
        {"name": "Test", "address": "AA:BB:CC:DD:EE:FF"}]}
    app._handle_websocket_message(message)

    assert update_called[0]


def test_handle_websocket_message_info(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = TEST_DEVICE_BASE

    merge_called = [False]

    def mock_merge(info):
        merge_called[0] = True

    def mock_call_from_thread(callback, *args, **kwargs):
        callback(*args, **kwargs)

    monkeypatch.setattr(app, 'call_from_thread', mock_call_from_thread)
    monkeypatch.setattr(app, '_merge_info_data', mock_merge)

    message = {"info": {"address": "AA:BB:CC:DD:EE:FF", "capabilities": {}}}
    app._handle_websocket_message(message)

    assert merge_called[0]


def test_handle_websocket_message_info_wrong_address(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = TEST_DEVICE_BASE

    merge_called = [False]

    def mock_merge(info):
        merge_called[0] = True

    monkeypatch.setattr(app, '_merge_info_data', mock_merge)

    message = {"info": {"address": "11:22:33:44:55:66", "capabilities": {}}}
    app._handle_websocket_message(message)

    assert not merge_called[0]


def test_handle_websocket_message_disconnect_update(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', MOCK_CONNECT)
    app = Omarchpods()

    app._selected_device = {"name": "Test",
                            "address": "AA:BB:CC:DD:EE:FF", "connected": True}

    update_called = [False]

    def mock_update():
        update_called[0] = True

    def mock_call_from_thread(callback, *args, **kwargs):
        callback(*args, **kwargs)

    monkeypatch.setattr(app, 'call_from_thread', mock_call_from_thread)
    monkeypatch.setattr(app, '_update_device', mock_update)
    monkeypatch.setattr(app, '_update_device_list', lambda devices: None)

    message = {"headphones": [
        {"name": "Test", "address": "AA:BB:CC:DD:EE:FF", "connected": False}]}
    app._handle_websocket_message(message)

    assert app._selected_device["connected"] is False
    assert update_called[0]
