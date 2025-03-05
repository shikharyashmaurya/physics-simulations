import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Sidebar parameters for simulation control
num_particles = st.sidebar.number_input("Number of particles", min_value=10, max_value=500, value=100)
dt = st.sidebar.slider("Time step (dt)", min_value=0.01, max_value=1.0, value=0.1)
num_steps = st.sidebar.slider("Number of simulation steps", min_value=10, max_value=500, value=200)
refresh_rate = st.sidebar.slider("Refresh rate (seconds)", min_value=0.01, max_value=0.5, value=0.1)

# Initialize particle positions randomly within a region
positions = np.random.uniform(-5, 5, (num_particles, 2))

def velocity_field(x, y):
    """
    Defines a vortex velocity field centered at the origin.
    u = -y, v = x gives a counter-clockwise rotation.
    """
    u = -y
    v = x
    return u, v

st.title("Fluid Dynamics Simulation: Particle Advection in a Vortex")

if st.button("Start Simulation"):
    placeholder = st.empty()  # container to update the plot
    for step in range(num_steps):
        # Compute the velocity for all particles at their current positions
        u, v = velocity_field(positions[:, 0], positions[:, 1])
        # Update particle positions using Euler integration
        positions[:, 0] += u * dt
        positions[:, 1] += v * dt
        
        # Create a plot of the current particle positions
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(positions[:, 0], positions[:, 1], color='blue', s=10)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_title(f"Step {step + 1}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        
        # Update the plot in the Streamlit app
        placeholder.pyplot(fig)
        time.sleep(refresh_rate)
