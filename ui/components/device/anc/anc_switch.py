from textual.widgets import Button


class AncSwitch(Button):
    def __init__(self, address: str, anc: dict, mode_value: int, mode_name: str, **kwargs):
        super().__init__(**kwargs)
        self._address = address
        self._anc = anc
        self._mode_value = mode_value
        self._mode_name = mode_name
        self.add_class("anc-switch")
        self._update_label()

    def _update_label(self) -> None:
        if not self._address or not self._anc:
            return

        selected = self._anc.get("selected", 0)
        readonly = self._anc.get("readonly", True)
        options = self._anc.get("options", 0)

        available = (options & self._mode_value) != 0
        is_active = selected == self._mode_value
        indicator = "●" if is_active else "○"
        label = f"{indicator} {self._mode_name}"

        self.label = label

        if is_active:
            self.add_class("anc-switch-active")
            self.remove_class("anc-switch-inactive")
        else:
            self.add_class("anc-switch-inactive")
            self.remove_class("anc-switch-active")

        self.disabled = readonly or not available

    def on_button_pressed(self) -> None:
        if self._address and self._anc and not self.disabled:
            capabilities = {
                "anc": {
                    "selected": self._mode_value
                }
            }
            self.app.set_anc_mode(self._address, capabilities)
