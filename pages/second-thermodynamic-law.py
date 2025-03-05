import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Second Law of Thermodynamics: Diffusion Simulation")
st.markdown("""
This simulation illustrates the Second Law of Thermodynamics.
Initially, particles are confined to the left half of the container.
Over time, random motion causes them to spread out evenly.
""")

# Sidebar controls to adjust simulation parameters
num_particles = st.sidebar.slider("Number of Particles", 100, 1000, 500, step=50)
num_steps = st.sidebar.slider("Number of Steps", 100, 2000, 500, step=50)
container_size = st.sidebar.slider("Container Size", 5, 20, 10)
diffusion_scale = st.sidebar.slider("Diffusion Scale", 0.05, 1.0, 0.1, step=0.05)
update_delay = st.sidebar.slider("Update Delay (seconds)", 0.001, 0.1, 0.01, step=0.005)

# Button to start simulation
if st.button("Start Simulation"):
    # Initialize particle positions: confined to the left half
    positions = np.zeros((num_particles, 2))
    positions[:, 0] = np.random.uniform(0, container_size / 2, num_particles)
    positions[:, 1] = np.random.uniform(0, container_size, num_particles)

    # Placeholder for the plot to update in each simulation step
    plot_placeholder = st.empty()

    for step in range(num_steps):
        # Update particle positions with a random walk (diffusion)
        positions += np.random.normal(loc=0.0, scale=diffusion_scale, size=positions.shape)
        
        # Reflect particles off the container boundaries
        positions[:, 0] = np.clip(positions[:, 0], 0, container_size)
        positions[:, 1] = np.clip(positions[:, 1], 0, container_size)
        
        # Create a scatter plot for the current state
        fig, ax = plt.subplots()
        ax.scatter(positions[:, 0], positions[:, 1], s=10, color='blue')
        ax.set_xlim(0, container_size)
        ax.set_ylim(0, container_size)
        ax.set_title(f"Step {step + 1}/{num_steps}")
        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        
        # Update the plot in the Streamlit app
        plot_placeholder.pyplot(fig)
        
        # Pause briefly to control update speed
        time.sleep(update_delay)
