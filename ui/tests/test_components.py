import pytest
from components.device.battery import BatteryIndicator
from components.device.ear_detection import EarDetection

BATTERY_SINGLE = {"single": {"battery": 85, "charging": False}}
BATTERY_LEFT_RIGHT = {"left": {"battery": 80, "charging": False}, "right": {
    "battery": 75, "charging": False}}
BATTERY_WITH_CASE = {"case": {"battery": 100, "charging": True}, "left": {
    "battery": 50, "charging": False}, "right": {"battery": 50, "charging": False}}
BATTERY_CHARGING = {"single": {"battery": 45, "charging": True}}
BATTERY_ZERO_LEFT = {"left": {"battery": 0, "charging": False},
                     "right": {"battery": 85, "charging": False}}
BATTERY_ALL_PARTS = {"case": {"battery": 100, "charging": False}, "left": {"battery": 80, "charging": False}, "right": {
    "battery": 75, "charging": False}, "single": {"battery": 90, "charging": False}}
BATTERY_MISSING_CHARGING = {"single": {"battery": 50}}
BATTERY_EMPTY = {}

EAR_DETECTION_IN_EAR = {"status": "InEar"}
EAR_DETECTION_OUT_OF_EAR = {"status": "OutOfEar"}
EAR_DETECTION_IN_CASE = {"status": "InCase"}
EAR_DETECTION_UNKNOWN = {"status": "Unknown"}
EAR_DETECTION_MISSING = {}


class TestBatteryIndicator:
    def test_battery_indicator_single(self):
        indicator = BatteryIndicator(BATTERY_SINGLE)
        text = indicator._get_battery_text()
        assert "[b]Battery:[/b]" in text
        assert "Single: 85%" in text
        assert "(Charging)" not in text

    def test_battery_indicator_left_right(self):
        indicator = BatteryIndicator(BATTERY_LEFT_RIGHT)
        text = indicator._get_battery_text()
        assert "Left: 80%" in text
        assert "Right: 75%" in text

    def test_battery_indicator_with_case(self):
        indicator = BatteryIndicator(BATTERY_WITH_CASE)
        text = indicator._get_battery_text()
        assert "Case: 100% (Charging)" in text
        assert "Left: 50%" in text
        assert "Right: 50%" in text

    def test_battery_indicator_charging(self):
        indicator = BatteryIndicator(BATTERY_CHARGING)
        text = indicator._get_battery_text()
        assert "Single: 45% (Charging)" in text

    def test_battery_indicator_zero_battery_excluded(self):
        indicator = BatteryIndicator(BATTERY_ZERO_LEFT)
        text = indicator._get_battery_text()
        assert "Left" not in text
        assert "Right: 85%" in text

    def test_battery_indicator_all_parts(self):
        indicator = BatteryIndicator(BATTERY_ALL_PARTS)
        text = indicator._get_battery_text()
        assert "Case: 100%" in text
        assert "Left: 80%" in text
        assert "Right: 75%" in text
        assert "Single: 90%" in text

    def test_battery_indicator_missing_charging_field(self):
        indicator = BatteryIndicator(BATTERY_MISSING_CHARGING)
        text = indicator._get_battery_text()
        assert "Single: 50%" in text
        assert "(Charging)" not in text

    def test_battery_indicator_empty(self):
        indicator = BatteryIndicator(BATTERY_EMPTY)
        text = indicator._get_battery_text()
        assert text == "[b]Battery:[/b]\n"


class TestEarDetection:
    def test_ear_detection_in_ear(self):
        component = EarDetection(EAR_DETECTION_IN_EAR)
        assert "In Ear" in str(component.render())

    def test_ear_detection_out_of_ear(self):
        component = EarDetection(EAR_DETECTION_OUT_OF_EAR)
        assert "Out of Ear" in str(component.render())

    def test_ear_detection_in_case(self):
        component = EarDetection(EAR_DETECTION_IN_CASE)
        assert "In Case" in str(component.render())

    def test_ear_detection_unknown(self):
        component = EarDetection(EAR_DETECTION_UNKNOWN)
        text = str(component.render())
        assert "Unknown" in text

    def test_ear_detection_missing_status(self):
        component = EarDetection(EAR_DETECTION_MISSING)
        text = str(component.render())
        assert "Unknown" in text
