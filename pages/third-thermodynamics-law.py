import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Visualization of the Third Law of Thermodynamics")
st.write("""
This simulation demonstrates the third law of thermodynamics using a simple model of a crystalline lattice.
As temperature approaches absolute zero, the atoms vibrate less, leading to a perfectly ordered state (minimal entropy).
""")

# Temperature slider (in Kelvin)
T = st.slider("Select Temperature (K)", 0.0, 300.0, 150.0, step=1.0)

# Define lattice dimensions (a simple 10x10 grid)
num_points = 10
x_coords, y_coords = np.meshgrid(np.linspace(0, 10, num_points), np.linspace(0, 10, num_points))
x_coords = x_coords.flatten()
y_coords = y_coords.flatten()

# Determine noise amplitude based on temperature.
# At T=300K the maximum displacement is set to 0.5 units, and at T=0 there is no displacement.
noise_amp = (T / 300) * 0.5

# Add random displacement to simulate thermal vibrations
x_noise = np.random.normal(0, noise_amp, size=x_coords.shape)
y_noise = np.random.normal(0, noise_amp, size=y_coords.shape)

# Compute the current positions of the atoms
x_positions = x_coords + x_noise
y_positions = y_coords + y_noise

# Plot the lattice with the displaced atomic positions
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(x_positions, y_positions, color="blue")
ax.set_title(f"Atomic positions at T = {T:.1f} K")
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 11)
ax.set_aspect("equal")

st.pyplot(fig)

st.write("""
As you lower the temperature using the slider, notice that the atoms’ positions become less scattered.
At T = 0 K, the atoms remain fixed in place (no thermal agitation), illustrating the third law: a perfect crystal 
has zero entropy at absolute zero.
""")
