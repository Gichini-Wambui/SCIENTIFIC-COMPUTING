# Task 6: Solution of Systems of Linear Equations

**Course:** BIT 2118 Scientific Computing
**Student name:** ______________  **Reg. No.:** ______________
**Program files:** `Task_06_linear_systems.py`, `Task_06_modified_circuit_analysis.py`

---

## B. Inputs and mathematical operations

**Input values**

| Input | Value | Meaning |
|---|---|---|
| Type A server | 4 CPU units, 8 GB memory | Resource use per server |
| Type B server | 2 CPU units, 12 GB memory | Resource use per server |
| Total CPU used | 20 units | Observed total |
| Total memory used | 72 GB | Observed total |

**The mathematical model.** Let x = number of Type A servers and y = number of Type B servers.

- CPU: 4x + 2y = 20
- Memory: 8x + 12y = 72

In matrix form this is **Ax = b** with A = [[4, 2], [8, 12]], b = [20, 72].

**Operations performed**

| Operation | Code |
|---|---|
| Solve Ax = b | `np.linalg.solve(A, b)` |
| Verify the answer | `A @ solution` should reproduce b |
| Residual | r = b − A·x, which should be about 0 |
| Residual norm | `np.linalg.norm(residual)`, one number measuring the size of the error |

## C. Changing an input

**Change:** total CPU usage changed from 20 to 22 units (b = [22, 72]).

| | Original | Changed |
|---|---|---|
| Printed result | A = 3, B = 4 | A = 4, B = 4 |
| **Exact** solution | x = 3, y = 4 | **x = 3.75, y = 3.5** |
| Residual norm | 0.0 | 0.0 |

**Explanation:**
- The program prints "4" and "4" only because the format `:.0f` rounds to whole numbers. The true solution is 3.75 and 3.5 servers. The printed line `Verification A @ solution: [22. 72.]` matches b only because the unrounded values are used there.
- A fractional number of servers is impossible. This means the observed totals (22 CPU, 72 GB) are **not consistent with a whole number of servers**, which suggests a measurement error or an unaccounted workload.
- Lesson: the code solves the equations correctly even when the answer makes no real-world sense. Always check that the result is physically meaningful, and do not hide decimals with rounding.
- Another possible change is making the rows proportional, for example Type B = (4 CPU, 16 GB) with Type A = (2 CPU, 8 GB). Then the determinant is 0, `np.linalg.solve` raises a *Singular matrix* error, and there is no unique solution.

## D. Meaning of the output

```
Type A servers: 3
Type B servers: 4
Verification A @ solution: [20. 72.]
Residual: [0. 0.]
Residual norm: 0.0
```

- There are **3 Type A servers and 4 Type B servers** active.
- Check by hand: CPU = 4(3) + 2(4) = 20 ✓ and memory = 8(3) + 12(4) = 72 ✓.
- The **residual is zero**, meaning the solution reproduces the observed totals exactly. A residual that is not close to zero would signal a problem.
- The determinant of A is 4·12 − 2·8 = 32, which is not zero, so the system has exactly one solution.
- No graph is produced in this task.

## E. Modified program: electrical circuit mesh analysis

**File:** `Task_06_modified_circuit_analysis.py`

**Real-world case:** find the current in each loop of a resistor circuit using Kirchhoff's voltage law. The unknowns are the mesh currents I₁, I₂, I₃ (amperes).

**Assumptions**
1. Mesh 1 has a 12 V source and a 10 Ω resistor of its own. It shares a 20 Ω resistor with mesh 2.
2. Mesh 2 has a 20 Ω resistor of its own. It shares 20 Ω with mesh 1 and 40 Ω with mesh 3.
3. Mesh 3 has a 6 V source acting against the assumed current direction (so −6 V), a 10 Ω resistor of its own, and shares 40 Ω with mesh 2.
4. Ideal sources and fixed resistances. All currents are assumed to flow in the same rotational direction.

**Equations (Σ voltage drops = source voltage in each loop)**

- 30·I₁ − 20·I₂ = 12
- −20·I₁ + 80·I₂ − 40·I₃ = 0
- −40·I₂ + 50·I₃ = −6

**Input data:** the 3×3 matrix A of resistances and the vector of source voltages (see the code).

**Output**

```
Mesh currents (mA): [461.54  92.31 -46.15]
Residual norm: 6.1e-16
Determinant of A: 52000.0
Condition number: 8.51
Current through shared 20 ohm resistor: 369.23 mA
Current through shared 40 ohm resistor: 138.46 mA
Power dissipated in resistors: 5815.385 mW
Power supplied by sources:     5815.385 mW
```

**Interpretation:**
- Mesh 1 carries about 461.5 mA and mesh 2 about 92.3 mA. **Mesh 3 is negative (−46.2 mA)**, so its current actually flows in the opposite direction to the one assumed. A negative sign is not an error, only a direction.
- The current in a resistor shared by two meshes is the **difference** of the mesh currents, for example I₁ − I₂ = 369.2 mA through the 20 Ω resistor.
- The residual norm (about 10⁻¹⁶) is zero apart from floating-point round-off (see Task 4), so the solution satisfies all three equations.
- The determinant (52,000) is non-zero, so the circuit has a unique solution. The condition number (8.5) is small, so the system is well-conditioned: small errors in resistor values will not cause large errors in the currents.
- **Energy check:** power dissipated in the resistors (5815.385 mW) equals power supplied by the sources (5815.385 mW), as the law of conservation of energy requires. This is an independent confirmation that the solution is correct.

---

## Repository checklist
- [ ] `Task_06/` folder pushed to **your own** GitHub repo
- [ ] Both `.py` files and this README included
- [ ] GitHub link uploaded on VLMS
