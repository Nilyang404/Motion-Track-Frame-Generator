import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def bezier_curve(points, num_frames):
    """ Generate Bezier curve trajectory """
    n = len(points) - 1  # Number of control points
    t_vals = np.linspace(0, 1, num_frames)**1.5  # Accelerated time distribution
    curve = np.zeros((num_frames, 2))

    for i in range(n+1):
        binomial_coeff = comb(n, i)  # Compute binomial coefficient
        curve += binomial_coeff * ((1 - t_vals) ** (n - i))[:, None] * (t_vals ** i)[:, None] * points[i]

    return curve[:, 0], curve[:, 1]

def generate_stretched_curve(start, end, num_frames, curve_factor=0.5):
    """ Generate a curved trajectory ensuring acceleration """
    x0, y0 = start
    x1, y1 = end

    # Determine the X offset direction of the control point
    offset_x = np.sign(x1 - x0) * abs(x1 - x0) * curve_factor
    if x0 == x1:
        offset_x = -abs(y1 - y0) * curve_factor  # Offset to the left for vertical direction

    # Determine the Y offset of the control point to ensure upward curvature
    control_x = (x0 + x1) / 2 + offset_x
    control_y = max(y0, y1) + curve_factor * abs(x1 - x0) + abs(y1 - y0)/2

    # Three key points of the Bezier curve
    bezier_points = np.array([
        [x0, y0],  # Start point
        [control_x, control_y],  # Control point
        [x1, y1]   # End point
    ])

    # Generate Bezier curve
    x_vals, y_vals = bezier_curve(bezier_points, num_frames)

    return x_vals, y_vals

# Example: different test cases
test_cases = [
    ((0, 0), (5, 5), 60, 0.5),   # Start on the left, end on the right
    ((5, 0), (0, 5), 60, 0.5),   # Start on the right, end on the left
    ((2, 0), (2, 5), 60, 0.5),   # Vertical movement (should shift left)
]

# Plot all test trajectories
plt.figure(figsize=(6, 6))
for start, end, frames, factor in test_cases:
    x_vals, y_vals = generate_stretched_curve(start, end, frames, factor)
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', markersize=3, label=f"Start {start} → End {end}")

# Visualization
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Stretched Curve with Directional Offset")
plt.grid()
plt.legend()
plt.show()
