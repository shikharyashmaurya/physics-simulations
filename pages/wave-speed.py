import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Wave Speed Visualization")

# Sidebar: Set simulation parameters
st.sidebar.header("Simulation Parameters")
amplitude = st.sidebar.slider("Amplitude", 0.1, 5.0, 1.0, step=0.1)
frequency = st.sidebar.slider("Frequency (Hz)", 0.1, 5.0, 1.0, step=0.1)
wave_speed = st.sidebar.slider("Wave Speed", 0.1, 10.0, 2.0, step=0.1)

# Define the spatial domain for the wave
x = np.linspace(0, 10, 500)

# Create a placeholder for updating the plot
placeholder = st.empty()

# Record the starting time
start_time = time.time()

# Animation loop
while True:
    # Calculate elapsed time
    t = time.time() - start_time

    # Compute wave values: y = A * sin(2πf(x - vt))
    y = amplitude * np.sin(2 * np.pi * frequency * (x - wave_speed * t))
    
    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"t = {t:.2f} s")
    ax.set_ylim([-amplitude * 1.2, amplitude * 1.2])
    ax.set_title("Wave Propagation")
    ax.set_xlabel("Position")
    ax.set_ylabel("Amplitude")
    ax.legend()
    
    # Update the plot in the Streamlit app
    placeholder.pyplot(fig)
    
    # Small delay to control animation speed
    time.sleep(0.05)
