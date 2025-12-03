💰 Debt Tracker (A–M–S Edition)

A simple, reliable and transparent command-line tool to track debts between a defined group of people.
Designed to avoid confusion, prevent double-counting, and ensure that all balances are always clean, mutually consistent and mathematically correct.

This version works for three people (A, M, S) but can be expanded easily.


---

⭐ Features

✔ Add any number of new debts in one action

You select a creditor, then register one or more debtors + amounts.
The program automatically merges all new entries and recalculates every pairwise relation.


---

✔ Automatic pair-wise consolidation

For each pair of people (A↔M, A↔S, M↔S), the program ensures there is always at most ONE final debt entry, representing the true net balance between them.

No duplicates, no messy logs, no ambiguity.


---

✔ Financially correct cancellations

You never cancel a debt by entering a negative amount.
Instead, you simply record the opposite debt, and the program cancels the two amounts automatically.

Examples:

If A owes M €20 and you enter “M owes A €20”, the program returns:

✓ Full cancellation between A and M

If A owes M €20 and you enter “M owes A €5”, the program returns:

A owes M €15.00


Both partial and full cancellations are fully supported.


---

✔ Alerts based on debt age

The script calculates how many days have passed since each debt was last updated:

🟡 Less than 3 days

🔴 3+ days → Overdue alert

🟢 No active debts



---

✔ Clean and human-readable CSV storage

All data is stored in:

/CSVs/debt_data.csv

Each row represents a final, consolidated debt, not raw historical entries.


---

📂 Folder structure

project_folder/
├── instruction_flow.py (if you also use the instruction engine)
├── debt_tracker.py     <-- THIS TOOL
└── CSVs/
    └── debt_data.csv


---

🚀 How to Use

Run:

python3 debt_tracker.py

You’ll see:

💰 DEBT TRACKER — Base Final (Fixed 2)

--- MENU ---
1. Add new debt ➕
2. View debt status 📊
3. Exit 🚪


---

1️⃣ Add New Debt

You select:

The creditor (who is owed)

One or more debtors (who owe)

Amounts (always positive)


Example flow:

--- Add new debt ---
Who is owed? (creditor): A
Who owes? (debtor): M
Amount (€): 10
Add another debt to same creditor? (y/n): y
Who owes? (debtor): S
Amount (€): 5
Add another debt to same creditor? (y/n): n

🧮 Total new debt to A: €15.00
Confirm and save? (y/n): y

After saving, the script will:

Combine this with previous data

Recalculate all pairwise balances

Remove any fully cancelled pairs

Save the final, clean results



---

2️⃣ View Current Debt Status

Example result:

📊 Current debt status:
M owes A €12.00 (🔴 5d delay ‼️)
S owes A € 5.00 (🟡)
A 🟢


---

🧠 How the Accounting Works (Short & Clear)

The rules are simple and strict:

• Every record means:

FROM owes TO

• Amounts are always positive. No negatives allowed.

Negative numbers cause mistakes in accounting — the system avoids them entirely.

• Cancellation happens by registering the opposite direction.

This keeps the history correct and traceable.

• After each operation, the program normalizes all pairs:

For each pair (A, M):

If A owes M is larger → final line = A owes M [difference]

If M owes A is larger → final line = M owes A [difference]

If equal → the pair is deleted (full cancellation)


This guarantees the database always stays clean.


---

👥 People List

By default, the program tracks debts among:

PEOPLE = ["A", "M", "S"]

You can add more:

PEOPLE = ["A", "M", "S", "J", "P"]

The logic expands automatically.


---

🛡 Reliability

This tool guarantees:

No corrupted entries

No inversions (A↔M bug solved)

No duplicates

No contradictory debts

All cancellations properly recognized

CSV remains clean and up-to-date



---

🧾 CSV Format

The internal CSV uses this structure:

from,to,amount,date
A,M,10.0,2025-01-03 21:55:00
S,A,5.0,2025-01-03 21:55:00

Each row is a final, consolidated pair, not raw history events.


---

📎 Full Program (Reference)

You already provided it, so the README simply points to:

> See debt_tracker.py for the full source code.
