import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Streamlit app title
st.title("1D Ideal Gas Simulation for Statistical Mechanics")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")
N = st.sidebar.slider("Number of particles", 10, 500, 100, step=10)
L = st.sidebar.slider("Box length", 1.0, 10.0, 5.0, step=0.5)
v0 = st.sidebar.slider("Initial velocity scale", 0.1, 5.0, 1.0, step=0.1)

# Constants
m = 1.0  # Particle mass (arbitrary units)
k = 1.0  # Boltzmann constant (simplified units)
dt = 0.01  # Time step

# Initialize simulation state
if 'positions' not in st.session_state:
    st.session_state.positions = np.random.uniform(0, L, N)
    st.session_state.velocities = np.random.normal(0, v0, N)
    st.session_state.total_momentum_transfer = 0.0
    st.session_state.total_time = 0.0

# Start button
if st.button("Start Simulation"):
    positions = st.session_state.positions
    velocities = st.session_state.velocities
    total_momentum_transfer = st.session_state.total_momentum_transfer
    total_time = st.session_state.total_time

    # Placeholder for dynamic updates
    placeholder = st.empty()

    # Simulation loop
    for step in range(500):  # Run for 500 steps
        # Update positions
        positions += velocities * dt

        # Handle collisions with walls
        for i in range(N):
            if positions[i] < 0:
                positions[i] = -positions[i]  # Reflect off left wall
                velocities[i] = -velocities[i]
                total_momentum_transfer += 2 * m * abs(velocities[i])
            elif positions[i] > L:
                positions[i] = 2 * L - positions[i]  # Reflect off right wall
                velocities[i] = -velocities[i]
                total_momentum_transfer += 2 * m * abs(velocities[i])

        total_time += dt

        # Calculate temperature from average kinetic energy
        # In 1D: <(1/2) m v^2> = (1/2) k T
        average_ke = (0.5 * m * np.sum(velocities**2)) / N
        T = (2 * average_ke) / k

        # Calculate force as momentum transfer per unit time
        F = total_momentum_transfer / total_time if total_time > 0 else 0
        F_theory = (N * k * T) / L  # Theoretical force from 1D ideal gas law

        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Position histogram
        ax1.hist(positions, bins=20, range=(0, L), color='blue', alpha=0.7)
        ax1.set_title("Particle Positions")
        ax1.set_xlabel("Position")
        ax1.set_ylabel("Count")
        
        # Velocity histogram
        ax2.hist(velocities, bins=20, color='red', alpha=0.7)
        ax2.set_title("Particle Velocities")
        ax2.set_xlabel("Velocity")
        ax2.set_ylabel("Count")
        
        plt.tight_layout()

        # Update placeholder with plot and metrics
        with placeholder.container():
            st.pyplot(fig)
            st.write(f"**Temperature (T):** {T:.2f} units")
            st.write(f"**Simulated Force (F):** {F:.2f} units")
            st.write(f"**Theoretical Force (F_theory):** {F_theory:.2f} units")

        # Small delay for visualization
        time.sleep(0.05)

    # Update session state
    st.session_state.positions = positions
    st.session_state.velocities = velocities
    st.session_state.total_momentum_transfer = total_momentum_transfer
    st.session_state.total_time = total_time

# Instructions
st.write("""
### How to Use
1. Adjust the parameters in the sidebar:
   - **Number of particles (N)**: Total particles in the simulation.
   - **Box length (L)**: Length of the 1D box.
   - **Initial velocity scale (v0)**: Controls the spread of initial velocities.
2. Click "Start Simulation" to run the simulation for 500 steps.
3. Observe the histograms and calculated values updating in real-time.
""")