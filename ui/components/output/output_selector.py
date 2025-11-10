import subprocess
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from textual.widgets import Static
from textual.timer import Timer
from .output_button import OutputButton


class OutputSelector(Vertical):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._outputs = []
        self._default_sink = None
        self._output_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static("[b]Output Device:[/b]")
        yield Horizontal(id="output-buttons-container")

    def on_mount(self) -> None:
        self._refresh_outputs()
        self._output_timer = self.set_interval(2.0, self._refresh_outputs)

    def on_unmount(self) -> None:
        if self._output_timer:
            self._output_timer.stop()

    def _refresh_outputs(self) -> None:
        outputs = self._get_outputs()
        default_sink = self._get_default_sink()

        if outputs != self._outputs or default_sink != self._default_sink:
            self._outputs = outputs
            self._default_sink = default_sink
            self._update_output_buttons()

    def _update_output_buttons(self) -> None:
        container = self.query_one("#output-buttons-container")
        container.remove_children()

        for sink_name, sink_description in self._outputs:
            is_default = sink_name == self._default_sink
            button = OutputButton(
                sink_name=sink_name,
                sink_description=sink_description,
                is_default=is_default
            )
            container.mount(button)

    def _get_outputs(self) -> list:
        try:
            result = subprocess.run(
                ["pactl", "list", "short", "sinks"],
                capture_output=True,
                text=True,
                check=True
            )

            outputs = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        sink_name = parts[1]
                        description = self._get_sink_description(sink_name)
                        outputs.append((sink_name, description))

            return outputs
        except (subprocess.CalledProcessError, ValueError, IndexError):
            return []

    def _get_sink_description(self, sink_name: str) -> str:
        try:
            result = subprocess.run(
                ["pactl", "list", "sinks"],
                capture_output=True,
                text=True,
                check=True
            )

            lines = result.stdout.split('\n')
            found_sink = False

            for i, line in enumerate(lines):
                if f"Name: {sink_name}" in line:
                    found_sink = True
                elif found_sink and "Description:" in line:
                    description = line.split("Description:", 1)[1].strip()
                    return description
                elif found_sink and line.startswith("Sink #"):
                    break

            return sink_name
        except (subprocess.CalledProcessError, ValueError, IndexError):
            return sink_name

    def _get_default_sink(self) -> str:
        try:
            result = subprocess.run(
                ["pactl", "get-default-sink"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
