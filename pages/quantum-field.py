import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("1D Klein–Gordon Field Simulation")
st.markdown(
    """
This simulation visualizes the dynamics of a free scalar field governed by the Klein–Gordon equation in one spatial dimension:

$$
\\frac{\\partial^2 \\phi}{\\partial t^2} = \\frac{\\partial^2 \\phi}{\\partial x^2} - m^2\\phi.
$$

This is a classical evolution of the field, which is a stepping stone toward understanding quantum field theory.
    """
)

# Sidebar parameters for the simulation
L = st.sidebar.slider("Domain Length (L)", 10.0, 100.0, 50.0)
N = st.sidebar.slider("Number of Spatial Points", 100, 1000, 200, step=10)
dx = L / N
dt = st.sidebar.slider("Time Step (dt)", 0.001, 0.1, 0.01)
m = st.sidebar.slider("Mass (m)", 0.0, 10.0, 1.0)
sim_delay = st.sidebar.slider("Simulation Delay (sec)", 0.001, 0.1, 0.01)

# Create spatial grid
x = np.linspace(-L/2, L/2, N)

# Initial conditions: a Gaussian pulse centered at x=0
phi = np.exp(-x**2)
phi_prev = phi.copy()  # For leapfrog integration

# Define the Laplacian with periodic boundary conditions using np.roll
def laplacian(phi, dx):
    return (np.roll(phi, -1) - 2 * phi + np.roll(phi, 1)) / dx**2

# Set up the figure for plotting
fig, ax = plt.subplots()
line, = ax.plot(x, phi, lw=2)
ax.set_ylim(-1.5, 1.5)
ax.set_title("Field Configuration")
ax.set_xlabel("x")
ax.set_ylabel("$\\phi(x,t)$")
plot_placeholder = st.empty()

# Run simulation when button is clicked
if st.button("Start Simulation"):
    num_steps = 500  # Total time steps for the simulation
    for i in range(num_steps):
        # Leapfrog update:
        #   phi_next = 2*phi - phi_prev + dt^2*(phi_xx - m^2 * phi)
        phi_next = 2 * phi - phi_prev + dt**2 * (laplacian(phi, dx) - m**2 * phi)
        
        # Update variables for next step
        phi_prev = phi.copy()
        phi = phi_next.copy()
        
        # Update the plot
        line.set_ydata(phi)
        ax.set_title(f"Time step: {i}")
        plot_placeholder.pyplot(fig)
        
        # Delay to make the animation visible
        time.sleep(sim_delay)
