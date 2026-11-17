# Task 4: Floating-Point Arithmetic and Numerical Errors

**Course:** BIT 2118 Scientific Computing
**Student name:** ______________  **Reg. No.:** ______________
**Program files:** `Task_04_numerical_errors.py`, `Task_04_modified_banking.py`

---

## B. Inputs and mathematical operations

**Input values**

| Input | Value | Purpose |
|---|---|---|
| `calculated`, `expected` | 0.1 + 0.2 and 0.3 | Floating-point comparison |
| `true_value` | √2 (full double precision) | Reference value |
| `approx_value` | 1.414 | Rounded approximation of √2 |
| `x` | 1e-4, 1e-8, 1e-12 | Small numbers for the stability test |

**Operations performed**

| Operation | Formula |
|---|---|
| Exact comparison | `calculated == expected` |
| Tolerance comparison | `np.isclose(a, b)` checks that \|a − b\| is very small |
| Absolute error | \|true − approximate\| |
| Relative error | absolute error / \|true\| |
| Unstable formula | (√(1+x) − 1) / x |
| Stable formula | 1 / (√(1+x) + 1) |

The two formulas are **algebraically identical**: multiply the top and bottom of the unstable one by (√(1+x) + 1). They behave very differently in a computer.

## C. Changing an input

**Change 1:** `approx_value` changed from 1.414 to 1.41421.

| | Original (1.414) | Changed (1.41421) |
|---|---|---|
| Absolute error | 0.00021356 | 0.00000356 |
| Relative error | 0.0151% | 0.000252% |

More digits kept means a smaller error. Adding two more digits reduced the error by about 60 times.

**Change 2:** a smaller x value, `1e-15`, was added to the stability test.

| x | Direct (unstable) | Stable | Correct limit |
|---|---|---|---|
| 1e-12 | 0.500044450291 | 0.500000000000 | 0.5 |
| 1e-15 | **0.444089209850** | 0.500000000000 | 0.5 |

As x shrinks, the direct formula gets worse, and at 1e-15 it is wrong in the second digit (0.444 instead of 0.5). The stable formula stays correct.

## D. Meaning of the output

```
0.1 + 0.2 = 0.30000000000000004
Exact comparison: False
Tolerance-based comparison: True
Absolute error: 0.00021356
Relative error: 0.01510114%
x=1e-04: direct=0.499987500624, stable=0.499987500625
x=1e-08: direct=0.499999996961, stable=0.499999998750
x=1e-12: direct=0.500044450291, stable=0.500000000000
```

- **0.1 + 0.2 ≠ 0.3 exactly.** Computers store numbers in binary, and 0.1 and 0.2 cannot be written exactly in binary, just as 1/3 cannot be written exactly in decimal. The sum is off by about 5×10⁻¹⁷. `np.isclose` correctly accepts the two values as equal within a small tolerance.
- **Truncating √2 to 1.414** gives a relative error of about 0.015%. This is acceptable for rough work but not for precise engineering.
- **The unstable formula** subtracts two nearly equal numbers, √(1+x) and 1, which is called *catastrophic cancellation*. Most of the correct digits cancel out and the leftover digits are mostly round-off error. The stable formula avoids the subtraction. The true value approaches 0.5 as x → 0.
- No graph is produced in this task.

## E. Modified program: banking and micro-payments

**File:** `Task_04_modified_banking.py`

**Real-world case:** a mobile-money platform credits 1,000,000 micro-payments of 0.10 KES to an account. The correct total is exactly 100,000.00 KES. The program shows how floating-point round-off accumulates, and compares four ways to avoid it.

**Assumptions**
1. Every payment is exactly 0.10 KES.
2. The true total is 100,000.00 KES.
3. A tolerance below one cent (0.01 KES) is acceptable for reporting, but a ledger must reconcile exactly.
4. Payments are added one by one, as in a transaction log.

**Input data:** N = 1,000,000 payments of 0.10.

**Methods compared:** naive float sum, `math.fsum`, `Decimal`, and integer cents.

**Output**

```
Naive float sum : 100000.00000133288
math.fsum       : 100000.0
Decimal         : 100000.00
Integer cents   : 100000.0
Naive absolute error: 0.0000013329 KES
Naive relative error: 1.333e-11
Naive total equals 100000.00 exactly? False
Within tolerance (np.isclose)? True
Ledger == bank (exact)? False
Ledger == bank (round to cents)? True
```

**Interpretation:**
- The naive sum is off by about 0.0000013 KES after a million additions. Each addition adds a tiny round-off error, and these **accumulate**. The error is tiny here, but it would grow with more transactions, and it makes an exact equality check fail.
- `math.fsum`, `Decimal` and integer cents all give exactly 100,000.00.
- The ledger check shows the practical danger: `0.1 + 0.2 == 0.3` is `False`, so a program comparing balances with `==` could wrongly flag a mismatch. Rounding to cents, or comparing with a tolerance, fixes this.
- **Recommendation:** financial software should store money as integers (cents) or `Decimal`, never as plain floats, and should compare values with a tolerance.

---

## Repository checklist
- [ ] `Task_04/` folder pushed to **your own** GitHub repo
- [ ] Both `.py` files and this README included
- [ ] GitHub link uploaded on VLMS
