import numpy as np
import time
from scipy.linalg import lu_factor, lu_solve

# A structure modelled as a chain of n nodes joined by springs (stiffness matrix K).
# Engineers must test many load cases f (e.g. different traffic or wind loads)
# on the SAME structure, solving K u = f for the displacements u.
#
# Assumptions: every spring has stiffness 100,000 N/mm, the first node is fixed to the
# ground, and loads are random forces between 0 and 50 N on each node.
n = 500
k = 100_000.0
cases = 2000

K = np.zeros((n, n))
for i in range(n):
    K[i, i] = 2 * k
    if i > 0:
        K[i, i - 1] = -k
    if i < n - 1:
        K[i, i + 1] = -k
K[-1, -1] = k           # free end

rng = np.random.default_rng(1)
loads = rng.uniform(0, 50, size=(cases, n))

# Method 1: repeat full elimination for every load case
t0 = time.perf_counter()
sol_direct = np.array([np.linalg.solve(K, f) for f in loads])
t_direct = time.perf_counter() - t0

# Method 2: factor once, reuse L and U for every load case
t0 = time.perf_counter()
lu, piv = lu_factor(K)
sol_lu = np.array([lu_solve((lu, piv), f) for f in loads])
t_lu = time.perf_counter() - t0

print("Both methods agree:", np.allclose(sol_direct, sol_lu))
print(f"Repeated np.linalg.solve ({cases} cases): {t_direct:.3f} s")
print(f"LU factor once + reuse   ({cases} cases): {t_lu:.3f} s")
print(f"Speed-up: {t_direct / t_lu:.1f}x")

worst = np.max([np.linalg.norm(f - K @ u) for f, u in zip(loads[:50], sol_lu[:50])])
print(f"Largest residual norm (first 50 cases): {worst:.2e}")
tip = sol_lu[:, -1]
print(f"Free-end displacement: mean {tip.mean():.1f} mm, max {tip.max():.1f} mm")
print(f"Heaviest load case total: {loads.sum(axis=1).max():.0f} N")
