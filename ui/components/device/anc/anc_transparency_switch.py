from .anc_switch import AncSwitch
from .anc_modes import AncMode


class AncTransparencySwitch(AncSwitch):
    def __init__(self, address: str, anc: dict, **kwargs):
        super().__init__(address, anc, AncMode.TRANSPARENCY, "Transparency", **kwargs)
