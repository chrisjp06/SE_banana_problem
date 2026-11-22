"""Input-safe amusement park helpers used by the Lab 7 fuzzing exercise."""

import math


def validate_height_and_fastpass(rider_spec):
    """Format ``HEIGHT:YES|NO``; return None for malformed input."""
    if not isinstance(rider_spec, str):
        return None
    parts = rider_spec.strip().split(":")
    if len(parts) != 2:
        return None
    height_text, pass_text = (part.strip() for part in parts)
    try:
        height = int(height_text)
    except ValueError:
        return None
    pass_map = {"YES": True, "NO": False}
    has_fastpass = pass_map.get(pass_text.upper())
    if has_fastpass is None:
        return None
    eligible = height >= 120
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    """Calculate riders/minute; return None for malformed or unsafe metrics."""
    if not isinstance(ride_metric_str, str) or ride_metric_str.count("/") != 1:
        return None
    riders_text, mins_text = (part.strip() for part in ride_metric_str.split("/"))
    try:
        riders = float(riders_text)
        cycle_mins = float(mins_text)
    except ValueError:
        return None
    if not math.isfinite(riders) or not math.isfinite(cycle_mins):
        return None
    if riders < 0 or cycle_mins <= 0:
        return None
    rate = riders / cycle_mins
    if not math.isfinite(rate):
        return None
    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    """Resolve a three-letter ride zone prefix; unknown values return None."""
    if not isinstance(zone_code, str):
        return None
    prefix = zone_code.strip().upper()[:3]
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar",
    }
    return restraint_types.get(prefix)


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    result = validate_height_and_fastpass(r_input)
    print(result if result is not None else "Invalid rider specification")

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    result = compute_dispatch_throughput(t_input)
    print("Throughput (riders/min):", result if result is not None else "Invalid ride metric")

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    result = resolve_safety_restraint_code(z_input)
    print("Restraint:", result if result is not None else "Unknown ride zone code")


if __name__ == "__main__":
    main()
