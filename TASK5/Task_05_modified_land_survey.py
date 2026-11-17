import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# A surveyor sketched a rectangular plot on a map grid (1 unit = 1 map square).
# Corners (row = [x, y]); first point repeated at the end to close the shape.
plot_map = np.array([
    [0.0, 0.0],
    [4.0, 0.0],
    [4.0, 2.0],
    [0.0, 2.0],
    [0.0, 0.0]
])

# Assumptions
metres_per_unit = 25.0          # 1 map unit = 25 m on the ground
north_offset = np.deg2rad(-30)  # map is rotated 30 degrees clockwise from true north
shift_x, shift_y = 500.0, 300.0 # position of plot origin in the survey coordinate system (m)

scale = np.array([[metres_per_unit, 0.0],
                  [0.0, metres_per_unit]])
rotation = np.array([[np.cos(north_offset), -np.sin(north_offset)],
                     [np.sin(north_offset),  np.cos(north_offset)]])

# Homogeneous coordinates let translation be done with a single matrix multiplication
T = np.array([[1.0, 0.0, shift_x],
              [0.0, 1.0, shift_y],
              [0.0, 0.0, 1.0]])
R = np.eye(3); R[:2, :2] = rotation
S = np.eye(3); S[:2, :2] = scale

M = T @ R @ S      # scale first, then rotate, then shift

homog = np.hstack([plot_map, np.ones((len(plot_map), 1))])
ground = (homog @ M.T)[:, :2]

area_map = 4.0 * 2.0
det_linear = np.linalg.det(rotation @ scale)
area_ground = area_map * det_linear

print("Combined 3x3 matrix:\n", np.round(M, 3))
print("Ground coordinates (m):\n", np.round(ground, 2))
print(f"Determinant of linear part: {det_linear:.1f}")
print(f"Plot area on map : {area_map:.1f} square units")
print(f"Plot area on ground: {area_ground:.0f} m2 = {area_ground/10000:.3f} hectares")

# Inverse matrix: convert ground coordinates back to map coordinates
back = (np.hstack([ground, np.ones((len(ground), 1))]) @ np.linalg.inv(M).T)[:, :2]
print("Round trip recovers original map points:", np.allclose(back, plot_map))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
ax1.plot(plot_map[:, 0], plot_map[:, 1], "o-")
ax1.set_title("Map sketch (map units)")
ax2.plot(ground[:, 0], ground[:, 1], "s-", color="tab:orange")
ax2.set_title("Ground coordinates (metres)")
for ax in (ax1, ax2):
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(True); ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("land_survey_plot.png", dpi=120)
