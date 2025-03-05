import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Set up the Streamlit app
st.title("Rotational Motion Simulation")

# User inputs via sliders
omega0 = st.slider("Initial angular velocity (rad/s)", 0.0, 10.0, 1.0)
alpha = st.slider("Angular acceleration (rad/s²)", -5.0, 5.0, 0.5)
T = st.slider("Total time (s)", 0.0, 10.0, 5.0)

# Create the figure and axis for plotting
fig, ax = plt.subplots()
ax.set_aspect('equal')  # Ensure the disk appears circular
ax.set_xlim(-1.5, 1.5)  # Set x-axis limits
ax.set_ylim(-1.5, 1.5)  # Set y-axis limits
ax.set_xticks([])       # Remove x-axis ticks
ax.set_yticks([])       # Remove y-axis ticks
ax.set_title("Rotating Disk")

# Plot the disk as a circle
theta_circle = np.linspace(0, 2 * np.pi, 100)
x_circle = np.cos(theta_circle)
y_circle = np.sin(theta_circle)
ax.plot(x_circle, y_circle, 'b-', label="Disk")

# Plot the initial orientation line (radius)
line, = ax.plot([0, 1], [0, 0], 'r-', linewidth=2, label="Orientation")

# Add a legend (optional, can be removed for simplicity)
ax.legend()

# Button to start the simulation
if st.button("Run Simulation"):
    # Create placeholders for the figure and text
    placeholder_fig = st.empty()
    placeholder_text = st.empty()

    # Simulation loop
    for t in np.arange(0, T, 0.1):
        # Calculate angular displacement and velocity
        theta = omega0 * t + 0.5 * alpha * t**2
        omega = omega0 + alpha * t

        # Update the line position
        x = np.cos(theta)
        y = np.sin(theta)
        line.set_data([0, x], [0, y])

        # Update the figure in the placeholder
        placeholder_fig.pyplot(fig)

        # Update the text with current values
        placeholder_text.write(
            f"Time: {t:.2f} s, Angle: {theta:.2f} rad, Angular velocity: {omega:.2f} rad/s"
        )

        # Pause briefly to create animation effect
        time.sleep(0.1)
else:
    st.write("Click the button to run the simulation.")