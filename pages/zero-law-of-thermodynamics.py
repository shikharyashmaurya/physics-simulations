import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Zeroth Law of Thermodynamics Simulation")
st.write("""
This simulation visualizes how three systems, each with an initial temperature,
exchange heat and eventually reach thermal equilibrium.
The zeroth law of thermodynamics states that if system A is in equilibrium with system B,
and system B is in equilibrium with system C, then A and C are in equilibrium.
""")

# Adjustable parameters
k = st.slider("Heat Transfer Coefficient (k)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
T_A0 = st.number_input("Initial Temperature of System A (°C)", value=100.0)
T_B0 = st.number_input("Initial Temperature of System B (°C)", value=50.0)
T_C0 = st.number_input("Initial Temperature of System C (°C)", value=25.0)
total_time = st.number_input("Total Simulation Time (seconds)", value=20.0)
dt = 0.1  # time step

# Time array
time_array = np.arange(0, total_time, dt)
num_steps = len(time_array)

# Initialize temperature arrays for each system
T_A = np.zeros(num_steps)
T_B = np.zeros(num_steps)
T_C = np.zeros(num_steps)

T_A[0] = T_A0
T_B[0] = T_B0
T_C[0] = T_C0

# Simulation: update the temperatures using a simple Euler method.
# System A exchanges heat with B.
# System C exchanges heat with B.
# System B is connected to both A and C.
for i in range(1, num_steps):
    dT_A = k * (T_B[i-1] - T_A[i-1])
    dT_B = k * ((T_A[i-1] - T_B[i-1]) + (T_C[i-1] - T_B[i-1]))
    dT_C = k * (T_B[i-1] - T_C[i-1])
    
    T_A[i] = T_A[i-1] + dT_A * dt
    T_B[i] = T_B[i-1] + dT_B * dt
    T_C[i] = T_C[i-1] + dT_C * dt

# Plot the results using Matplotlib
fig, ax = plt.subplots()
ax.plot(time_array, T_A, label="System A", color='red')
ax.plot(time_array, T_B, label="System B", color='green')
ax.plot(time_array, T_C, label="System C", color='blue')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Thermal Equilibrium Through Heat Exchange")
ax.legend()
st.pyplot(fig)
