import websocket
import json
import threading
import logging
import time
from typing import Callable, Optional

WEBSOCKET_SERVER_ADDRESS = "ws://localhost:2020"
RECONNECT_DELAY_SECONDS = 5
MAX_RECONNECT_ATTEMPTS = 3

logger = logging.getLogger(__name__)

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
        self._should_reconnect = True
        self._reconnect_attempts = 0
        self._connect()

    def set_message_callback(self, callback: Callable[[dict], None]) -> None:
        """
        Set the callback function for received messages.

        Args:
            callback: Function to call when a message is received
        """
        self._message_callback = callback

    def get_all(self) -> None:
        self._send(COMMANDS["get_all"])

    def get_active_device_info(self) -> None:
        self._send(COMMANDS["get_active_device_info"])

    def connect_device(self, device_address: str) -> None:
        """
        Args:
            device_address: Bluetooth address of the device to connect
        """
        command = COMMANDS["connect_device"].copy()
        command["arguments"] = {"address": device_address}
        self._send(command)

    def disconnect_device(self, device_address: str) -> None:
        """
        Args:
            device_address: Bluetooth address of the device to disconnect
        """
        command = COMMANDS["disconnect_device"].copy()
        command["arguments"] = {"address": device_address}
        self._send(command)

    def set_capabilities(self, device_address: str, capabilities: dict) -> None:
        """
        Args:
            device_address: Bluetooth address of the device
            capabilities: Dictionary of capabilities to set
        """
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
            logger.error(f"Connection failed: {e}")
            self.ws = None
            raise

    def _send(self, data):
        if self.ws is None:
            logger.warning("WebSocket not connected, cannot send message")
            return
        self.ws.send(json.dumps(data))

    def _on_open(self, ws):
        logger.info("WebSocket connection opened")

    def _on_message(self, ws, message):
        logger.debug(f"Received message: {message}")
        if self._message_callback:
            try:
                data = json.loads(message)
                self._message_callback(data)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse message: {message}")
        return message

    def _on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """
        Args:
            ws: WebSocket instance
            close_status_code: Close status code
            close_msg: Close message
        """
        logger.info(f"WebSocket connection closed: {
                    close_status_code} - {close_msg}")

        if self._should_reconnect and self._reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
            self._reconnect_attempts += 1
            logger.info(f"Attempting to reconnect ({
                        self._reconnect_attempts}/{MAX_RECONNECT_ATTEMPTS})...")
            time.sleep(RECONNECT_DELAY_SECONDS)
            try:
                self._connect()
                self._reconnect_attempts = 0  # Reset on successful connection
            except Exception as e:
                logger.error(f"Reconnection attempt failed: {e}")
        elif self._reconnect_attempts >= MAX_RECONNECT_ATTEMPTS:
            logger.error("Max reconnection attempts reached. Giving up.")

    def close(self) -> None:
        """Close the WebSocket connection and stop reconnection attempts."""
        self._should_reconnect = False
        if self.ws:
            self.ws.close()
