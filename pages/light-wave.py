import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Title and description
st.title("Light Wave Simulation")
st.write("""
This simulation visualizes light as a transverse wave. 
Adjust the wavelength and frequency to see how the wave changes. 
Check the 'Animate' box to see the wave propagate over time.
Note: Units are arbitrary, and the wave speed is slowed down for visualization purposes.
""")

# Interactive sliders for wave parameters
wavelength = st.slider("Wavelength", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
frequency = st.slider("Frequency", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Checkbox to toggle animation
animate = st.checkbox("Animate")

# Define wave parameters
A = 1  # Amplitude (fixed at 1 for simplicity)
k = 2 * np.pi / wavelength  # Wave number (k = 2π/λ)
omega = 2 * np.pi * frequency  # Angular frequency (ω = 2πf)

# Spatial coordinates
x = np.linspace(0, 10, 1000)  # Position array from 0 to 10 with 1000 points

# Animation or static plot based on user input
if animate:
    # Create a placeholder for dynamic updates
    placeholder = st.empty()
    
    # Run animation for 100 frames
    num_frames = 100
    for frame in range(num_frames):
        # Calculate time for this frame
        t = frame * 0.1
        
        # Compute wave amplitude at this time
        y = A * np.sin(k * x - omega * t)
        
        # Create and configure the plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_ylim(-1.5, 1.5)  # Fixed y-axis limits to show wave clearly
        ax.set_xlabel("Position")
        ax.set_ylabel("Amplitude")
        ax.set_title(f"Light Wave at t = {t:.1f}")
        
        # Update the placeholder with the new plot
        placeholder.pyplot(fig)
        
        # Close the figure to prevent memory buildup
        plt.close(fig)
        
        # Control animation speed
        time.sleep(0.1)
else:
    # Display a static plot at t=0 when animation is off
    t = 0
    y = A * np.sin(k * x - omega * t)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("Position")
    ax.set_ylabel("Amplitude")
    ax.set_title("Light Wave at t = 0")
    st.pyplot(fig)