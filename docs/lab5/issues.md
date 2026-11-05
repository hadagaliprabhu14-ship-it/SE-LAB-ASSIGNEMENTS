# Static analysis findings and fixes

The reports were generated against the assigned repository's original `supplier_orders.py` and the cleaned copy in this folder. Line numbers below refer to the original copy at `before/supplier_orders.py`. The findings are ordered with higher severity first.

| Issue | Type / severity | Line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command includes supplier text | Bandit B605 / High | 20–21 | `os.system` starts a shell command using concatenated text, creating a command injection risk if supplier data is untrusted. | Removed shell execution and print a warehouse notification directly. |
| SQL built with string interpolation | Bandit B608 / Medium | 11 | Supplier and item values were inserted into SQL by string formatting, allowing SQL injection and breaking on quotes. | Use SQLite parameter placeholders and pass values separately. |
| Broad exception silently ignored | Pylint W0718, Bandit B110 / Low | 25–28 | `except Exception: pass` can conceal database errors and leave cleanup failures unnoticed. | Removed the catch-all; SQLite errors now surface to the caller. |
| Mutable global order total | Pylint W0603 / quality | 6, 9–13 | A global counter couples order placement to module state and complicates reuse. | Compute the quantity total from the database and return it from `place_order`. |
| Unused remarks argument | Pylint W0613 / quality | 16 | `remarks` was accepted but never stored or used. | Removed the unused parameter from `mark_received`. |
| Naming, docstrings, and formatting problems | Pylint C0114/C0116/C0103; Flake8 E225/E501 | 1, 5, 9–35 | Missing documentation, camelCase names, long lines, and missing operator spacing reduced consistency and readability. | Added module/function docstrings, converted names to snake_case, and formatted statements to satisfy Flake8. |
| No order input validation | Review finding / correctness | 9 | Empty names and non-positive quantities could be recorded. | Reject blank supplier/item values and quantities that are not positive integers; the table also has constraints. |

## Verification summary

- Pylint: original score **2.41/10**; cleaned score **10.00/10** (target: above 9.5).
- Bandit: original report found **1 High, 1 Medium, and 1 Low** issue; cleaned report found **0** issues.
- Flake8: original report found **4** formatting violations; cleaned report is empty (no violations).
- Reports are saved in `reports/before/` and `reports/after/`.
