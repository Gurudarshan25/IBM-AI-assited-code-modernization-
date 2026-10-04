# test_helpers.py
import pytest

import fleet_utils
from config_loader import load_settings, get_int


def test_km_to_miles():
    # 100 km is about 62.1 miles (the old factor 1.609 gave 160.9).
    assert fleet_utils.km_to_miles(100) == pytest.approx(62.1371, abs=0.001)


def test_settings_rules_match_code():
    s = load_settings()
    assert get_int(s, "service_interval_km", -1) == 15000
    assert get_int(s, "warn_at_percent", -1) == 80


def test_value_containing_equals_sign_is_kept(tmp_path):
    cfg = tmp_path / "settings.cfg"
    cfg.write_text("report_title = A=B\n", encoding="utf-8")
    assert load_settings(str(cfg))["report_title"] == "A=B"
