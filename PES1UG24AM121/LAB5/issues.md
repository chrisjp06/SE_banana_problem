# Lab 5: Documented Static Analysis Issues & Fixes

**Student Name:** Janhavi Rajpurohit  
**SRN:** PES1UG24AM121  
**Repository:** `L5_54_warehouse-stock`  
**File Analyzed:** `warehouse_stock_manager.py`  

---

### Identified Issues Table

| Issue | Tool / Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **Arbitrary Code Execution via `eval()`** | Bandit / High Severity (B307) | 62, 80 | Use of `eval()` on supervisor formula input (`eval(formula, ...)`) and on string execution (`eval("print(...)")`) allows remote arbitrary code execution. | Replaced `eval()` with a custom deterministic arithmetic parser `_safe_eval_formula()` using strict regex matching `current([+\-*/])(\d+)`, and replaced direct `eval()` call with `print()`. |
| **Insecure Cryptographic Hash (`MD5`)** | Bandit / High Severity (B324) | 31 | `hashlib.md5()` is cryptographically weak, prone to collision vulnerabilities, and flagged by security audits. | Migrated from MD5 to standard `hashlib.sha256()`, encoding strings explicitly in UTF-8. |
| **Hardcoded Supervisor Credential** | Bandit / Low Severity (B105) | 10 | Password `"wh-admin-1234"` was stored as plaintext in the global scope of source code. | Extracted password configuration to environment variable `SUPERVISOR_PASSWORD` with SHA-256 hash comparison for verification. |
| **Silent Exception Swallowing (`bare-except`)** | Pylint (W0702) & Flake8 (E722) | 23 | Bare `except:` block silently suppressed all exceptions, including `KeyboardInterrupt` and `SystemExit`, masking critical bugs. | Replaced bare exception with proactive conditional check `if sku in warehouse_stock:` to cleanly handle missing keys. |
| **Mutable Default Argument (`history=[]`)** | Pylint / Bug Warning (W0102) | 12 | The default empty list `history=[]` is evaluated once at definition time, sharing state across independent invocations. | Changed parameter signature to `history=None` and initialized `history = []` dynamically inside the function body. |
| **Unmanaged Resource Allocation (Missing `with`)** | Pylint / Refactor (R1732, W1514) | 34, 40, 63 | File objects opened with `open()` without context manager or explicit encoding, risking file handle leakage on exceptions. | Wrapped all file operations in `with open(..., encoding="utf-8") as file:` context managers. |
| **Unused Imports & Variables** | Pylint & Flake8 (W0611, F401, W0612, F841) | 2, 4, 54 | `logging` and `os` were imported but never utilized; `total_units` was calculated and assigned but never used. | Removed dead imports and redundant computations to streamline execution and eliminate dead code. |
| **PEP 8 Formatting & Style Infractions** | Flake8 (E302, E305, E501, W291) | Multiple | Missing double blank lines between functions, lines exceeding 79 characters, and trailing whitespace. | Reformatted according to PEP 8 standards with proper blank lines, line lengths ≤ 79 characters, and trimmed whitespace. |

---

### Verification Summary
* **Pylint Score Before Fix:** 4.48 / 10
* **Pylint Score After Fix:** **10.00 / 10**
* **Bandit Issues Before Fix:** 5 (1 High, 2 Medium, 2 Low)
* **Bandit Issues After Fix:** **0 (No issues identified)**
* **Flake8 Violations Before Fix:** 19 violations
* **Flake8 Violations After Fix:** **0 violations**
