# Lab 7: Fuzz Testing with Hypothesis

This is the completed Lab 7 deliverables folder, based on the assigned repository's starter `processor.py` and `test_processor.py`.

## Deliverables

- `processor.py`: hardened application script.
- `test_processor.py`: Hypothesis property-based tests for all three public functions.
- `deliverables/Lab7_FuzzTesting_Evidence.pdf`: evidence document containing the initial run, minimized fuzz failures, fixed script runs, and passing fuzz rerun.
- `deliverables/screenshots/`: PNG evidence panels used in the PDF.
- `deliverables/logs/`: captured command outputs, including the full initial failure report.
- `deliverables/buggy_processor_original.py`: original starter version used to reproduce the failures.

The evidence panels are rendered from captured PowerShell output logs. They preserve the command results and are included in the PDF; they are not direct desktop screenshots.

## Input behavior after the fix

- `validate_height_and_fastpass` returns `None` for non-string, malformed, or unsupported fast-pass inputs.
- `compute_dispatch_throughput` returns `None` for malformed metrics, non-finite values, negative rider counts, zero/negative cycle time, or an overflowing rate.
- `resolve_safety_restraint_code` returns `None` for non-string values and unknown prefixes.
- The command-line script prints a readable validation message when any function returns `None`.

## Run

Install dependencies with `py -m pip install -r requirements.txt`, then run `py -m pytest -q test_processor.py` and `py processor.py` from this folder.
