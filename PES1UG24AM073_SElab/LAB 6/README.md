# Lab 6: Code and Branch Coverage

This folder contains a local working copy of the Lab 6 amusement park module, two independent pytest suites, coverage evidence, and the required commit history.

## Files

- `amusement_park_ride_access.py`: module under test copied from the assigned repository.
- `CodeCoverageTest_Student_application.py`: line/code coverage suite.
- `BranchCoverageTest_Student_application.py`: branch coverage suite.
- `deliverables/`: text transcripts, coverage summaries, HTML report, and PNG evidence sheets rendered from the terminal transcripts. The PNGs are transcript renderings rather than direct desktop captures.

The handout uses `xxxx` in the test filenames as a student identifier. Replace `Student` with your assigned identifier before submission if required by your instructor.

## Run the analyses

From this folder, run:

```powershell
py -m coverage erase
py -m coverage run --source=amusement_park_ride_access -m pytest -q CodeCoverageTest_Student_application.py
py -m coverage report -m

py -m coverage erase
py -m coverage run --branch --source=amusement_park_ride_access -m pytest -q BranchCoverageTest_Student_application.py
py -m coverage report -m
```

The first run reports line coverage; the second measures branches as well. The checked-in evidence records each suite independently.
