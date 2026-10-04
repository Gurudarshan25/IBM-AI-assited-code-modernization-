# test_fleet_report.py
import pytest

from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_survives_car_without_reading():
    # VOS-7788 (as in fleet_sample.json) has no "last_service_km": the report must not crash,
    # must not count it as due, and must leave it out of the average instead of treating it as 0.
    fleet = SAMPLE + [{"id": "VOS-7788", "odometer": 92000}]
    s = fleet_summary(fleet)
    assert s["count"] == 3
    assert s["due"] == 1
    assert s["no_reading"] == 1
    assert s["average_wear"] == pytest.approx(fleet_summary(SAMPLE)["average_wear"])


def test_average_wear_uses_true_division():
    # 99.33% and 20% average to 59.67%, not the floored 59 (or 0 from floored wear).
    fleet = [
        {"id": "A", "odometer": 14900, "last_service_km": 0},
        {"id": "B", "odometer": 3000, "last_service_km": 0},
    ]
    assert fleet_summary(fleet)["average_wear"] == pytest.approx(59.667, abs=0.01)


def test_empty_fleet_does_not_divide_by_zero():
    assert fleet_summary([])["average_wear"] == 0.0
