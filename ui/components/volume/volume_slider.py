from textual.events import Click
from textual.message import Message
from textual.widgets import Static


class VolumeSlider(Static):
    def __init__(self, initial_value: int = 50, **kwargs):
        super().__init__(**kwargs)
        self._value = initial_value
        self._bar_width = 20
        self._update_display()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int):
        self._value = max(0, min(100, new_value))
        self._update_display()

    def on_resize(self) -> None:
        available_width = self.size.width
        if available_width > 10:
            self._bar_width = available_width - 8
        else:
            self._bar_width = 20
        self._update_display()

    def _update_display(self):
        filled = int(self._value / 100 * self._bar_width)
        bar = "█" * filled + "░" * (self._bar_width - filled)
        self.update(f"┌{bar}┐ {self._value}%")

    def on_click(self, event: Click) -> None:
        bar_start = 1

        relative_x = (event.x - bar_start) / self._bar_width
        if 0 <= relative_x <= 1:
            new_volume = int(relative_x * 100)
            self.value = new_volume
            self.post_message(self.Clicked(self.value))

    class Clicked(Message):
        def __init__(self, value: int):
            self.value = value
            super().__init__()
