import pytest
from main import Omarchpods


def test_app_instantiation(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', lambda self: None)
    app = Omarchpods()
    assert app is not None
    assert app.websocket_client is not None


def test_select_device(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', lambda self: None)
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._send', lambda self, data: None)
    app = Omarchpods()
    device = {"name": "Test AirPods",
              "address": "00:11:22:33:44:55", "connected": True}
    monkeypatch.setattr(app, '_update_device', lambda: None)
    app.select_device(device)
    assert app._selected_device == device


def test_toggle_connection(monkeypatch):
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._connect', lambda self: None)
    monkeypatch.setattr(
        'websocket_client.WebSocketClient._send', lambda self, data: None)
    app = Omarchpods()
    device = {"name": "Test AirPods",
              "address": "00:11:22:33:44:55", "connected": True}
    monkeypatch.setattr(app, '_update_device', lambda: None)
    app.select_device(device)

    monkeypatch.setattr(app.websocket_client,
                        'disconnect_device', lambda addr: None)
    app.toggle_device_connection(device)
