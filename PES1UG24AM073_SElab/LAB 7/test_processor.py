"""Hypothesis fuzz tests for all public processor input functions."""

import math

import pytest
from hypothesis import example, given, settings, strategies as st

from processor import (
    compute_dispatch_throughput,
    resolve_safety_restraint_code,
    validate_height_and_fastpass,
)


RESTRAINTS = {
    "CST": "Over-the-Shoulder Harness",
    "WTR": "Lap Bar and Seatbelt",
    "DRP": "Hydraulic Shoulder Vest",
    "WHL": "Manual Safety Bar",
}


def call_without_crashing(function, value):
    try:
        return function(value)
    except Exception as error:
        pytest.fail(f"{function.__name__} crashed for {value!r}: {type(error).__name__}: {error}")


def expected_rider_result(value):
    if not isinstance(value, str):
        return None
    parts = value.strip().split(":")
    if len(parts) != 2:
        return None
    try:
        height = int(parts[0].strip())
    except ValueError:
        return None
    fastpass = parts[1].strip().upper()
    if fastpass not in {"YES", "NO"}:
        return None
    status = "FastPass Priority" if fastpass == "YES" else "Standard Entry"
    eligibility = "Approved" if height >= 120 else "Denied"
    return f"Height {height}cm: {eligibility} ({status})"


def expected_throughput(value):
    if not isinstance(value, str) or value.count("/") != 1:
        return None
    riders_text, minutes_text = value.split("/")
    try:
        riders = float(riders_text)
        minutes = float(minutes_text)
    except ValueError:
        return None
    if not math.isfinite(riders) or not math.isfinite(minutes) or riders < 0 or minutes <= 0:
        return None
    rate = riders / minutes
    return round(rate, 2) if math.isfinite(rate) else None


def expected_restraint(value):
    if not isinstance(value, str):
        return None
    return RESTRAINTS.get(value.strip().upper()[:3])


@settings(max_examples=60, deadline=None)
@given(st.one_of(st.text(max_size=80), st.none()))
@example("120:YES")
@example("119:no")
@example("1000: yes ")
def test_validate_height_and_fastpass_never_crashes(value):
    result = call_without_crashing(validate_height_and_fastpass, value)
    assert result == expected_rider_result(value)


@settings(max_examples=60, deadline=None)
@given(st.one_of(st.text(max_size=80), st.none()))
@example("48/2.5")
@example("0/1")
@example("1/0")
@example("nan/2")
@example("1e308/1e-308")
def test_compute_dispatch_throughput_never_crashes(value):
    result = call_without_crashing(compute_dispatch_throughput, value)
    assert result == expected_throughput(value)


@settings(max_examples=60, deadline=None)
@given(st.one_of(st.text(max_size=80), st.none()))
@example("CST_01")
@example(" wtr_A ")
@example("DRP")
@example("UNKNOWN")
def test_resolve_safety_restraint_code_never_crashes(value):
    result = call_without_crashing(resolve_safety_restraint_code, value)
    assert result == expected_restraint(value)
