import subprocess
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Static
from textual import on
from textual.timer import Timer
from .volume_slider import VolumeSlider


class VolumeController(Vertical):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_volume = self._get_current_volume()
        self._volume_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static("[b]System Volume (click slider to adjust):[/b]")
        yield VolumeSlider(initial_value=self._current_volume)

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
            slider = self.query_one(VolumeSlider)
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
