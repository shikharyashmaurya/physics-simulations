import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc

# Streamlit app title and description
st.title("Reflection Simulation")
st.write("Adjust the angle of incidence to see how the reflected ray changes according to the law of reflection.")

# Slider for angle of incidence (in degrees)
θ = st.slider("Angle of incidence (degrees)", 0, 89, 45)

# Calculate angles in degrees for incident and reflected rays
# Normal is at 90° (vertical), incident ray comes from the left side
φ_incident = 90 + θ      # Angle of incident ray from positive x-axis
φ_reflected = 90 - θ     # Angle of reflected ray from positive x-axis

# Create Matplotlib figure
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_aspect('equal')  # Ensure angles look correct
ax.set_xlim(-10, 10)
ax.set_ylim(-1, 10)     # Mirror at y=0, rays above

# Draw the mirror (horizontal line)
ax.plot([-10, 10], [0, 0], 'k-', linewidth=2, label='Mirror')

# Draw the normal (vertical dashed line)
ax.plot([0, 0], [0, 5], 'k--', linewidth=1, label='Normal')

# Length of rays for visualization
r = 10

# Calculate endpoint coordinates for incident and reflected rays
x_inc = r * np.cos(np.radians(φ_incident))
y_inc = r * np.sin(np.radians(φ_incident))
x_ref = r * np.cos(np.radians(φ_reflected))
y_ref = r * np.sin(np.radians(φ_reflected))

# Draw incident ray (from endpoint to origin)
ax.arrow(x_inc, y_inc, -x_inc, -y_inc, head_width=0.5, head_length=0.5, fc='blue', ec='blue', label='Incident Ray')

# Draw reflected ray (from origin to endpoint)
ax.arrow(0, 0, x_ref, y_ref, head_width=0.5, head_length=0.5, fc='red', ec='red', label='Reflected Ray')

# Label the rays
ax.text(x_inc/2, y_inc/2, 'Incident Ray', color='blue', fontsize=10)
ax.text(x_ref/2, y_ref/2, 'Reflected Ray', color='red', fontsize=10)

# Add angle arcs and labels
# Incident angle arc (from normal at 90° to incident ray)
arc_inc = Arc((0, 0), 4, 4, theta1=90, theta2=φ_incident, edgecolor='green', linewidth=1)
ax.add_patch(arc_inc)
ax.text(2, 2, f'θ = {θ}°', color='green', fontsize=10)

# Reflected angle arc (from reflected ray to normal at 90°)
arc_ref = Arc((0, 0), 4, 4, theta1=φ_reflected, theta2=90, edgecolor='green', linewidth=1)
ax.add_patch(arc_ref)
ax.text(-3, 2, f'θ = {θ}°', color='green', fontsize=10)

# Add labels for axes
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Display the plot in Streamlit
st.pyplot(fig)