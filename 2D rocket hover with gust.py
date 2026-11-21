import matplotlib.pyplot as plt
import math
import random

def simulate_hover(kp, ki, kd):     
    gravity = 9.81  
    dt = 0.01
    duration = 20.0
    mass = 1.0

    max_thrust_x = 2.0
    max_thrust_y = 20.0

    velocity_x = 0.0
    x = 0.0
    target_x = 0
    accumulated_error_x = 0.0

    kp_x = 4.0
    kd_x = 3.0
    ki_x = 0.5

    height = 0.0
    target_height = 5.0
    velocity_y = 0.0
    accumulated_error_y = 0.0

    xs = []
    heights = []
    times = []
    thrusts = []

    for step in range(round(duration / dt)):
        time = step *dt 

        wind_force = 0.25 if 4.0 <= time < 5.0 else 0.0

        #Vertical controller
        error_y = target_height - height
        correction = kp * error_y + ki *accumulated_error_y - kd * velocity_y

        requested_thrust_y = mass * (gravity + correction)
        thrust_y = min(max(requested_thrust_y, 0.0), max_thrust_y)

        #Horizontal controller
        error_x = target_x - x
        correction_x = kp_x * error_x + ki_x * accumulated_error_x - kd_x * velocity_x 
        requested_thrust_x = mass * correction_x
        thrust_x = min(max(requested_thrust_x, -max_thrust_x), max_thrust_x)

        acceleration_x = (thrust_x + wind_force) / mass

        if (0.0 <= requested_thrust_y <= max_thrust_y 
                or (requested_thrust_y > max_thrust_y and error_y < 0) 
                or (requested_thrust_y < 0.0 and error_y > 0)):
            accumulated_error_y+= error_y * dt

        if (-max_thrust_x <= requested_thrust_x <= max_thrust_x 
                or (requested_thrust_x > max_thrust_x and error_x < 0) 
                or (requested_thrust_x < -requested_thrust_x and error_x > 0)):
            accumulated_error_x+= error_x * dt

        times.append(time)
        heights.append(height)
        thrusts.append(thrust_y)
        xs.append(x)

        x += velocity_x * dt + 0.5 * acceleration_x * dt**2
        velocity_x += acceleration_x * dt


        acceleration_y = thrust_y / mass - gravity
        height += velocity_y *dt + 0.5 * acceleration_y* dt**2
        velocity_y += acceleration_y * dt

        if height <= 0.0:
            height = 0.0
            velocity_y = max(0.0, velocity_y)

    return times, heights, thrusts, xs

plt.figure()
for label, kp, ki, kd in [
    ("P only", 4.0, 0.0, 0.0),
    ("PD",     4.0, 0.0, 3.0),
    ("PID",    4.0, 1.0, 3.0),
]:
    times, heights, thrusts, xs = simulate_hover(kp, ki, kd)
    plt.plot(times, heights, label=label)

plt.axhline(5.0, color="black", linestyle="--", label="Target height")
plt.xlabel("Time (s)")
plt.ylabel("Height (m)")
plt.legend()
plt.grid()

# Second figure: all three runs have the same horizontal response.
plt.figure()
plt.plot(times, xs, label="Horizontal position")
plt.axhline(0, color="black", linestyle="--", label="Target x")
plt.axvspan(4, 5, alpha=0.15, color="gray", label="Gust")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal position (m)")
plt.legend()
plt.grid()

plt.show()