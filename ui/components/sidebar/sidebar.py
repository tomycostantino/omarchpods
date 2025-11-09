from typing import List, Dict, Any
from textual.reactive import reactive
from textual.widgets import Static
from textual.containers import Container, Vertical
from textual.app import ComposeResult

from .device import Device


class Sidebar(Vertical):
    device_list: List[Dict[str, Any]] = reactive([])

    def compose(self) -> ComposeResult:
        yield Static("[b]Devices[/b]", classes="sidebar-header")
        yield Container(id="device-list")

    def watch_device_list(self, device_list: List[Dict[str, Any]]) -> None:
        container = self.query_one("#device-list")
        container.remove_children()

        if not device_list:
            container.mount(Static("[dim]No devices found[/dim]"))
        else:
            for device in device_list:
                container.mount(Device(device))
