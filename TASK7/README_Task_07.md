# Task 7: Gaussian Elimination and LU Decomposition

## B. Inputs and mathematical operations

**Input values**

| Input | Value |
|---|---|
| Coefficient matrix A (3×3) | [[4, −1, 0], [−1, 4, −1], [0, −1, 3]] |
| Measurement vector b₁ | [15, 10, 10] |
| Measurement vector b₂ | [16, 11, 9] |
| Measurement vector b₃ | [14, 12, 11] |

The same matrix A is used with three different right-hand sides, as in a simulation that receives a new measurement every second.

**Operations performed**

| Operation | Meaning | Code |
|---|---|---|
| LU factorisation | Write PA = LU, where L is lower triangular, U is upper triangular and P records row swaps | `lu_factor(A)` |
| Solve for each b | Forward substitution (Ly = Pb), then back substitution (Ux = y) | `lu_solve((lu, piv), b)` |
| Residual | r = b − A·x | `np.linalg.norm(residual)` |
| Comparison | Full direct solve for the first set | `np.linalg.solve()` |

**Why it is efficient:** factoring A is the expensive step (about n³ operations). Each solve afterwards is cheap (about n² operations). Factoring **once** and reusing L and U is therefore faster than repeating elimination for every new b.

For this A, the factors are (computed separately for this document):

- L = [[1, 0, 0], [−0.25, 1, 0], [0, −0.267, 1]]
- U = [[4, −1, 0], [0, 3.75, −1], [0, 0, 2.733]]

## C. Changing an input

**Change:** the diagonal entries A[0,0] and A[2,2] were reduced (4 → 1.2 and 3 → 1.2), with b unchanged.

| | Original | Changed |
|---|---|---|
| Solution for b₁ | [5, 5, 5] | [23.51, 13.21, 19.35] |
| Solution for b₂ | [5.32, 5.27, 4.76] | [24.70, 13.64, 18.87] |
| Condition number of A | 2.39 | 7.52 |
| Residual norm | about 10⁻¹⁵ | about 10⁻¹⁴ |

**Explanation:**
- The unknowns became several times larger. Smaller diagonal entries mean each unknown has less "resistance" against the same inputs, so the response grows. In physical terms, the system became weaker.
- The condition number (a measure of how much errors can be magnified) rose from 2.4 to 7.5. The system is still well-conditioned, but it is more sensitive to errors than before.
- LU decomposition still works and the residual is still essentially zero. The method itself is not affected by this change.
- The matrix was reduced to a weaker diagonal, so it is still invertible (determinant 3.36), but making the diagonal even smaller would eventually cause failure.

## D. Meaning of the output

```
Measurement set 1
Solution: [5. 5. 5.]
Residual norm: 0.0

Measurement set 2
Solution: [5.31707317 5.26829268 4.75609756]
Residual norm: 1.7763568394002505e-15

Measurement set 3
Solution: [4.90243902 5.6097561  5.53658537]
Residual norm: 0.0

Direct solution for first set: [5. 5. 5.]
```

- For each measurement vector the program finds the unknowns that satisfy all three equations. For b₁ the answer is exactly (5, 5, 5): 4(5) − 5 = 15 ✓.
- Small changes in the measurements (sets 2 and 3) give small changes in the answers (about 5 ± 0.5). This shows the system is stable.
- The **residual norms are essentially zero** (up to 10⁻¹⁵), which is floating-point round-off (see Task 4). The factorisation is accurate.
- The **direct solution** `np.linalg.solve` gives the same answer as the LU method for the first set, which confirms the LU result.
- No graph is produced in this task.

## E. Modified program: structural analysis with many load cases

**File:** `Task_07_modified_structural_load_cases.py`

**Real-world case:** a structure is modelled as a chain of 500 nodes joined by springs. Engineers test many load cases (traffic, wind and so on) on the same structure. The stiffness matrix K stays the same and only the load vector f changes, so we solve **K·u = f** for the displacements u. This is the pattern used in finite-element analysis.

**Assumptions**
1. 500 nodes connected in a chain by springs of stiffness 100,000 N/mm each.
2. The first node is fixed to the ground and the last end is free.
3. Each load case applies a random force between 0 and 50 N to each node.
4. 2,000 load cases are tested.
5. The behaviour is linear (displacement proportional to force) and static.

**Input data:** the 500×500 tridiagonal stiffness matrix K and 2,000 random load vectors (seed 1).

**Compared:** solving every case from scratch with `np.linalg.solve` against factoring once with `lu_factor` and reusing it with `lu_solve`.

**Output**

```
Both methods agree: True
Repeated np.linalg.solve (2000 cases): 6.901 s
LU factor once + reuse   (2000 cases): 0.183 s
Speed-up: 37.8x
Largest residual norm (first 50 cases): 1.17e-08
Free-end displacement: mean 31.3 mm, max 34.4 mm
Heaviest load case total: 13502 N
```

**Interpretation:**
- Both methods give the same displacements (`True`), but reusing the factorisation is about **38 times faster** for 2,000 load cases. Timings will differ on your machine, but the speed-up should be large.
- The residual (about 10⁻⁸) is tiny compared with the loads, which are of order 10–50 N per node, so the solutions are accurate.
- The free end moves 31 mm on average and 34 mm at most across all load cases. A designer would compare this with an allowable deflection limit to decide whether the structure is safe.
- Because K is a model assumption, this is a simplified teaching model and not a design calculation for a real structure.

