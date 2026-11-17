# Task 5: Matrix Algebra and Matrix Operations

## B. Inputs and mathematical operations

**Input values**

| Input | Value | Meaning |
|---|---|---|
| `points` | (0,0), (1,0), (1,1), (0,1) | Corners of a unit square, one per row |
| `angle` | 45° (converted to radians) | Rotation angle |
| `scale` | diag(2.0, 1.5) | Stretch x by 2 and y by 1.5 |

**Operations performed**

| Operation | Mathematics | Code |
|---|---|---|
| Rotation matrix | R = [[cos θ, −sin θ], [sin θ, cos θ]] | `rotation` |
| Scaling matrix | S = [[2, 0], [0, 1.5]] | `scale` |
| Combined transformation | T = R·S (scale first, then rotate) | `rotation @ scale` |
| Transform all points | p′ = T·p for every point | `points @ transformation.T` |
| Determinant | det(T) | `np.linalg.det()` |

The points are stored as rows, so the code multiplies by the **transpose** of T. This gives the same result as applying T to each column vector.

## C. Changing an input

**Change:** rotation angle changed from 45° to 90°, and x-scale changed from 2.0 to 3.0.

| | Original | Changed |
|---|---|---|
| Point (1,0) goes to | (1.414, 1.414) | (≈0, 3.0) |
| Point (1,1) goes to | (0.354, 2.475) | (−1.5, 3.0) |
| Point (0,1) goes to | (−1.061, 1.061) | (−1.5, ≈0) |
| Determinant | 3.0 | **4.5** |

**Explanation:**
- At 90° the shape is turned a quarter turn. The x-stretch (3.0) now points up the y-axis, so the point (1,0) lands at height 3. The original y-stretch (1.5) points along the negative x-axis, so the shape extends from x = −1.5 to 0.
- The determinant changed from 2 × 1.5 = 3 to 3 × 1.5 = 4.5. **The determinant is the area scale factor**, so the unit square (area 1) became a rectangle of area 4.5.
- Rotation never changes the determinant (it is always 1). Only the scaling changes it.
- Values like `1.8e-16` in the changed output are floating-point round-off (see Task 4) and should be read as 0.

## D. Meaning of the output

```
Transformed points:
 [[ 0.          0.        ]
  [ 1.41421356  1.41421356]
  [ 0.35355339  2.47487373]
  [-1.06066017  1.06066017]]
Determinant: 2.9999999999999996
```

- The square was stretched into a rectangle and then rotated by 45°. The corner (0,0) stays at the origin, because matrix transformations leave the origin fixed.
- The corner (1,0) moved to (1.414, 1.414). It was stretched to length 2 and turned 45°, so x and y are equal (2·cos 45° ≈ 1.414).
- The determinant is 3, which means the shape's area is **3 times larger** than the original (2 × 1.5). It is positive, so the shape is rotated but not mirrored. The value 2.9999999999999996 is round-off for exactly 3.
- A non-zero determinant also means the matrix is invertible, so the transformation can be undone.
- No graph is produced in this task.

## E. Modified program: land survey coordinate conversion

**File:** `Task_05_modified_land_survey.py`

**Real-world case:** a surveyor sketches a rectangular farm plot on a map grid. The sketch must be converted to real ground coordinates, which needs scaling (map units to metres), rotation (the map is not aligned to north) and translation (position in the survey system).

**Assumptions**
1. The plot is a 4 × 2 map-unit rectangle.
2. 1 map unit = 25 m on the ground.
3. The map is rotated 30° clockwise from true north.
4. The plot origin sits at (500 m, 300 m) in the survey coordinate system.
5. The ground is flat, so a 2-D model is adequate.

**New technique:** **homogeneous coordinates**. Translation is not a 2×2 matrix operation, so points are written as (x, y, 1) and a 3×3 matrix is used. This lets scaling, rotation and translation be combined into one matrix M = T·R·S. The program also uses `np.linalg.inv` to convert back.

**Input data:** the five corner points of the plot (the first is repeated to close the outline), plus the scale, angle and shift above.

**Output**

```
Combined 3x3 matrix:
 [[ 21.651  12.5   500.   ]
  [-12.5    21.651 300.   ]
  [  0.      0.      1.   ]]
Ground coordinates (m):
 [[500.  300. ]
  [586.6 250. ]
  [611.6 293.3]
  [525.  343.3]
  [500.  300. ]]
Determinant of linear part: 625.0
Plot area on map : 8.0 square units
Plot area on ground: 5000 m2 = 0.500 hectares
Round trip recovers original map points: True
```

**Graph interpretation (`land_survey_plot.png`):**
- The left panel shows the plot as sketched: a 4 × 2 rectangle aligned with the axes.
- The right panel shows the same plot in ground coordinates. It is a rectangle of the same shape, much larger (100 m × 50 m), tilted by 30° and located near (500–610 m, 250–345 m).
- Because the transformation has no shearing, angles and proportions are preserved. Only size, orientation and position change.

**Interpretation of results:**
- The determinant 625 equals 25², the area scale factor from map units to square metres (rotation does not change area). The map area of 8 units therefore becomes 8 × 625 = **5,000 m² = 0.5 hectares**.
- `Round trip recovers original map points: True` confirms the inverse matrix correctly undoes the conversion, which is needed to plot ground survey data back onto the map.
- The same approach is used in GIS software, computer graphics, and robot navigation.

