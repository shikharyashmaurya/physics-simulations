import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Heat Diffusion Simulation")

# Simulation parameters
nx, ny = 50, 50  # Grid size
alpha = st.slider("Thermal Diffusivity (α)", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
dt = st.slider("Time Step (dt)", min_value=0.001, max_value=0.1, value=0.01, step=0.005)
steps = st.number_input("Number of Simulation Steps", min_value=10, max_value=1000, value=100, step=10)

# Initialize temperature field: all zeros with a hot spot in the center
T = np.zeros((nx, ny))
T[nx//2, ny//2] = 100.0

# Placeholder for plotting
plot_placeholder = st.empty()

def update_temperature(T, alpha, dt):
    """
    Update temperature using a simple finite difference scheme for the 2D heat equation.
    The update formula for interior grid points is:
    T_new[i, j] = T[i, j] + α * dt * (T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1] - 4*T[i, j])
    """
    T_new = T.copy()
    T_new[1:-1, 1:-1] = T[1:-1, 1:-1] + alpha * dt * (
        T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:] + T[1:-1, :-2] - 4 * T[1:-1, 1:-1]
    )
    return T_new

# Run the simulation loop
for i in range(int(steps)):
    T = update_temperature(T, alpha, dt)
    
    # Create the plot
    fig, ax = plt.subplots()
    heatmap = ax.imshow(T, cmap='hot', interpolation='nearest')
    ax.set_title(f"Step {i+1}")
    ax.axis('off')
    
    # Display the plot in the Streamlit placeholder
    plot_placeholder.pyplot(fig)
    
    # Pause to simulate time evolution (adjust the sleep time as needed)
    time.sleep(0.1)
