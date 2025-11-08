from .anc_switch import AncSwitch


class AncAdaptiveSwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, 4, "Adaptive", **kwargs)
