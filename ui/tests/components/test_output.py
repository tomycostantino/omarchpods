import pytest
from unittest.mock import Mock, patch
from components.output.output_button import OutputButton
from components.output.output_selector import OutputSelector


class TestOutputButton:
    def test_creation(self):
        button = OutputButton("test_sink", "Test Sink", True)
        assert button._sink_name == "test_sink"
        assert button._is_default is True

    def test_label_shows_active_indicator(self):
        button = OutputButton("test_sink", "Test Sink", True)
        label_text = str(button.label)
        assert "●" in label_text
        assert "Test Sink" in label_text

    def test_label_shows_inactive_indicator(self):
        button = OutputButton("test_sink", "Test Sink", False)
        assert "○" in str(button.label)

    def test_active_has_success_class(self):
        button = OutputButton("test_sink", "Test Sink", True)
        assert button.has_class("output-button-active")

    def test_inactive_has_panel_class(self):
        button = OutputButton("test_sink", "Test Sink", False)
        assert button.has_class("output-button-inactive")

    def test_press_inactive_triggers_action(self):
        button = OutputButton("test_sink", "Test Sink", False)
        assert button._is_default is False
        assert button._sink_name == "test_sink"

    def test_press_active_is_default(self):
        button = OutputButton("test_sink", "Test Sink", True)
        assert button._is_default is True


class TestOutputSelector:
    def test_creation(self):
        selector = OutputSelector()
        assert selector._outputs == []
        assert selector._default_sink is None

    def test_compose_yields_two_widgets(self):
        selector = OutputSelector()
        yielded = list(selector.compose())
        assert len(yielded) == 2

    def test_timer_starts_on_mount(self):
        selector = OutputSelector()
        selector.set_interval = Mock(return_value=Mock())
        selector._refresh_outputs = Mock()
        selector.on_mount()
        selector.set_interval.assert_called_once_with(
            2.0, selector._refresh_outputs)

    def test_timer_stops_on_unmount(self):
        selector = OutputSelector()
        mock_timer = Mock()
        selector._output_timer = mock_timer
        selector.on_unmount()
        mock_timer.stop.assert_called_once()

    @patch('subprocess.run')
    def test_get_outputs_parses_pactl_output(self, mock_run):
        mock_run.return_value.stdout = "0\tsink1\tmodule\n1\tsink2\tmodule\n"
        selector = OutputSelector()
        selector._get_sink_description = lambda x: f"Desc {x}"
        outputs = selector._get_outputs()
        assert len(outputs) == 2
        assert outputs[0] == ("sink1", "Desc sink1")

    @patch('subprocess.run')
    def test_get_outputs_handles_error(self, mock_run):
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, 'pactl')
        selector = OutputSelector()
        assert selector._get_outputs() == []

    @patch('subprocess.run')
    def test_get_default_sink_returns_name(self, mock_run):
        mock_run.return_value.stdout = "default_sink\n"
        selector = OutputSelector()
        assert selector._get_default_sink() == "default_sink"

    @patch('subprocess.run')
    def test_get_default_sink_handles_error(self, mock_run):
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, 'pactl')
        selector = OutputSelector()
        assert selector._get_default_sink() == ""

    @patch('subprocess.run')
    def test_get_sink_description_extracts_description(self, mock_run):
        mock_run.return_value.stdout = "Name: test\n\tDescription: Test Device\n"
        selector = OutputSelector()
        assert selector._get_sink_description("test") == "Test Device"

    @patch('subprocess.run')
    def test_get_sink_description_falls_back_to_name(self, mock_run):
        mock_run.return_value.stdout = "Name: test\n"
        selector = OutputSelector()
        assert selector._get_sink_description("test") == "test"

    def test_refresh_updates_when_outputs_change(self):
        selector = OutputSelector()
        selector._get_outputs = Mock(return_value=[("sink1", "Sink 1")])
        selector._get_default_sink = Mock(return_value="sink1")
        selector._update_output_buttons = Mock()
        selector._refresh_outputs()
        assert selector._outputs == [("sink1", "Sink 1")]
        selector._update_output_buttons.assert_called_once()

    def test_refresh_skips_update_when_unchanged(self):
        selector = OutputSelector()
        selector._outputs = [("sink1", "Sink 1")]
        selector._default_sink = "sink1"
        selector._get_outputs = Mock(return_value=[("sink1", "Sink 1")])
        selector._get_default_sink = Mock(return_value="sink1")
        selector._update_output_buttons = Mock()
        selector._refresh_outputs()
        selector._update_output_buttons.assert_not_called()

    def test_update_buttons_clears_and_mounts(self):
        selector = OutputSelector()
        selector._outputs = [("sink1", "Sink 1")]
        selector._default_sink = "sink1"
        mock_container = Mock()
        selector.query_one = Mock(return_value=mock_container)
        selector._update_output_buttons()
        mock_container.remove_children.assert_called_once()
        mock_container.mount.assert_called_once()
