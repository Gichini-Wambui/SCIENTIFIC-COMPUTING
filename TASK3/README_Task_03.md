# Task 3: Mathematical Functions and Vectorization

**Course:** BIT 2118 Scientific Computing
**Student name:** ______________  **Reg. No.:** ______________
**Program files:** `Task_03_vectorization.py`, `Task_03_modified_electricity_billing.py`

---

## B. Inputs and mathematical operations

**Input values**

| Input | Description |
|---|---|
| `latency_ms` | 1,000,000 random latency values, uniformly distributed between 5 and 250 ms |
| Random seed `42` | Makes the "random" data identical on every run (reproducible) |

**Operations performed**

| Step | Mathematics | Code |
|---|---|---|
| Unit conversion | seconds = ms / 1000 | `latency_ms / 1000.0` |
| Squaring | y = seconds² | `seconds ** 2` |
| Timing | measure how long each method takes | `timeit.timeit()` |

Two versions compute the same result:
- **Loop version:** a Python `for` loop handles one value at a time.
- **Vectorized version:** one NumPy expression handles all one million values at once, using compiled C code internally.

## C. Changing an input

**Change:** the number of measurements N was changed from 1,000,000 to 100,000 and to 5,000,000.

| N | Loop time | Vectorized time | Speed-up |
|---|---|---|---|
| 100,000 | 0.0135 s | 0.0005 s | 25.1x |
| 1,000,000 (original) | 0.1424 s | 0.0031 s | 45.8x |
| 5,000,000 | 0.7605 s | 0.0220 s | 34.6x |

**Explanation:** both methods take longer as N grows, roughly in proportion to N, but the vectorized version is always far faster. The speed-up figure varies between runs (25x to 46x here) because timings depend on CPU load, caching and memory. The consistent conclusion is that vectorization is **tens of times faster**. Your own timings will differ from these, which is normal. Report your own numbers.

## D. Meaning of the output

```
First five squared latency values: [0.03787665 0.01266192 0.04637842 0.03092504 0.00078812]
Loop time: 0.1424 s
Vectorized time: 0.0031 s
Approximate speed-up: 45.8x
```

- The first line shows latency squared in **seconds²**. For example, 0.0379 s² corresponds to a latency of about 195 ms (0.195² ≈ 0.038).
- The loop took about 0.14 s and the vectorized code about 0.003 s, giving a speed-up of about **46x** for the same answer.
- No graph is produced in this task.
- Vectorization makes the code both **shorter** (two lines instead of a loop) and **faster**. This matters when millions of operations are repeated, as in signal processing or machine learning.

## E. Modified program: tiered electricity billing

**File:** `Task_03_modified_electricity_billing.py`

**Real-world case:** a power utility must compute monthly bills for one million households under a tiered tariff, where the price per unit rises with consumption.

**Assumptions**
1. Tariff (assumed, not an official one): 12 KES/kWh for the first 30 kWh, 16 KES/kWh for the next 70 kWh, 22 KES/kWh above 100 kWh.
2. 16% VAT is added to the energy charge.
3. Monthly usage follows a gamma distribution (shape 4, scale 20), mean about 80 kWh. This gives a right-skewed spread, so a few households use far more than average.
4. No fixed charges or levies.

**Input data:** 1,000,000 simulated monthly usage values in kWh (seed 42).

**Vectorized technique:** each tier is computed for all households at once with `np.minimum`, `np.clip` and `np.maximum`, replacing the `if / elif / else` chain inside the loop.

**Output**

```
Results identical: True
Average bill: 1408.83 KES
Highest bill: 9522.88 KES
Total revenue: 1408.83 million KES
Households above 100 kWh: 26.5%
Loop time: 0.2419 s | Vectorized time: 0.0186 s
Approximate speed-up: 13.0x
```

**Interpretation:**
- `Results identical: True` confirms the vectorized version gives the same bills as the loop, so it is correct and not just fast.
- The average household pays about 1,409 KES per month, and the heaviest user about 9,523 KES. Total revenue for one million households is about 1,409 million KES.
- About 26.5% of households fall in the most expensive tier (above 100 kWh).
- The speed-up is smaller (13x) than in the main task because the tier calculation needs several array operations, but vectorization is still clearly faster.
- For a utility billing millions of customers each month, this approach cuts processing time and is easier to maintain.

---

## Repository checklist
- [ ] `Task_03/` folder pushed to **your own** GitHub repo
- [ ] Both `.py` files and this README included
- [ ] GitHub link uploaded on VLMS
