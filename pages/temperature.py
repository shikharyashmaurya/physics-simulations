import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Temperature Distribution Simulation")

st.markdown("""
This simulation visualizes the evolution of temperature along a 1D rod using the heat equation:

\[
\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}
\]

We discretize space and time and update the temperature profile using the explicit finite difference method.
""")

# Simulation parameters from user inputs
length = st.sidebar.slider("Rod Length", min_value=10, max_value=100, value=50)
N = st.sidebar.slider("Number of Spatial Points", min_value=50, max_value=500, value=100)
alpha = st.sidebar.slider("Thermal Diffusivity (α)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
time_steps = st.sidebar.slider("Number of Time Steps", min_value=100, max_value=1000, value=500)
dt = st.sidebar.slider("Time Step Size (dt)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)

dx = length / (N - 1)

# Stability check for the explicit finite difference method (CFL condition)
if dt > dx**2 / (2 * alpha):
    st.warning("The chosen time step may be too large for stability. Consider reducing dt.")

# Define the spatial domain
x = np.linspace(0, length, N)

# Initial condition: base temperature with a Gaussian peak in the center
base_temp = 20  # base temperature in °C
u = np.ones(N) * base_temp
u += 80 * np.exp(-((x - length/2)**2) / (2 * (length/10)**2))

# Create a placeholder for the plot
plot_placeholder = st.empty()

st.markdown("### Simulation Running...")

# Simulation loop
for t in range(time_steps):
    # Create a new temperature array
    u_new = u.copy()
    
    # Update interior points using the finite difference method
    for i in range(1, N - 1):
        u_new[i] = u[i] + dt * alpha * (u[i + 1] - 2 * u[i] + u[i - 1]) / dx**2
    u = u_new
    
    # Plot the temperature distribution
    fig, ax = plt.subplots()
    ax.plot(x, u, color='r', lw=2, label="Temperature")
    ax.set_xlabel("Position along the rod")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title(f"Time step {t+1}/{time_steps}")
    ax.legend()
    ax.set_ylim(0, base_temp + 90)
    
    # Update the plot in the Streamlit app
    plot_placeholder.pyplot(fig)
    
    # A short delay for animation effect
    time.sleep(0.05)
