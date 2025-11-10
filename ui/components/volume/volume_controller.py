import subprocess
from typing import Dict, Any
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from textual.widgets import Static
from textual import on
from textual.events import Click
from textual.message import Message
from textual.timer import Timer


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


class VolumeController(Vertical):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_volume = self._get_current_volume()
        self._volume_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static("[b]🖱️ System Volume (click slider to adjust):[/b]")
        yield VolumeSlider(initial_value=self._current_volume, id="volume-slider")

    def on_mount(self) -> None:
        self._volume_timer = self.set_interval(1.0, self._check_volume_update)

    def on_unmount(self) -> None:
        if self._volume_timer:
            self._volume_timer.stop()

    @on(VolumeSlider.Clicked)
    def on_volume_changed(self, event: VolumeSlider.Clicked) -> None:
        self._set_system_volume(event.value)
        self._current_volume = event.value

    def _check_volume_update(self) -> None:
        current_system_volume = self._get_current_volume()
        if current_system_volume != self._current_volume:
            self._current_volume = current_system_volume
            slider = self.query_one("#volume-slider", VolumeSlider)
            slider.value = current_system_volume

    def _get_current_volume(self) -> int:
        try:
            result = subprocess.run(
                ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout
            if "/" in output:
                percentage = output.split("/")[1].strip().split("%")[0]
                return int(percentage)
        except (subprocess.CalledProcessError, ValueError, IndexError):
            pass
        return 50

    def _set_system_volume(self, volume: int) -> None:
        try:
            subprocess.run(
                ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume}%"],
                check=True
            )
        except subprocess.CalledProcessError:
            pass
