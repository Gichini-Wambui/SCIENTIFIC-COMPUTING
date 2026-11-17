# Task 2: NumPy Arrays and Numerical Computation

## B. Inputs and mathematical operations

**Input values**

| Input | Description |
|---|---|
| `temperatures_c` | NumPy array of 24 hourly temperatures (°C), from 18.5 at 00:00 to 19.0 at 23:00 |

**Operations performed**

| Operation | Mathematics | NumPy |
|---|---|---|
| Mean | (x₁ + x₂ + … + x₂₄) / 24 | `np.mean()` |
| Minimum / Maximum | smallest / largest element | `np.min()`, `np.max()` |
| Unit conversion | F = 1.8·C + 32 applied to every element | `1.8 * temperatures_c + 32` |

The conversion is **vectorized**: one expression is applied to all 24 values with no loop.

## C. Changing an input

**Change:** the 14:00 reading was changed from 29.1 °C to 35.0 °C (simulating a heat spike or faulty sensor).

| Output | Original | After change |
|---|---|---|
| Mean | 23.12 °C | 23.37 °C |
| Minimum | 17.50 °C | 17.50 °C (unchanged) |
| Maximum | 29.40 °C | **35.00 °C** |

**Explanation:** the mean rose by (35.0 − 29.1)/24 ≈ 0.25 °C because one value out of 24 changed by 5.9 °C. The minimum did not change because the edited value is not the lowest. The maximum changed completely because 35.0 exceeds the old peak of 29.4. This shows the **mean is moderately sensitive** to one outlier, while the **maximum is fully sensitive** to it.

## D. Meaning of the output

Original output:

```
Daily mean temperature: 23.12 C
Minimum temperature: 17.50 C
Maximum temperature: 29.40 C
First six Fahrenheit readings: [65.3  64.4  64.04 63.5  64.22 66.2 ]
```

- The **average temperature over the day** was 23.12 °C.
- The **coolest hour** was 17.5 °C (around 03:00, before sunrise) and the **warmest** was 29.4 °C (around midday), a daily range of about 11.9 °C.
- The first six Fahrenheit values (00:00 to 05:00) are all about 64–66 °F, matching 17.5–19.0 °C. This confirms the conversion works.
- No graph is produced in this task.

## E. Modified program: vaccine-fridge monitoring

**File:** `Task_02_modified_vaccine_fridge.py`

**Real-world case:** a rural clinic uses an IoT sensor in its vaccine fridge. Most vaccines must stay between 2 °C and 8 °C. The program detects when the cold chain was broken.

**Assumptions**
1. One reading per hour for 24 hours.
2. The safe range is 2 °C to 8 °C for all stored vaccines.
3. Sensor readings are accurate, with no calibration error.
4. The fridge warms mid-day, for example because of a power cut or a door left open.

**Input data:** 24 hourly readings from 3.9 °C to 9.8 °C (see the code).

**New NumPy technique:** a boolean mask `(fridge_c < 2) | (fridge_c > 8)` marks unsafe hours, and `np.where()` returns which hours they were.

**Output**

```
Mean: 5.83 C | Min: 3.90 C | Max: 9.80 C
Hours outside 2.0-8.0 C: 5 of 24
Unsafe hours (0-23): [10 11 12 13 14]
Percentage of day unsafe: 20.8%
Peak temperature in F: 49.6 F
```

**Interpretation:** the daily mean (5.83 °C) is inside the safe range, but this hides a problem. Between 10:00 and 14:00 the fridge exceeded 8 °C for 5 hours (20.8% of the day), peaking at 9.8 °C. A mean alone would wrongly suggest everything was fine. Checking each reading with a mask is therefore necessary. The clinic should investigate the cause, such as a power outage or door left open, and check the vaccine vial monitors before use.

---


