from .anc_switch import AncSwitch
from .anc_modes import AncMode


class AncNoiseCancellationSwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, AncMode.NOISE_CANCELLATION, "ANC", **kwargs)
