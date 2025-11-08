from .anc_switch import AncSwitch


class AncNoiseCancellationSwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, 16, "ANC", **kwargs)
