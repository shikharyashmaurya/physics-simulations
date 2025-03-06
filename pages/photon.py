import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Set up the Streamlit interface
st.title("Photon Emission Simulation")
st.write("This simulation shows photons being emitted from a central light source and traveling outward in straight lines.")

# Create the figure and axis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')  # Ensure the plot is square
ax.set_xticks([])       # Remove x-axis ticks
ax.set_yticks([])       # Remove y-axis ticks

# Plot the light source at the origin
ax.scatter([0], [0], color='red', s=100, label='Light Source')

# Initialize lists to store photon positions and velocities
positions = []
velocities = []
v = 0.5  # Speed of photons (arbitrary units per frame)

# Create a placeholder for the plot in Streamlit
placeholder = st.empty()

# Run the animation for 100 frames
for i in range(100):
    # Add a new photon at the source with a random direction
    theta = np.random.uniform(0, 2 * np.pi)  # Random angle in radians
    vx = v * np.cos(theta)                   # x-component of velocity
    vy = v * np.sin(theta)                   # y-component of velocity
    positions.append([0.0, 0.0])             # Start at origin
    velocities.append([vx, vy])
    
    # Update the position of each photon
    for j in range(len(positions)):
        positions[j][0] += velocities[j][0]
        positions[j][1] += velocities[j][1]
    
    # Remove photons that go out of bounds (beyond x=±10 or y=±10)
    indices_to_keep = [
        j for j in range(len(positions))
        if abs(positions[j][0]) < 10 and abs(positions[j][1]) < 10
    ]
    positions = [positions[j] for j in indices_to_keep]
    velocities = [velocities[j] for j in indices_to_keep]
    
    # Clear the previous plot and redraw
    ax.clear()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.scatter([0], [0], color='red', s=100)  # Redraw the source
    
    # Plot the photons if there are any
    if positions:
        pos_array = np.array(positions)
        ax.scatter(pos_array[:, 0], pos_array[:, 1], color='blue', s=10)
    
    # Update the plot in the Streamlit placeholder
    placeholder.pyplot(fig)
    
    # Pause briefly to control animation speed
    time.sleep(0.1)