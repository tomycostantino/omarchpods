from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Static


class BatteryIndicator(Vertical):
    def __init__(self, battery: dict, **kwargs):
        super().__init__(**kwargs)
        self._battery = battery

    def compose(self) -> ComposeResult:
        battery_text = self._get_battery_text()
        yield Static(battery_text, id="battery-display")

    def _get_battery_text(self) -> str:
        battery_text = "[b]Battery:[/b]\n"
        for part in ['case', 'left', 'right', 'single']:
            if part in self._battery:
                b = self._battery[part]
                if b['battery'] > 0:
                    status = "(Charging)" if b['charging'] else ""
                    battery_text += f"  {part.capitalize()
                                         }: {b['battery']}% {status}\n"
        return battery_text
