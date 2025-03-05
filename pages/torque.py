import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title and description
st.title("Torque Visualization")
st.write("""
This simulation demonstrates torque, the rotational equivalent of force. Torque (τ) is calculated as τ = r × F, 
where r is the distance from the pivot to the force application point, and F is the force magnitude. 
The direction of the force determines whether the torque causes clockwise or counterclockwise rotation.
""")

# Define constants
L = 1.0  # Length of the bar in meters

# User inputs
r = st.slider("Distance from pivot (m)", 0.0, L, 0.5, help="Distance from the pivot where the force is applied.")
F = st.slider("Force magnitude (N)", 0.0, 100.0, 50.0, help="Magnitude of the applied force in Newtons.")
direction = st.selectbox("Force direction", ["downward", "upward"], help="Direction of the force relative to the bar.")
show_rotation = st.checkbox("Show rotation effect", help="Toggle to see the bar rotated based on the torque.")

# Calculate torque (assuming force is perpendicular, so sin(θ) = 1)
if direction == "downward":
    tau = -r * F  # Negative torque indicates clockwise rotation
    force_dir = -1
else:
    tau = r * F   # Positive torque indicates counterclockwise rotation
    force_dir = 1

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))

# Plot the bar based on rotation option
if show_rotation:
    k = 0.005  # Scaling factor for rotation angle (radians per Nm)
    theta = k * tau  # Rotation angle in radians
    x_end = L * np.cos(theta)
    y_end = L * np.sin(theta)
    ax.plot([0, x_end], [0, y_end], 'b-', linewidth=5, label="Bar (rotated)")
else:
    ax.plot([0, L], [0, 0], 'b-', linewidth=5, label="Bar")

# Plot the pivot point
ax.plot(0, 0, 'ro', markersize=10, label="Pivot")

# Plot the force arrow (only if not showing rotation, to keep it clear)
if not show_rotation:
    arrow_length = 0.1
    ax.arrow(r, 0, 0, force_dir * arrow_length, head_width=0.05, head_length=0.05, fc='g', ec='g', label="Force")

# Add torque annotation
torque_text = f"Torque: {abs(tau):.2f} Nm ({'clockwise' if tau < 0 else 'counterclockwise'})"
ax.text(0.1, 0.15 if not show_rotation else -0.15, torque_text, fontsize=10)

# Customize the plot
ax.set_xlim(-0.1, L + 0.1)
ax.set_ylim(-0.2, 0.2)
ax.set_aspect('equal')
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

# Explanatory text
st.write("""
- **Blue line**: The bar, pivoted at the red dot.
- **Green arrow**: The applied force (visible when 'Show rotation effect' is unchecked).
- **Torque**: Calculated as τ = r × F. Positive τ means counterclockwise rotation; negative τ means clockwise.
- **Rotation effect**: When checked, the bar rotates by an angle proportional to the torque (θ = k × τ, where k = 0.005 rad/Nm).
""")