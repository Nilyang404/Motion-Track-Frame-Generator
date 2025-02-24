import numpy as np
import matplotlib.pyplot as plt

def generate_trajectory_with_any_acceleration(start, end, num_frames, acceleration, curve_factor=1.0):
    x0, y0 = start
    x1, y1 = end
    a_x, a_y = acceleration 


    A = 0.5 * a_y
    B = -y1 + y0
    C = 0  #
    
    discriminant = B**2 - 4*A*C

    total_time = (-B + np.sqrt(discriminant)) / (2*A) if A != 0 else -B / (A + 1e-5)

    v_x0 = (x1 - x0 - 0.5 * a_x * total_time**2) / total_time
    v_y0 = (y1 - y0 - 0.5 * a_y * total_time**2) / total_time
    v_x0 *= curve_factor
    v_y0 *= curve_factor

    times = np.linspace(0, total_time, num_frames)**1.2 


    x_vals = x0 + v_x0 * times + 0.5 * a_x * times**2
    y_vals = y0 + v_y0 * times + 0.5 * a_y * times**2

    return x_vals, y_vals


x_vals, y_vals = generate_trajectory_with_any_acceleration(
    (0, 0), (5, 5), 50, (-2, -5), 1.2)

plt.plot(x_vals, y_vals, marker='o', linestyle='-', markersize=3)
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Trajectory with Arbitrary Acceleration")
plt.grid()
plt.scatter([0, 5], [0, 5], color="red", label="Start/End")
plt.legend()
plt.show()
