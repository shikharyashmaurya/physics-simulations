import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.title("Resonance Visualization: Driven Damped Harmonic Oscillator")
st.write(
    "This simulation demonstrates resonance in a driven, damped oscillator. "
    "Use the sidebar to adjust the forcing amplitude, damping coefficient, and driving frequency. "
    "Watch how the displacement over time changes, and explore the resonance curve showing the steady-state amplitude."
)

# Sidebar parameters
F0 = st.sidebar.slider("Forcing Amplitude (F0)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
b = st.sidebar.slider("Damping Coefficient (b)", min_value=0.0, max_value=2.0, value=0.1, step=0.05)
omega_drive = st.sidebar.slider("Driving Frequency (ω)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

# Physical parameters
m = 1.0   # mass
k = 1.0   # spring constant (thus natural frequency ω₀ = sqrt(k/m) = 1)

# Time settings
t = np.linspace(0, 50, 1000)

# Define the differential equation for the oscillator
def oscillator(state, t):
    x, v = state
    # dx/dt = v, and dv/dt comes from: m*x'' + b*x' + k*x = F0*cos(omega_drive*t)
    dxdt = v
    dvdt = (F0 * np.cos(omega_drive * t) - b * v - k * x) / m
    return [dxdt, dvdt]

# Initial conditions: starting from rest
state0 = [0.0, 0.0]
sol = odeint(oscillator, state0, t)

# Plot the displacement vs time
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, sol[:, 0], label="Displacement x(t)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Displacement (m)")
ax.set_title("Driven Damped Harmonic Oscillator Response")
ax.legend()
st.pyplot(fig)

# Plot the resonance curve: steady-state amplitude vs driving frequency
st.header("Steady-State Amplitude vs Driving Frequency")
omega_range = np.linspace(0.1, 3.0, 300)
# The steady-state amplitude can be derived analytically:
# A = F0 / sqrt((k - m*ω²)² + (b*ω)²)
amplitudes = F0 / np.sqrt((k - m * omega_range**2)**2 + (b * omega_range)**2)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(omega_range, amplitudes, 'r-', label="Steady-State Amplitude")
ax2.set_xlabel("Driving Frequency (ω)")
ax2.set_ylabel("Amplitude")
ax2.set_title("Resonance Curve")
ax2.legend()
st.pyplot(fig2)

st.write(
    "Notice that the amplitude peaks when the driving frequency approaches the system's natural frequency (ω ≈ 1). "
    "This is the resonance phenomenon: the system responds most strongly when forced near its natural frequency."
)
