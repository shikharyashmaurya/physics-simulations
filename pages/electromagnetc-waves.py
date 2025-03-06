import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 4*np.pi)
ax.set_ylim(-2, 2)
ax.set_xlabel("Position (m)")
ax.set_ylabel("Field Strength")
ax.grid(True)

# Initialize empty lines for E and B fields
e_line, = ax.plot([], [], lw=2, label='Electric Field (E)')
b_line, = ax.plot([], [], lw=2, label='Magnetic Field (B)')
ax.legend()

# Widgets in sidebar
st.sidebar.header("Wave Parameters")
frequency = st.sidebar.slider("Frequency (Hz)", 1, 20, 5)
wavelength = st.sidebar.slider("Wavelength (m)", 1, 10, 5)
amplitude = st.sidebar.slider("Amplitude (V/m)", 0.1, 2.0, 1.0)

# Animation function
def animate(i):
    x = np.linspace(0, 4*np.pi, 1000)
    phase = 2 * np.pi * frequency * (i/30)
    
    # Electric field (y-direction)
    e = amplitude * np.sin((2*np.pi*x)/wavelength - phase)
    
    # Magnetic field (z-direction, scaled by 1/c)
    b = (amplitude/3e8) * np.sin((2*np.pi*x)/wavelength - phase)
    
    e_line.set_data(x, e)
    b_line.set_data(x, b)
    return e_line, b_line

# Create and display animation
ani = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
st.pyplot(fig)
