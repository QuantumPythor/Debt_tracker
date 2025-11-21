#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debt Tracker Base Final — FIXED2
Solves the A↔M inversion issue.
Keeps clear, stable pair-wise debt calculation.
"""

import csv
import os
from datetime import datetime

# --- Config ---
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CSVs")
os.makedirs(BASE_DIR, exist_ok=True)
DATA_FILE = os.path.join(BASE_DIR, "debt_data.csv")
PEOPLE = ["A", "M", "S"]

# --- Helpers ---
def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["from", "to", "amount", "date"])

def load_data():
    ensure_file()
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_data(rows):
    ensure_file()
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["from", "to", "amount", "date"])
        for r in rows:
            w.writerow([r["from"], r["to"], r["amount"], r["date"]])

def prompt_person(prompt):
    while True:
        p = input(prompt).strip().upper()
        if p in PEOPLE:
            return p
        print("❌ Invalid name. Use A, M or S.")

def prompt_amount(prompt):
    while True:
        s = input(prompt).strip()
        try:
            a = float(s)
            if a > 0:
                return a
            print("❌ Amount must be positive.")
        except:
            print("❌ Invalid number, try like 12.34")

# --- Core functions ---
def add_debt():
    rows = load_data()
    print("\n--- Add new debt ---")
    creditor = prompt_person("Who is owed? (creditor): ")

    new_entries = []
    temp_total = 0.0

    while True:
        debtor = prompt_person("Who owes? (debtor): ")
        if debtor == creditor:
            print("❌ Debtor cannot be the same as creditor.")
            continue

        amount = prompt_amount("Amount (€): ")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entries.append({"from": debtor, "to": creditor, "amount": amount, "date": date})
        temp_total += amount

        again = input("Add another debt to same creditor? (y/n): ").strip().lower()
        if again != "y":
            break

    print(f"\n🧮 Total new debt to {creditor}: €{temp_total:.2f}")
    confirm = input("Confirm and save? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Cancelled.")
        return

    # Combine old and new data
    rows.extend(new_entries)

    # Recalculate all debts pairwise
    debts = {}
    for r in rows:
        a, b = r["from"], r["to"]
        amt = float(r["amount"])
        key = tuple(sorted([a, b]))
        if key not in debts:
            debts[key] = 0.0
        # Positive means first owes second alphabetically
        if a < b:
            debts[key] += amt
        else:
            debts[key] -= amt

    # Build clean final list
    clean_rows = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for (a, b), net in debts.items():
        if abs(net) < 0.01:
            print(f"✅ Full cancellation between {a} and {b}")
            continue
        if net > 0:
            clean_rows.append({"from": a, "to": b, "amount": str(round(net, 2)), "date": now})
            print(f"📘 {a} owes {b} €{abs(net):.2f}")
        else:
            clean_rows.append({"from": b, "to": a, "amount": str(round(-net, 2)), "date": now})
            print(f"📗 {b} owes {a} €{abs(net):.2f}")

    save_data(clean_rows)
    print("✅ Debts saved and recalculated correctly.")

def show_status():
    rows = load_data()
    today = datetime.now()

    debts_by_debtor = {p: [] for p in PEOPLE}
    for r in rows:
        debtor = r["from"]
        creditor = r["to"]
        amt = float(r["amount"])
        date = datetime.strptime(r["date"], "%Y-%m-%d %H:%M:%S")
        days = (today - date).days
        debts_by_debtor[debtor].append((creditor, amt, days))

    print("\n📊 Current debt status:")
    any_debt = False
    for p in PEOPLE:
        if not debts_by_debtor[p]:
            print(f"{p} 🟢")
        else:
            any_debt = True
            for creditor, amt, days in debts_by_debtor[p]:
                color = "🟡" if days < 3 else f"🔴 {days}d delay ‼️"
                print(f"{p} owes {creditor} €{amt:.2f} ({color})")
    if not any_debt:
        print("\n✅ No debts — all clear 🟢")

# --- Main ---
def main():
    ensure_file()
    print("💰 DEBT TRACKER — Base Final (Fixed 2)")

    while True:
        print("\n--- MENU ---")
        print("1. Add new debt ➕")
        print("2. View debt status 📊")
        print("3. Exit 🚪")

        opt = input("→ ").strip()
        if opt == "1":
            add_debt()
        elif opt == "2":
            show_status()
        elif opt == "3":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid option — try again.")

if __name__ == "__main__":
    main()