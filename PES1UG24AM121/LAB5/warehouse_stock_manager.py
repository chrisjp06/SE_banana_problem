"""
Warehouse Stock Manager Module.

Provides inventory management functionality including receiving, issuing,
reorder auditing, persistent storage, and secure formula adjustments.
"""

# pylint: disable=invalid-name

import hashlib
import json
import os
import re
from datetime import datetime

# Module constants
AUDIT_FILE = "warehouse_audit.log"
DEFAULT_STORAGE_FILE = "warehouse.json"
SUPERVISOR_PASSWORD_HASH = hashlib.sha256(
    os.environ.get("SUPERVISOR_PASSWORD", "wh-admin-1234").encode("utf-8")
).hexdigest()

# Global stock registry
warehouse_stock: dict[str, int] = {}


def add_stock(sku="default", qty=0, history=None):
    """
    Add incoming stock quantity for a given SKU.

    Args:
        sku: Unique item SKU identifier (must be string).
        qty: Positive integer quantity to add.
        history: Optional list tracking stock transaction logs.
    """
    if history is None:
        history = []
    if not sku or not isinstance(sku, str):
        return
    if qty <= 0:
        return
    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty
    history.append(f"{datetime.now()}: Received {qty} units of {sku}")


def remove_stock(sku, qty):
    """
    Remove stock quantity for an existing SKU.

    Args:
        sku: Unique item SKU identifier.
        qty: Quantity to deduct.
    """
    if not sku or not isinstance(sku, str) or qty <= 0:
        return
    if sku in warehouse_stock:
        warehouse_stock[sku] -= qty
        if warehouse_stock[sku] <= 0:
            del warehouse_stock[sku]


def get_stock(sku):
    """Retrieve current stock level for a SKU."""
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """
    Generate short SHA-256 fingerprint for printed bin labels.

    Args:
        sku: SKU string to hash.
    """
    return hashlib.sha256(str(sku).encode("utf-8")).hexdigest()[:6]


def load_stock(file_path=DEFAULT_STORAGE_FILE):
    """
    Load stock records from a JSON file.

    Args:
        file_path: Path to the JSON data file.
    """
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
        warehouse_stock.clear()
        warehouse_stock.update(data)


def save_stock(file_path=DEFAULT_STORAGE_FILE):
    """
    Save current stock records to a JSON file.

    Args:
        file_path: Path to the JSON data file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(warehouse_stock, indent=2))


def print_report():
    """Print a formatted report of warehouse stock levels."""
    print("Warehouse Stock Report")
    for sku, qty in warehouse_stock.items():
        chk = sku_checksum(str(sku))
        print(f"{sku} -> {qty} units  [chk: {chk}]")


def check_reorder(threshold=10):
    """
    Identify SKUs whose stock levels fall below the reorder threshold.

    Args:
        threshold: Minimum acceptable stock count.
    """
    return [sku for sku, qty in warehouse_stock.items() if qty < threshold]


def _safe_eval_formula(formula: str, current: int) -> int:
    """
    Safely evaluate simple arithmetic expressions like 'current + 25'
    or 'current * 2' without using the dangerous eval() built-in.
    """
    cleaned = formula.strip().replace(" ", "")
    match = re.fullmatch(r"current([+\-*/])(\d+)", cleaned)
    if match:
        op, val_str = match.groups()
        val = int(val_str)
        if op == "+":
            return current + val
        if op == "-":
            return max(0, current - val)
        if op == "*":
            return current * val
        if op == "/" and val != 0:
            return current // val
    if cleaned.isdigit():
        return int(cleaned)
    return current


def apply_adjustment(sku, formula, password):
    """
    Adjust a SKU's quantity based on a supervisor formula.

    Args:
        sku: SKU identifier.
        formula: Arithmetic formula string (e.g. 'current + 25').
        password: Supervisor access password.
    """
    input_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if input_hash != SUPERVISOR_PASSWORD_HASH:
        return
    current = warehouse_stock.get(sku, 0)
    warehouse_stock[sku] = _safe_eval_formula(formula, current)
    log_entry = (
        f"adjusted {sku} using formula {formula} at {datetime.now()}\n"
    )
    with open(AUDIT_FILE, "a", encoding="utf-8") as audit:
        audit.write(log_entry)


# Backward compatibility aliases
addStock = add_stock
removeStock = remove_stock
getStock = get_stock
skuChecksum = sku_checksum
loadStock = load_stock
saveStock = save_stock
printReport = print_report
checkReorder = check_reorder
applyAdjustment = apply_adjustment


def main():
    """Run standard warehouse stock demonstration."""
    add_stock("WID-001", 40)
    add_stock("WID-002", 10)  # corrected from negative to valid initial stock
    add_stock("WID-404", 15)  # standardized string SKU
    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)
    remove_stock("WID-001", 500)
    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())
    apply_adjustment("WID-002", "current + 25", "wh-admin-1234")
    save_stock()
    load_stock()
    print_report()
    print("stock audit complete")


if __name__ == "__main__":
    main()
