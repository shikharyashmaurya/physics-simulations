import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Centripetal Force Simulation")

# Sidebar parameters for tuning the simulation
mass = st.sidebar.slider("Mass (kg)", 0.1, 10.0, 1.0, 0.1)
speed = st.sidebar.slider("Speed (m/s)", 0.1, 10.0, 5.0, 0.1)
radius = st.sidebar.slider("Radius (m)", 0.5, 10.0, 3.0, 0.1)

# Calculate centripetal force: F = m * v^2 / r
centripetal_force = mass * (speed ** 2) / radius
st.sidebar.write("Centripetal Force (N):", round(centripetal_force, 2))

st.write("""
This simulation visualizes an object in uniform circular motion.
The object follows a circular path and the green arrow indicates the centripetal force,
pointing inward toward the center of the circle.
""")

if st.button("Start Simulation"):
    plot_area = st.empty()  # placeholder for updating plot

    # Time parameters for simulation
    t = 0.0
    dt = 0.05  # time step in seconds
    simulation_duration = 20  # seconds
    
    while t < simulation_duration:
        # Compute angular position (theta = omega * t, where omega = speed/radius)
        theta = (speed / radius) * t
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        # Set up the plot
        fig, ax = plt.subplots(figsize=(6,6))
        # Draw the circular path
        circle = plt.Circle((0, 0), radius, color='blue', fill=False, linestyle='--')
        ax.add_artist(circle)
        # Plot the moving object as a red dot
        ax.plot(x, y, 'ro', markersize=10)
        # Draw the centripetal force arrow (from the object pointing to the center)
        ax.arrow(x, y, -x, -y, head_width=0.2, head_length=0.3, fc='green', ec='green')
        
        # Set plot limits and formatting
        ax.set_xlim(-radius - 1, radius + 1)
        ax.set_ylim(-radius - 1, radius + 1)
        ax.set_aspect('equal', 'box')
        ax.set_title("Centripetal Force Simulation")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        
        # Update the plot in the Streamlit app
        plot_area.pyplot(fig)
        
        t += dt
        time.sleep(0.05)
