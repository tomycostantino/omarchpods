import pytest
from components.volume.volume_controller import VolumeController, VolumeSlider


class TestVolumeController:
    def test_volume_controller_creation(self):
        controller = VolumeController()
        assert controller is not None

    def test_volume_controller_compose(self):
        controller = VolumeController()
        yielded = list(controller.compose())
        assert len(yielded) == 2


class TestVolumeSlider:
    def test_volume_slider_creation_default(self):
        slider = VolumeSlider()
        assert slider.value == 50
        assert "50%" in str(slider.render())

    def test_volume_slider_creation_custom_value(self):
        slider = VolumeSlider(initial_value=75)
        assert slider.value == 75
        assert "75%" in str(slider.render())

    def test_volume_slider_value_setter(self):
        slider = VolumeSlider()
        slider.value = 25
        assert slider.value == 25
        assert "25%" in str(slider.render())

    def test_volume_slider_value_bounds(self):
        slider = VolumeSlider()
        slider.value = -10
        assert slider.value == 0

        slider.value = 150
        assert slider.value == 100

    def test_volume_slider_display_format(self):
        slider = VolumeSlider(initial_value=42)
        display_text = str(slider.render())
        assert "┌" in display_text
        assert "┐" in display_text
        assert "42%" in display_text

    def test_volume_slider_bar_length(self):
        slider = VolumeSlider(initial_value=0)
        display_text = str(slider.render())
        assert display_text.count("░") > display_text.count("█")

        slider.value = 100
        display_text = str(slider.render())
        assert display_text.count("█") > display_text.count("░")

    def test_volume_slider_has_resize_method(self):
        slider = VolumeSlider()
        assert hasattr(slider, 'on_resize')
        slider.on_resize()

    def test_volume_slider_click_left_side(self):
        slider = VolumeSlider()
        click_event = type('ClickEvent', (), {'x': 5})()
        slider.on_click(click_event)

        assert slider.value < 25

    def test_volume_slider_click_right_side(self):
        slider = VolumeSlider()
        click_event = type('ClickEvent', (), {'x': 20})()
        slider.on_click(click_event)

        assert slider.value > 75

    def test_volume_slider_click_outside_bar(self):
        slider = VolumeSlider()
        original_value = slider.value

        click_event = type('ClickEvent', (), {'x': 0})()
        slider.on_click(click_event)

        assert slider.value == original_value
