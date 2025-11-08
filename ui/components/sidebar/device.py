from textual.widgets import Button

from utils import device_status_text


class Device(Button):
    def __init__(self, device: dict, **kwargs):
        self._device = device
        label = f"{device['name']}\n[dim]{device_status_text(device)}[/dim]"

        super().__init__(label, **kwargs)
        self.add_class("device-button")

    def on_button_pressed(self) -> None:
        self.app.select_device(self._device)
