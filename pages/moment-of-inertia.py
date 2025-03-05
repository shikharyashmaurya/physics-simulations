import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title and Introduction
st.title("Moment of Inertia Simulation")
st.markdown("### What is Moment of Inertia?")
st.write("Moment of Inertia (I) measures an object's resistance to rotational motion. It depends on the mass and its distribution relative to the axis of rotation. In this simulation, adjust the masses, their positions, and the axis to see how I changes.")

# Sidebar for Number of Masses
st.sidebar.title("Settings")
num_masses = st.sidebar.slider("Number of masses", 1, 5, 1)

# Input Sliders for Masses and Positions
masses = []
positions = []
for i in range(num_masses):
    st.subheader(f"Mass {i+1}")
    col1, col2 = st.columns(2)
    with col1:
        m = st.slider(f"Mass (kg)", 0.1, 10.0, 1.0, key=f"m{i}")
    with col2:
        r = st.slider(f"Position (m)", 0.0, 1.0, 0.5, key=f"r{i}")
    masses.append(m)
    positions.append(r)

# Axis of Rotation Slider
axis_pos = st.slider("Axis of rotation position (m)", 0.0, 1.0, 0.0)

# Calculations
total_mass = sum(masses)
x_cm = sum(m * r for m, r in zip(masses, positions)) / total_mass if total_mass > 0 else 0
I = sum(m * (r - axis_pos)**2 for m, r in zip(masses, positions))

# Display Formula and Results
st.write("The Moment of Inertia is calculated as:")
st.latex(r"I = \sum_{i} m_i (r_i - a)^2")
st.write(f"where *a* is the axis position: {axis_pos} m")
st.write("**Calculation details:**")
for i, (m, r) in enumerate(zip(masses, positions)):
    contribution = m * (r - axis_pos)**2
    st.write(f"Mass {i+1}: {m} kg at {r} m, distance to axis: {abs(r - axis_pos):.2f} m, contribution: {contribution:.2f} kg m²")
st.write(f"**Total Moment of Inertia: {I:.2f} kg m²**")

# Plot Rod with Masses
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 0], 'k-', linewidth=2, label="Rod")
for r in positions:
    ax.plot(r, 0, 'ro', markersize=10)  # Masses as red circles
ax.axvline(x=axis_pos, color='b', linestyle='--', label="Axis of Rotation")
ax.plot(x_cm, 0, 'g*', markersize=15, label="Center of Mass")
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 0.1)
ax.set_xlabel("Position (m)")
ax.set_title("Rod with Masses")
ax.legend()
st.pyplot(fig)

# Plot I vs. Axis Position
st.subheader("Moment of Inertia vs. Axis Position")
axis_positions = np.linspace(0, 1, 100)
I_values = [sum(m * (r - a)**2 for m, r in zip(masses, positions)) for a in axis_positions]
fig2, ax2 = plt.subplots()
ax2.plot(axis_positions, I_values, label="I vs. Axis Position")
ax2.axvline(x=x_cm, color='g', linestyle='--', label="Center of Mass")
ax2.set_xlabel("Axis Position (m)")
ax2.set_ylabel("Moment of Inertia (kg m²)")
ax2.legend()
st.pyplot(fig2)

# Torque and Angular Acceleration
st.subheader("Apply Torque")
torque = st.number_input("Torque (N m)", 0.0, 100.0, 1.0)
if I > 0:
    alpha = torque / I
    st.write(f"Angular acceleration: {alpha:.2f} rad/s²")
else:
    st.write("Moment of Inertia is zero, cannot calculate angular acceleration.")