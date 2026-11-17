import numpy as np

# Three-loop resistor circuit analysed with mesh currents (Kirchhoff's voltage law).
#
#  Mesh 1: V1 = 12 V, own resistor 10 ohm, shares 20 ohm with mesh 2
#  Mesh 2: own resistor 20 ohm, shares 20 ohm with mesh 1 and 40 ohm with mesh 3
#  Mesh 3: V2 = 6 V (opposing direction), own resistor 10 ohm, shares 40 ohm with mesh 2
#
# Unknowns: I1, I2, I3 (mesh currents in amperes)
R_own = [10.0, 20.0, 10.0]
R_12, R_23 = 20.0, 40.0
V = np.array([12.0, 0.0, -6.0])

A = np.array([
    [R_own[0] + R_12,       -R_12,                 0.0],
    [-R_12,       R_own[1] + R_12 + R_23,        -R_23],
    [0.0,                   -R_23,       R_own[2] + R_23]
])

I = np.linalg.solve(A, V)
residual = V - A @ I

print("Coefficient matrix A:\n", A)
print("Mesh currents (A):", np.round(I, 5))
print("Mesh currents (mA):", np.round(I * 1000, 2))
print("Residual norm:", np.linalg.norm(residual))
print("Determinant of A:", round(np.linalg.det(A), 1))
print("Condition number:", round(np.linalg.cond(A), 2))

# Current and power in the shared resistors
I_R12 = I[0] - I[1]
I_R23 = I[1] - I[2]
print(f"Current through shared 20 ohm resistor: {I_R12*1000:.2f} mA")
print(f"Current through shared 40 ohm resistor: {I_R23*1000:.2f} mA")
total_power = sum(R_own[k] * I[k]**2 for k in range(3)) \
              + R_12 * I_R12**2 + R_23 * I_R23**2
source_power = V[0] * I[0] + V[2] * I[2]
print(f"Power dissipated in resistors: {total_power*1000:.3f} mW")
print(f"Power supplied by sources:     {source_power*1000:.3f} mW")
