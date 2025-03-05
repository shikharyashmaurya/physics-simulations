import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Sound Wave Simulation")

# Create sliders for adjusting the simulation parameters.
amplitude = st.slider("Amplitude", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
frequency = st.slider("Frequency (Hz)", min_value=1, max_value=20, value=5)
phase_speed = st.slider("Speed", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

# Button to start the simulation
simulate = st.button("Simulate Sound Wave")

# Placeholder for the animated plot
plot_placeholder = st.empty()

if simulate:
    # Create a spatial domain for the simulation.
    x = np.linspace(0, 2 * np.pi, 400)
    # Run the simulation for a fixed number of frames.
    for i in range(200):
        t = i * 0.05  # time increments
        # Compute the wave function: y(x, t) = A * sin(2π f (x - vt))
        y = amplitude * np.sin(2 * np.pi * frequency * (x - phase_speed * t))
        
        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_ylim(-2, 2)
        ax.set_title("Sound Wave")
        ax.set_xlabel("Distance")
        ax.set_ylabel("Amplitude")
        
        # Update the placeholder with the new plot
        plot_placeholder.pyplot(fig)
        plt.close(fig)
        
        # Delay to control the animation speed
        time.sleep(0.05)
