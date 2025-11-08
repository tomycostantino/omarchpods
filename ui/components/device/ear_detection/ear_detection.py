from textual.widgets import Static


class EarDetection(Static):
    def __init__(self, ear_detection: dict, **kwargs):
        super().__init__(**kwargs)
        self._ear_detection = ear_detection
        self.update_display()

    def update_display(self):
        status = self._ear_detection.get("status", "Unknown")
        if status == "InEar":
            display_status = "In Ear"
        elif status == "OutOfEar":
            display_status = "Out of Ear"
        else:
            display_status = status
        self.update(f"[b]👂:[/b] {display_status}")
