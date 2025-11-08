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
    data = reactive(None)

    def compose(self) -> ComposeResult:
        yield Container(id="device")

    def on_mount(self) -> None:
        self._display_placeholder()

    def watch_data(self, data):
        if data:
            self._data = data
            self._display_data()

    def _display_placeholder(self) -> None:
        self._clear_content_area()
        self._mount_on_content_area(
            Static("[b]Select a device from the sidebar[/b]",
                   classes="content-message")
        )

    def _display_data(self):
        self._clear_content_area()

        self._display_header()
        self._display_toggle_button()
        self._display_battery()
        self._display_ear_detection()
        self._display_anc()

    def _display_header(self):
        self._mount_on_content_area(
            Static(f"[b]{self._data['name']}[/b]", classes="device-title")
        )

    def _display_toggle_button(self):
        label = "Disconnect" if is_connected(self._data) else "Connect"
        button = ToggleConnectionButton(device=self._data, label=label)
        self._mount_on_content_area(button)

    def _display_battery(self):
        if self._data.get("capabilities", False) and self._data["capabilities"].get("battery", False):
            self._mount_on_content_area(
                BatteryIndicator(self._data["capabilities"]["battery"])
            )

    def _display_anc(self):
        if self._data.get("capabilities", False) and self._data["capabilities"].get("anc", False):
            self._mount_on_content_area(
                AncController(self._data["address"],
                              self._data["capabilities"]["anc"])
            )

    def _display_ear_detection(self):
        if self._data.get("capabilities", False) and self._data["capabilities"].get("earDetection", False):
            self._mount_on_content_area(
                EarDetection(self._data["capabilities"]["earDetection"])
            )

    def _get_content_area(self):
        return self.query_one("#device")

    def _mount_on_content_area(self, to_mount):
        content_area = self._get_content_area()
        content_area.mount(to_mount)

    def _clear_content_area(self):
        content_area = self._get_content_area()
        content_area.remove_children()
