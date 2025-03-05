import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Title of the app
st.title("Conservation of Momentum Simulation")

# Sidebar for user inputs
st.sidebar.title("Parameters")
m1 = st.sidebar.slider("Mass of Object 1 (kg)", 0.1, 10.0, 1.0, step=0.1)
m2 = st.sidebar.slider("Mass of Object 2 (kg)", 0.1, 10.0, 1.0, step=0.1)
u1 = st.sidebar.slider("Initial Velocity of Object 1 (m/s)", -10.0, 10.0, 5.0, step=0.1)
u2 = st.sidebar.slider("Initial Velocity of Object 2 (m/s)", -10.0, 10.0, -3.0, step=0.1)
initial_distance = st.sidebar.slider("Initial Distance Between Objects (m)", 1.0, 20.0, 10.0, step=0.1)

# Initial positions
x1 = 0.0  # Object 1 starts at origin
x2 = initial_distance  # Object 2 starts at the initial distance

# Determine if and when a collision occurs
# For x1 < x2, collision happens if u1 > u2 (Object 1 catches up to Object 2)
if u1 > u2:
    t_collision = (x2 - x1) / (u1 - u2)
    collision_message = f"Time to collision: {t_collision:.2f} s"
else:
    t_collision = float('inf')
    collision_message = "Objects will not collide with these velocities."

st.write(collision_message)

# Calculate final velocities after elastic collision (if it occurs)
if t_collision < float('inf'):
    v1 = (u1 * (m1 - m2) + 2 * m2 * u2) / (m1 + m2)
    v2 = (u2 * (m2 - m1) + 2 * m1 * u1) / (m1 + m2)
else:
    v1 = u1  # No collision, velocities remain unchanged
    v2 = u2

# Simulation parameters
dt = 0.1  # Time step (s)
total_time = 10.0  # Total simulation time (s)

# Initialize simulation variables
pos1 = x1
pos2 = x2
vel1 = u1
vel2 = u2
collided = False
times = []
momenta1 = []
momenta2 = []
total_momenta = []

# Placeholder for the dynamic plot
placeholder = st.empty()

# Run the simulation
t = 0.0
while t < total_time:
    # Check for collision
    if not collided and t >= t_collision:
        vel1 = v1
        vel2 = v2
        collided = True
    
    # Update positions
    pos1 += vel1 * dt
    pos2 += vel2 * dt
    
    # Calculate momenta
    momentum1 = m1 * vel1
    momentum2 = m2 * vel2
    total_momentum = momentum1 + momentum2
    
    # Store data for plotting
    times.append(t)
    momenta1.append(momentum1)
    momenta2.append(momentum2)
    total_momenta.append(total_momentum)
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Top plot: Positions of the objects
    ax1.plot([pos1], [0], 'ro', markersize=10, label='Object 1 (Red)')
    ax1.plot([pos2], [0], 'bo', markersize=10, label='Object 2 (Blue)')
    ax1.set_xlim(-5, initial_distance + 5)
    ax1.set_ylim(-1, 1)
    ax1.set_xlabel('Position (m)')
    ax1.set_title(f'Time: {t:.1f} s')
    ax1.legend()
    ax1.grid(True)
    
    # Bottom plot: Momentum over time
    ax2.plot(times, momenta1, 'b-', label='Momentum of Object 1')
    ax2.plot(times, momenta2, 'g-', label='Momentum of Object 2')
    ax2.plot(times, total_momenta, 'r-', label='Total Momentum')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Momentum (kg m/s)')
    ax2.legend()
    ax2.grid(True)
    
    # Update the plot in Streamlit
    placeholder.pyplot(fig)
    plt.close(fig)
    
    # Increment time and add a delay for animation
    t += dt
    time.sleep(0.1)