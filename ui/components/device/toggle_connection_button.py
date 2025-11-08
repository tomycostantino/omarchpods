from textual.widgets import Button


class ToggleConnectionButton(Button):
    def __init__(self, device: dict, label: str, **kwargs):
        super().__init__(label=label, **kwargs)
        self._device = device
        self.add_class("device-button")

    def on_button_pressed(self) -> None:
        if self._device:
            self.app.toggle_device_connection(self._device)
