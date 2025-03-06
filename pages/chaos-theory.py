import streamlit as st
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define the Lorenz system
def lorenz(state, t, sigma, beta, rho):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

# Title and description
st.title("Lorenz Attractor - Chaos Theory Visualization")
st.write(
    "This simulation visualizes the Lorenz attractor, a system that exhibits chaotic behavior. "
    "Adjust the parameters using the sidebar to see how the system's trajectory changes."
)

# Sidebar for interactive parameter controls
st.sidebar.header("Simulation Parameters")
sigma = st.sidebar.slider("Sigma (σ)", 0.1, 20.0, 10.0)
beta = st.sidebar.slider("Beta (β)", 0.1, 10.0, 8.0/3.0, step=0.1)
rho = st.sidebar.slider("Rho (ρ)", 0.1, 50.0, 28.0, step=0.1)

initial_x = st.sidebar.number_input("Initial x", value=1.0)
initial_y = st.sidebar.number_input("Initial y", value=1.0)
initial_z = st.sidebar.number_input("Initial z", value=1.0)

t_max = st.sidebar.number_input("Simulation Time", value=40.0, min_value=1.0)
num_points = st.sidebar.number_input("Number of Points", value=10000, min_value=100, step=100)

# Time array for simulation
t = np.linspace(0, t_max, num_points)

# Initial state and integration of the Lorenz equations
state0 = [initial_x, initial_y, initial_z]
states = odeint(lorenz, state0, t, args=(sigma, beta, rho))

# Plotting the Lorenz attractor
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(states[:, 0], states[:, 1], states[:, 2], lw=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Lorenz Attractor")

st.pyplot(fig)
