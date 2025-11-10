from textual.widgets import Button


class OutputButton(Button):
    def __init__(self, sink_name: str, sink_description: str, is_default: bool, **kwargs):
        """
        Args:
            sink_name: Internal name of the sink (e.g., "alsa_output.pci-0000_00_1f.3.analog-stereo")
            sink_description: Human-readable description of the sink
            is_default: Whether this is the current default sink
        """
        super().__init__(**kwargs)
        self._sink_name = sink_name
        self._sink_description = sink_description
        self._is_default = is_default
        self._update_label()

    def _update_label(self) -> None:
        indicator = "●" if self._is_default else "○"
        self.label = f"{indicator} {self._sink_description}"

        if self._is_default:
            self.add_class("output-button-active")
            self.remove_class("output-button-inactive")
        else:
            self.add_class("output-button-inactive")
            self.remove_class("output-button-active")

    def on_button_pressed(self) -> None:
        if not self._is_default:
            self.app.set_default_output(self._sink_name)
