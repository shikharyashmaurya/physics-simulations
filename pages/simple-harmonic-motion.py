import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Set up the app title and sidebar parameters.
st.title("Simple Harmonic Motion Simulation")

st.sidebar.header("SHM Parameters")
A = st.sidebar.slider("Amplitude (A)", 0.0, 10.0, 5.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 10.0, 2.0, 0.1)
phase = st.sidebar.slider("Phase (φ)", 0.0, 2*np.pi, 0.0, 0.1)
duration = st.sidebar.slider("Duration (seconds)", 1, 60, 20)
dt = st.sidebar.slider("Time Step (seconds)", 0.01, 0.2, 0.05)

# Button to start the simulation.
if st.button("Start Simulation"):
    t = 0.0
    placeholder = st.empty()  # Container for dynamically updating the plot.
    
    while t < duration:
        # Calculate the displacement using the SHM formula.
        x = A * np.cos(omega * t + phase)
        
        # Create a new figure for this time step.
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlim(-A-1, A+1)
        ax.set_ylim(-1.5, 1.5)
        ax.axhline(0, color="black", linestyle="--", linewidth=0.5)  # Equilibrium line
        
        # Draw the oscillator as a red circle at (x, 0).
        ax.plot(x, 0, "ro", markersize=15)
        ax.set_title(f"Time: {t:.2f} s, x = {x:.2f}")
        ax.set_xlabel("Displacement")
        ax.get_yaxis().set_visible(False)  # Hide the y-axis for clarity
        
        # Update the plot in the placeholder container.
        placeholder.pyplot(fig)
        
        # Pause for a short duration to control the update rate.
        time.sleep(dt)
        t += dt
