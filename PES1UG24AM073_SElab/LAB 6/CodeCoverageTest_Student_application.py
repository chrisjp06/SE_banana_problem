"""Code (line) coverage tests for the supplied Lab 6 module."""

import pytest

from amusement_park_ride_access import inspect_safety_restraints, process_ride_admissions


def test_admission_validation_rejects_bad_input():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_closed_and_unknown_ride_groups_are_skipped_or_rejected():
    result = process_ride_admissions(
        [{"is_open": False}, {"is_open": True, "ride_type": "unknown"}], 5.0
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_ride_prices_adult_child_and_fast_lane():
    groups = [
        {"is_open": True, "ride_type": "roller_coaster", "patrons": [
            {"height_cm": 150}, {"height_cm": 130, "is_child": True}
        ]},
        {"is_open": True, "ride_type": "water_ride", "has_fast_lane": True,
         "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "family", "patrons": [{"height_cm": 150}]},
    ]
    assert process_ride_admissions(groups, 5.0) == {
        "total_revenue": 73.0, "status": "COMPLETED"
    }


def test_height_health_warning_and_coaster_group_cancellation():
    groups = [
        {"is_open": True, "ride_type": "family", "patrons": [
            {"height_cm": 0}, {"height_cm": 110},
            {"height_cm": 150, "health_warning": True}, {"height_cm": 150}
        ]},
        {"is_open": True, "ride_type": "roller_coaster", "has_fast_lane": True,
         "patrons": [{"height_cm": 150}, {"height_cm": 160, "health_warning": True}]},
    ]
    result = process_ride_admissions(groups, 3.0)
    assert result == {"total_revenue": 13.0, "status": "COMPLETED"}


def test_safety_audit_status():
    patrons = [{"height_cm": 0} for _ in range(5)]
    result = process_ride_admissions(
        [{"is_open": True, "ride_type": "family", "patrons": patrons}], 0.0
    )
    assert result == {"total_revenue": 0.0, "status": "SAFETY_AUDIT"}


@pytest.mark.parametrize(
    "streams,expected",
    [([], "NO_DATA"), ([[1, 0, 1, 0]], "SAFE"), ([[0, 0]], "EMERGENCY_LOCK"),
     ([[0], [1, 0, 0]], "EMERGENCY_LOCK")],
)
def test_restraint_stream_outcomes(streams, expected):
    assert inspect_safety_restraints(streams) == expected
