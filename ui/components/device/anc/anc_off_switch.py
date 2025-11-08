from .anc_switch import AncSwitch


class AncOffSwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, 1, "Off", **kwargs)
