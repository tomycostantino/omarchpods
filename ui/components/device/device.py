from typing import Optional, Dict, Any
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from textual.reactive import reactive

from .toggle_connection_button import ToggleConnectionButton
from .anc import AncController
from .battery import BatteryIndicator
from .ear_detection import EarDetection
from utils import is_connected


class Device(Vertical):
    data: Optional[Dict[str, Any]] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Container(id="device")

    def on_mount(self) -> None:
        self._display_placeholder()

    def watch_data(self, data: Optional[Dict[str, Any]]) -> None:
        """
        Args:
            data: Device data dictionary containing device information and capabilities
        """
        if data:
            self._data = data
            self._display_data()

    def _display_placeholder(self) -> None:
        self._clear_content_area()
        self._mount_on_content_area(
            Static("[b]Select a device from the sidebar[/b]",
                   classes="content-message")
        )

    def _display_data(self) -> None:
        self._clear_content_area()

        self._display_header()
        self._display_toggle_button()
        self._display_battery()
        self._display_ear_detection()
        self._display_anc()

    def _display_header(self) -> None:
        device_name = self._data.get('name', 'Unknown Device')
        self._mount_on_content_area(
            Static(f"[b]{device_name}[/b]", classes="device-title")
        )

    def _display_toggle_button(self) -> None:
        label = "Disconnect" if is_connected(self._data) else "Connect"
        button = ToggleConnectionButton(device=self._data, label=label)
        self._mount_on_content_area(button)

    def _display_battery(self) -> None:
        capabilities = self._data.get("capabilities", {})
        battery = capabilities.get("battery")

        if battery:
            self._mount_on_content_area(BatteryIndicator(battery))

    def _display_ear_detection(self) -> None:
        capabilities = self._data.get("capabilities", {})
        ear_detection = capabilities.get("earDetection")

        if ear_detection:
            self._mount_on_content_area(EarDetection(ear_detection))

    def _display_anc(self) -> None:
        capabilities = self._data.get("capabilities", {})
        anc = capabilities.get("anc")

        if anc and "address" in self._data:
            self._mount_on_content_area(
                AncController(self._data["address"], anc)
            )

    def _get_content_area(self) -> Container:
        return self.query_one("#device", Container)

    def _mount_on_content_area(self, to_mount) -> None:
        """
        Args:
            to_mount: Widget to mount
        """
        content_area = self._get_content_area()
        content_area.mount(to_mount)

    def _clear_content_area(self) -> None:
        content_area = self._get_content_area()
        content_area.remove_children()
