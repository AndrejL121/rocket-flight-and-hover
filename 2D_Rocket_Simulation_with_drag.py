import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation


def simulate_rocket(thrust, dry_mass, fuel_mass, fuel_usage, angle_deg, drag_k=0.0):
    time = 0       # time step, seconds
    gravity = 9.81   # metres per second squared
    dt = 0.01
    burn_time = fuel_mass/fuel_usage

    y = 0
    x = 0
    velocity_x = 0.0
    velocity_y = 0.0

    theta = math.radians(angle_deg)

    ys = []
    xs = []
    times = []

    while y >= 0:
        xs.append(x)
        ys.append(y)
        times.append(time)
        
        mass = dry_mass+fuel_mass

        if time < burn_time:
            current_thrust = thrust
        else:
             current_thrust = 0.0


        a_x = current_thrust * math.cos(theta) / mass - drag_k * velocity_x
        a_y = current_thrust * math.sin(theta) / mass - gravity - drag_k *velocity_y


        x += velocity_x * dt + 0.5*a_x*dt*dt
        y += velocity_y * dt + 0.5*a_y*dt*dt

        velocity_x += a_x*dt    
        velocity_y += a_y*dt

        fuel_mass = max(0.0, fuel_mass - fuel_usage * dt)
               
        time += dt

    return times, xs, ys

fig, ax = plt.subplots()
flights = []

for drag_k in [0.0, 0.1, 0.3]:
    times, xs, ys = simulate_rocket(
        thrust=15,
        dry_mass=0.7,
        fuel_mass=0.3,
        fuel_usage=0.1,
        angle_deg=80,
        drag_k=drag_k,
    )

    path, = ax.plot(xs, ys, label=f"Drag coefficient = {drag_k} 1/s")

    peak = ys.index(max(ys))
    ax.scatter(xs[peak], ys[peak], color=path.get_color(), zorder=3)
    print(f"Drag {drag_k}: peak height {ys[peak]:.2f} m at {times[peak]:.2f} s")

    print(
        f"Drag = {drag_k}: "
        f"maximum height = {max(ys):.2f} m, "
        f"approximate range = {xs[-1]:.2f} m"
    )

    rocket, = ax.plot([], [], "o", color=path.get_color())
    flights.append((rocket, times, xs, ys))

ax.set_xlabel("Horizontal distance (metres)")
ax.set_ylabel("Height (metres)")
ax.set_title("Effect of linear drag on rocket trajectory")
ax.set_aspect("equal")
ax.grid()
ax.legend()

clock = ax.text(0.03, 0.95, "", transform=ax.transAxes, va="top")

all_times = [times for rocket, times, xs, ys in flights]
shared_times = max(all_times, key=len)

def update(i):
    for rocket, times, xs, ys in flights:
        last_index = len(xs) - 1
        j = min(i, last_index)
        rocket.set_data([xs[j]], [ys[j]])

    clock.set_text(f"Time = {shared_times[i]:.2f} s")

frames = list(range(0, len(shared_times) - 1, 5))
frames.append(len(shared_times) - 1)

animation = FuncAnimation(fig, update, frames=frames, interval=50, repeat=False)
plt.show()