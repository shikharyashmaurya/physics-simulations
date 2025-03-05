import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Work-Energy Theorem Simulation")
st.markdown("""
This simulation demonstrates the **Work-Energy Theorem**, which states that the net work done on an object equals its change in kinetic energy:  
**\( W_{\text{net}} = \Delta K \)**.  
Adjust the parameters below to explore how an applied force (with optional friction) affects a block's motion and energy.
""")

# Input fields
st.subheader("Input Parameters")
m = st.number_input("Mass of the block (kg)", min_value=0.1, value=1.0, step=0.1)
F = st.number_input("Applied force (N)", min_value=0.0, value=10.0, step=1.0)
mu_k = st.number_input("Coefficient of kinetic friction (μ_k)", min_value=0.0, value=0.0, step=0.05)
T = st.number_input("Total time (s)", min_value=0.1, value=5.0, step=0.1)

# Constants
g = 9.8  # Acceleration due to gravity (m/s²)

# Calculate kinetic friction force
f_k = mu_k * m * g

# Determine net force
if F > f_k:
    F_net = F - f_k
    st.write(f"Net force: {F_net:.2f} N")
else:
    F_net = 0
    st.warning("The applied force is not sufficient to overcome friction, so the block does not move.")

# Calculate acceleration
a = F_net / m if F_net > 0 else 0

# Time array for simulation
t = np.linspace(0, T, 100)

# Calculate motion and energy
if F_net > 0:
    x = 0.5 * a * t**2  # Position: x(t) = (1/2) a t² (starting from rest)
    v = a * t           # Velocity: v(t) = a t
else:
    x = np.zeros_like(t)
    v = np.zeros_like(t)

K = 0.5 * m * v**2      # Kinetic energy: K(t) = (1/2) m v²
W_net = F_net * x       # Net work done: W_net(t) = F_net * x(t)

# Plotting
st.subheader("Visualizations")
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), height_ratios=[1, 1])
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 1]})

# Plot 1: Position vs. Time
ax1.plot(t, x, label="Position", color="blue")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Position (m)")
ax1.set_title("Position of the Block Over Time")
ax1.grid(True)
ax1.legend()

# Plot 2: Net Work and Kinetic Energy vs. Time
ax2.plot(t, W_net, label="Net Work Done", color="green")
ax2.plot(t, K, label="Kinetic Energy", color="orange", linestyle="--")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Energy (J)")
ax2.set_title("Net Work Done vs. Kinetic Energy")
ax2.grid(True)
ax2.legend()

# Adjust layout and display plot
plt.tight_layout()
st.pyplot(fig)

# Display final values
st.subheader(f"Results at t = {T} s")
if F_net > 0:
    st.write(f"Final position: {x[-1]:.2f} m")
    st.write(f"Final velocity: {v[-1]:.2f} m/s")
    st.write(f"Net work done: {W_net[-1]:.2f} J")
    st.write(f"Change in kinetic energy: {K[-1] - K[0]:.2f} J")
    st.success("Notice that the net work done equals the change in kinetic energy, confirming the Work-Energy Theorem!")
else:
    st.write("Since the block does not move:")
    st.write("Net work done: 0.00 J")
    st.write("Change in kinetic energy: 0.00 J")