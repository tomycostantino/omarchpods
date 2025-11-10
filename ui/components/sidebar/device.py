from typing import Dict, Any
from textual.widgets import Button

from utils import device_status_text


class Device(Button):
    def __init__(self, device: Dict[str, Any], **kwargs):
        """
        Args:
            device: Device data dictionary containing name and connection info
        """
        self._device = device
        device_name = device.get('name', 'Unknown Device')
        label = f"{device_name}\n[dim]{device_status_text(device)}[/dim]"

        super().__init__(label, **kwargs)

    def on_button_pressed(self) -> None:
        self.app.select_device(self._device)
