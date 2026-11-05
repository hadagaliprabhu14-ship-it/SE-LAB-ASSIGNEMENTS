# Lab 5 — Static Code Analysis

Assigned repository: [L5_18_supplier_orders](https://github.com/SETAPESU26/L5_18_supplier_orders)  
Assigned program: `supplier_orders.py`

## Files

- `supplier_orders.py` — cleaned program.
- `before/supplier_orders.py` — original source used to produce baseline reports.
- `issues.md` — findings and fixes.
- `reflection.md` — reflection responses.
- `reports/before/` and `reports/after/` — Pylint, Bandit, Flake8, and demonstration output.
- `requirements.txt` — analyzer versions used for these reports.

## Results

| Tool | Before | After |
|---|---:|---:|
| Pylint | 2.41/10 | 10.00/10 |
| Bandit | 3 findings (High 1, Medium 1, Low 1) | 0 findings |
| Flake8 | 4 violations | 0 violations |

## Reproduce the reports

From this folder, install the pinned tools in a virtual environment and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\supplier_orders.py
python -m pylint .\supplier_orders.py
python -m bandit -r .\supplier_orders.py
python -m flake8 .\supplier_orders.py
```

The saved reports were generated with Python 3.13.7, Pylint 4.1.3, Bandit 1.9.4, and Flake8 7.5.0.

## Commit requirement

The handout asks for three commits, one grouped around each tool's findings. The project instructions for this work say not to commit or push, so no commits were created. Suggested local commit grouping when you choose to commit:

1. `fix: address Bandit security findings` — parameterized SQL and remove shell execution / swallowed exception.
2. `refactor: improve supplier order code quality` — remove global state and unused argument; add validation and documentation.
3. `style: resolve Flake8 formatting findings` — apply the clean formatting shown in the final source.
