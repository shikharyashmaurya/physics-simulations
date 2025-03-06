import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.title("Lorenz Attractor Simulation")
st.write("Visualize the chaotic behavior of a nonlinear dynamical system by adjusting the parameters below:")

# Parameter sliders
sigma = st.slider("Sigma (σ)", min_value=0.1, max_value=20.0, value=10.0, step=0.1)
rho = st.slider("Rho (ρ)", min_value=0.1, max_value=50.0, value=28.0, step=0.1)
beta = st.slider("Beta (β)", min_value=0.1, max_value=10.0, value=8/3, step=0.1)

st.write(f"Current Parameters: σ = {sigma}, ρ = {rho}, β = {beta}")

# Define the Lorenz system of differential equations
def lorenz(state, t, sigma, beta, rho):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Time span for the simulation
t = np.linspace(0, 40, 10000)
# Initial conditions for x, y, z
state0 = [1.0, 1.0, 1.0]

# Integrate the Lorenz equations over time t
states = odeint(lorenz, state0, t, args=(sigma, beta, rho))
x, y, z = states[:, 0], states[:, 1], states[:, 2]

# Create a 3D plot of the Lorenz attractor
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, lw=0.5)
ax.set_title("Lorenz Attractor")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")

st.pyplot(fig)
