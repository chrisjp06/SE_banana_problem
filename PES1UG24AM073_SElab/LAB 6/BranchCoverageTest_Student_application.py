"""Decision and branch coverage tests for the supplied Lab 6 module."""

import pytest

from amusement_park_ride_access import inspect_safety_restraints, process_ride_admissions


def test_validation_branches():
    with pytest.raises(ValueError):
        process_ride_admissions(None, 0.0)  # Invalid type; short-circuits the OR.
    with pytest.raises(ValueError):
        process_ride_admissions([], -0.01)  # Valid type, invalid fee.
    assert process_ride_admissions([], 0.0)["status"] == "ZERO_ADMISSIONS"


def test_group_open_default_and_all_ride_type_decisions():
    groups = [
        {},
        {"is_open": True, "ride_type": "roller_coaster", "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "water_ride", "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "family", "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "unknown"},
    ]
    assert process_ride_admissions(groups, 0.0) == {
        "total_revenue": 53.0, "status": "COMPLETED"
    }


def test_patron_decisions_and_fast_lane_default_and_enabled():
    groups = [
        {"is_open": True, "ride_type": "family", "patrons": [
            {},  # height <= 0
            {"height_cm": 110},  # height > 0 but below minimum
            {"height_cm": 150, "health_warning": True},  # warning, non-coaster
            {"height_cm": 130, "is_child": True},  # child fare
            {"height_cm": 150},  # adult fare
        ]},
        {"is_open": True, "ride_type": "water_ride", "has_fast_lane": True,
         "patrons": [{"height_cm": 150}]},
    ]
    assert process_ride_admissions(groups, 4.0) == {
        "total_revenue": 38.0, "status": "COMPLETED"
    }


def test_coaster_health_warning_breaks_group_and_fast_lane_still_charged():
    groups = [{"is_open": True, "ride_type": "roller_coaster", "has_fast_lane": True,
               "patrons": [{"height_cm": 150}, {"height_cm": 160, "health_warning": True}]}]
    assert process_ride_admissions(groups, 2.5) == {
        "total_revenue": 2.5, "status": "COMPLETED"
    }


def test_rejection_threshold_and_zero_revenue_decisions():
    audit = process_ride_admissions(
        [{"is_open": True, "ride_type": "family", "patrons": [{"height_cm": 0}] * 5}], 0.0
    )
    assert audit["status"] == "SAFETY_AUDIT"
    assert process_ride_admissions([{"is_open": True, "ride_type": "family",
                                     "patrons": [{"height_cm": 150, "health_warning": True}]}],
                                   0.0)["status"] == "ZERO_ADMISSIONS"


def test_restraint_branches_include_reset_and_emergency():
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints([[0, 1, 0]]) == "SAFE"
    assert inspect_safety_restraints([[1, 0, 0]]) == "EMERGENCY_LOCK"
    assert inspect_safety_restraints([[], [0, 0]]) == "EMERGENCY_LOCK"
