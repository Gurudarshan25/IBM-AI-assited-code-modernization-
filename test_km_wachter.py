# test_km_wachter.py
import pytest

from km_wachter import needs_service, wear_percent, SERVICE_INTERVAL_KM, WARN_AT_PERCENT


def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False


def test_wear_percent_uses_true_division():
    # 14,900 / 15,000 is 99.33%; floor division (//) used to return 0.
    assert wear_percent(14900, 15000) == pytest.approx(99.333, abs=0.01)
    assert wear_percent(7500, 15000) == pytest.approx(50.0)


def test_threshold_boundary_is_unchanged():
    # Exactly 80% of 15,000 km (12,000 km) is due; one km less is not.
    assert SERVICE_INTERVAL_KM == 15000 and WARN_AT_PERCENT == 80
    assert needs_service({"id": "X", "odometer": 12000, "last_service_km": 0}) is True
    assert needs_service({"id": "Y", "odometer": 11999, "last_service_km": 0}) is False
