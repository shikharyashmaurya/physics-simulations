import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Wave Simulation")

# Sidebar sliders for simulation parameters
amplitude = st.sidebar.slider("Amplitude (A)", 0.1, 5.0, 1.0, step=0.1)
frequency = st.sidebar.slider("Frequency (ω)", 0.1, 10.0, 1.0, step=0.1)
phase = st.sidebar.slider("Phase (φ)", 0.0, 2 * np.pi, 0.0, step=0.1)
speed = st.sidebar.slider("Speed (v)", 0.1, 5.0, 1.0, step=0.1)

st.markdown(r"**Wave Equation:** $y(x,t) = A \sin\big(\omega (x - vt) + \phi\big)$")

# Placeholder for the plot that will be updated in the loop
plot_placeholder = st.empty()

# Define x range for the wave
x = np.linspace(0, 4 * np.pi, 400)
t = 0

# Infinite loop to update the plot continuously.
# Adjust time.sleep() to control the speed of animation.
while True:
    # Compute the wave at time t
    y = amplitude * np.sin(frequency * (x - speed * t) + phase)
    
    # Create a new figure for each update
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"t = {t:.2f}")
    ax.set_ylim(-amplitude - 1, amplitude + 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Traveling Wave Simulation")
    ax.legend()
    
    # Update the Streamlit plot
    plot_placeholder.pyplot(fig)
    
    # Close the figure to avoid resource warnings
    plt.close(fig)
    
    # Increment time and sleep briefly to animate
    t += 0.1
    time.sleep(0.1)
