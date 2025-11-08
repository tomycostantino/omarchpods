from .anc_switch import AncSwitch


class AncTransparencySwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, 2, "Transparency", **kwargs)
