import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Refraction Simulation")
st.markdown("""
This simulation visualizes the refraction of light as it passes from one medium to another.
Adjust the indices of refraction (n1 and n2) and the angle of incidence to see how the light ray bends.
- **Red arrow**: Incident ray
- **Blue arrow**: Refracted ray (if refraction occurs)
- **Green arrow**: Reflected ray (if total internal reflection occurs)
""")

# Input sliders
n1 = st.slider("Index of refraction of first medium (n1)", min_value=1.0, max_value=2.0, value=1.0, step=0.01)
n2 = st.slider("Index of refraction of second medium (n2)", min_value=1.0, max_value=2.0, value=1.5, step=0.01)
theta1_deg = st.slider("Angle of incidence (degrees)", min_value=0, max_value=90, value=30, step=1)

# Convert angle to radians
theta1 = np.deg2rad(theta1_deg)

# Check for total internal reflection and calculate theta2
if n1 > n2 and np.sin(theta1) > n2 / n1:
    total_internal_reflection = True
    theta2_deg = None
else:
    total_internal_reflection = False
    sin_theta2 = (n1 / n2) * np.sin(theta1)
    theta2 = np.arcsin(sin_theta2)
    theta2_deg = np.rad2deg(theta2)

# Create plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')  # Ensure angles are visually accurate

# Draw interface between media
ax.axhline(0, color='gray', linewidth=2, label='Interface')

# Fill media with colors
ax.fill_between([-10, 10], 0, 10, color='lightblue', alpha=0.3, label=f'Medium 1 (n1 = {n1:.2f})')
ax.fill_between([-10, 10], -10, 0, color='lightgreen', alpha=0.3, label=f'Medium 2 (n2 = {n2:.2f})')

# Draw normal line
ax.axvline(0, color='gray', linestyle='--', label='Normal')

# Incident ray (from top-left to origin)
start_x = -5 * np.sin(theta1)
start_y = 5 * np.cos(theta1)
dx_inc = -start_x  # Direction to (0,0)
dy_inc = -start_y
ax.arrow(start_x, start_y, dx_inc, dy_inc, head_width=0.5, head_length=0.5, fc='r', ec='r', length_includes_head=True, label='Incident ray')

# Refracted or reflected ray
if not total_internal_reflection:
    # Refracted ray (from origin downward)
    dx_ref = 5 * np.sin(theta2)
    dy_ref = -5 * np.cos(theta2)
    ax.arrow(0, 0, dx_ref, dy_ref, head_width=0.5, head_length=0.5, fc='b', ec='b', length_includes_head=True, label='Refracted ray')
else:
    # Reflected ray (from origin upward)
    dx_ref = 5 * np.sin(theta1)
    dy_ref = 5 * np.cos(theta1)
    ax.arrow(0, 0, dx_ref, dy_ref, head_width=0.5, head_length=0.5, fc='g', ec='g', length_includes_head=True, label='Reflected ray')

# Add labels for media
ax.text(-9, 5, f'Medium 1\nn1 = {n1:.2f}', fontsize=10, verticalalignment='center')
ax.text(-9, -5, f'Medium 2\nn2 = {n2:.2f}', fontsize=10, verticalalignment='center')

# Add legend
ax.legend(loc='upper right')

# Display plot
st.pyplot(fig)

# Display results
if total_internal_reflection:
    st.write("Total Internal Reflection occurs. No refraction.")
else:
    st.write(f"Angle of refraction: {theta2_deg:.2f} degrees")