import math
from decimal import Decimal
import numpy as np

# A mobile-banking system credits 1,000,000 micro-payments of 0.10 KES each.
# The true total is exactly 100,000.00 KES.
N = 1_000_000
payment = 0.10
true_total = 100_000.00

# Method 1: naive running sum with floats
naive = 0.0
for _ in range(N):
    naive += payment

# Method 2: math.fsum (error-compensated summation)
accurate = math.fsum([payment] * N)

# Method 3: Decimal arithmetic (exact decimal representation)
exact = sum(Decimal("0.10") for _ in range(N))

# Method 4: work in integer cents
cents = sum([10] * N) / 100

print(f"Naive float sum : {naive!r}")
print(f"math.fsum       : {accurate!r}")
print(f"Decimal         : {exact}")
print(f"Integer cents   : {cents!r}")
print(f"Naive absolute error: {abs(naive - true_total):.10f} KES")
print(f"Naive relative error: {abs(naive - true_total) / true_total:.3e}")
print("Naive total equals 100000.00 exactly?", naive == true_total)
print("Within tolerance (np.isclose)?", np.isclose(naive, true_total))

# Reconciliation check: why exact equality is dangerous in banking
balance_ledger = 0.1 + 0.2
balance_bank = 0.3
print("Ledger == bank (exact)?", balance_ledger == balance_bank)
print("Ledger == bank (round to cents)?", round(balance_ledger, 2) == round(balance_bank, 2))
