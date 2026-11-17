import numpy as np

# Hourly readings (deg C) from an IoT sensor in a rural clinic vaccine fridge
# Safe range for most vaccines: 2 C to 8 C
fridge_c = np.array([
    4.2, 4.0, 3.9, 4.1, 4.3, 4.6,
    5.2, 6.1, 7.0, 7.9, 8.6, 9.3,
    9.8, 9.1, 8.2, 7.1, 6.0, 5.1,
    4.7, 4.4, 4.2, 4.0, 3.9, 4.1
])
LOW, HIGH = 2.0, 8.0

mean_t, min_t, max_t = fridge_c.mean(), fridge_c.min(), fridge_c.max()

# Boolean mask: True where reading is outside the safe range
unsafe = (fridge_c < LOW) | (fridge_c > HIGH)
hours_unsafe = unsafe.sum()
unsafe_hours_index = np.where(unsafe)[0]   # hour of day (0-23)

# Vectorized conversion to Fahrenheit
fridge_f = 1.8 * fridge_c + 32

print(f"Mean: {mean_t:.2f} C | Min: {min_t:.2f} C | Max: {max_t:.2f} C")
print(f"Hours outside {LOW}-{HIGH} C: {hours_unsafe} of {fridge_c.size}")
print("Unsafe hours (0-23):", unsafe_hours_index)
print(f"Percentage of day unsafe: {hours_unsafe / fridge_c.size:.1%}")
print(f"Peak temperature in F: {fridge_f.max():.1f} F")
