from typing import Dict, Any
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from textual.widgets import Static

from .anc_off_switch import AncOffSwitch
from .anc_transparency_switch import AncTransparencySwitch
from .anc_adaptive_switch import AncAdaptiveSwitch
from .anc_noise_cancellation_switch import AncNoiseCancellationSwitch


class AncController(Vertical):
    def __init__(self, address: str, anc: Dict[str, Any], **kwargs):
        """
        Args:
            address: Bluetooth address of the device
            anc: ANC capability data from the device
        """
        super().__init__(**kwargs)
        self._address = address
        self._anc = anc

    def compose(self) -> ComposeResult:
        yield Static("[b]ANC Mode:[/b]")

        with Horizontal():
            yield AncNoiseCancellationSwitch(self._address, self._anc, id="anc-switch-noise-cancellation")
            yield AncAdaptiveSwitch(self._address, self._anc, id="anc-switch-adaptive")
            yield AncTransparencySwitch(self._address, self._anc, id="anc-switch-transparency")
            yield AncOffSwitch(self._address, self._anc, id="anc-switch-off")
