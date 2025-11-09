from websocket_client import WebSocketClient
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Static
from textual.binding import Binding

from components.sidebar import Sidebar
from components.device import Device
from utils import sort_by_connection, is_connected

APPLICATION_TITLE = """
 ██████╗ ███╗   ███╗ █████╗ ██████╗  ██████╗██╗  ██╗██████╗  ██████╗ ██████╗ ███████╗
██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██║   ██║██╔████╔██║███████║██████╔╝██║     ███████║██████╔╝██║   ██║██║  ██║███████╗
██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗██║     ██╔══██║██╔═══╝ ██║   ██║██║  ██║╚════██║
╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗██║  ██║██║     ╚██████╔╝██████╔╝███████║
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═════╝ ╚══════╝
"""


class Omarchpods(App):
    CSS_PATH = "main.css"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.websocket_client = WebSocketClient()
        self.websocket_client.set_message_callback(
            self._handle_websocket_message)

        self._selected_device = None

    def compose(self) -> ComposeResult:
        yield Static(APPLICATION_TITLE, id="ascii-header")
        with Horizontal():
            yield Sidebar()
            yield Device()
        yield Footer()

    def on_mount(self) -> None:
        try:
            self.websocket_client.get_all()
        except Exception as e:
            self.notify(f"Failed to connect to server: {e}", severity="error")

    def select_device(self, device):
        is_different_device = (
            self._selected_device is None or
            self._selected_device["address"] != device["address"]
        )

        self._selected_device = device

        if is_different_device:
            self._update_device()
            self.websocket_client.get_all()

    def toggle_device_connection(self, device):
        if is_connected(device):
            self.websocket_client.disconnect_device(device["address"])
            self.notify(f"Disconnecting from {device["name"]}")
        else:
            self.websocket_client.connect_device(device["address"])
            self.notify(f"Connecting to {device["name"]}")

    def set_anc_mode(self, address, capabilities):
        self.websocket_client.set_capabilities(address, capabilities)
        self.notify(f"Setting ANC capabilities")

    def _handle_websocket_message(self, data: dict) -> None:
        if "headphones" in data:
            headphones = data["headphones"]
            self.call_from_thread(self._update_device_list, headphones)
            if self._selected_device_disconnected(headphones):
                self._selected_device["connected"] = False
                self._update_device()

        if "info" in data:
            info = data["info"]
            if self._selected_device and info.get("address") == self._selected_device.get("address"):
                self.call_from_thread(self._merge_info_data, info)

    def _selected_device_disconnected(self, device_list):
        for device in device_list:
            if (
                device["address"] == self._selected_device["address"]
                and device["connected"] is False
                and self._selected_device["connected"]
            ):
                return True

    def _merge_info_data(self, info: dict):
        self._selected_device = {**self._selected_device, **info}
        self._update_device()

    def _update_device_list(self, device_list: list) -> None:
        sorted_devices = sort_by_connection(device_list)
        self.query_one(Sidebar).device_list = sorted_devices

        if sorted_devices:
            first_device = sorted_devices[0]
            should_auto_select = self._selected_device is None

            if should_auto_select and is_connected(first_device):
                self.select_device(first_device)

    def _update_device(self) -> None:
        device = self.query_one(Device)
        # Deeply mutate it so it is re rendered
        device.data = {
            **self._selected_device} if self._selected_device else None


def main():
    app = Omarchpods()
    app.run()


if __name__ == "__main__":
    main()
