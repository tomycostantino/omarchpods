import websocket
import json
import threading
from typing import Callable, Optional

WEBSOCKET_SERVER_ADDRESS = "ws://localhost:2020"

COMMANDS = {
    "get_all":                  {"method": "GetAll"},
    "get_active_device_info":   {"method": "GetActiveDeviceInfo"},
    "connect_device":           {"method": "ConnectDevice"},
    "disconnect_device":        {"method": "DisconnectDevice"},
    "set_capabilities":         {"method": "SetCapabilities"}
}


class WebSocketClient:
    def __init__(self):
        self._server_url = WEBSOCKET_SERVER_ADDRESS
        self.ws = None
        self._listen_thread = None
        self._message_callback = None
        self._connect()

    def set_message_callback(self, callback: Callable[[dict], None]) -> None:
        self._message_callback = callback

    def connect(self) -> None:
        if self.ws is None:
            self._connect()

    def get_all(self) -> None:
        self._send(COMMANDS["get_all"])

    def get_active_device_info(self) -> None:
        self._send(COMMANDS["get_active_device_info"])

    def connect_device(self, device_address: str) -> None:
        command = COMMANDS["connect_device"]
        command["arguments"] = {"address": device_address}
        self._send(command)

    def disconnect_device(self, device_address: str) -> None:
        command = COMMANDS["disconnect_device"]
        command["arguments"] = {"address": device_address}
        self._send(command)

    def set_capabilities(self, device_address: str, capabilities: dict) -> None:
        command = COMMANDS["set_capabilities"].copy()
        command["arguments"] = {
            "address": device_address,
            "capabilities": capabilities
        }
        self._send(command)

    def _connect(self):
        try:
            self.ws = websocket.WebSocketApp(
                self._server_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            self._listen_thread = threading.Thread(
                target=self.ws.run_forever,
                daemon=True
            )
            self._listen_thread.start()
        except Exception as e:
            print(f"Connection failed: {e}")
            self.ws = None
            raise

    def _send(self, data):
        if self.ws is None:
            print("WebSocket not connected, cannot send message")
            return
        self.ws.send(json.dumps(data))

    def _on_open(self, ws):
        print("Connection opened")

    def _on_message(self, ws, message):
        print(f"Message: {message}")
        if self._message_callback:
            try:
                data = json.loads(message)
                self._message_callback(data)
            except json.JSONDecodeError:
                print(f"Failed to parse message: {message}")
        return message

    def _on_error(self, ws, error):
        print(f"Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")
