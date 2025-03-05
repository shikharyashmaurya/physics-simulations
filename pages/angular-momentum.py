import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title of the app
st.title("Angular Momentum Visualization")

# Let the user choose the type of motion
motion_type = st.selectbox("Select Motion Type", ["Linear Motion", "Circular Motion"])

# Scenario 1: Linear Motion
if motion_type == "Linear Motion":
    st.subheader("Linear Motion")
    st.write("A particle moves in a straight line. Adjust the initial position and velocity to see how Angular Momentum behaves.")

    # Input sliders for initial position and velocity
    x0 = st.slider("Initial x-position (x₀)", -5.0, 5.0, 0.0)
    y0 = st.slider("Initial y-position (y₀)", -5.0, 5.0, 0.0)
    v_x = st.slider("Velocity x-component (vₓ)", -2.0, 2.0, 1.0)
    v_y = st.slider("Velocity y-component (vᵧ)", -2.0, 2.0, 0.0)
    t = st.slider("Time (t)", 0.0, 10.0, 0.0)
    m = 1.0  # Mass set to 1 for simplicity

    # Calculate position at time t
    x = x0 + v_x * t
    y = y0 + v_y * t

    # Calculate Angular Momentum (z-component)
    L_z = m * (x * v_y - y * v_x)

    # Create the plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  # Equal scaling for x and y axes
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True)

    # Plot the origin
    ax.plot(0, 0, 'ko', label='Origin')

    # Plot the particle's path (straight line)
    if v_x != 0 or v_y != 0:
        # Define the line extending beyond plot limits
        s = 100
        x1 = x0 + v_x * (-s)
        y1 = y0 + v_y * (-s)
        x2 = x0 + v_x * s
        y2 = y0 + v_y * s
        ax.plot([x1, x2], [y1, y2], 'g--', label='Path')

    # Plot position vector (blue)
    ax.arrow(0, 0, x, y, head_width=0.5, head_length=0.5, fc='blue', ec='blue', label='Position Vector')
    # Plot velocity vector (red)
    ax.arrow(x, y, v_x, v_y, head_width=0.5, head_length=0.5, fc='red', ec='red', label='Velocity Vector')
    # Plot particle position
    ax.plot(x, y, 'ro', label='Particle')

    # Display Angular Momentum
    ax.text(-9, 9, f'L_z = {L_z:.2f}', fontsize=12)

    # Add legend
    ax.legend(loc='upper right')
    st.pyplot(fig)

# Scenario 2: Circular Motion
elif motion_type == "Circular Motion":
    st.subheader("Circular Motion")
    st.write("A particle moves in a circle around the origin. Adjust the radius and angular velocity to observe Angular Momentum.")

    # Input sliders for radius and angular velocity
    r = st.slider("Radius (r)", 0.5, 5.0, 2.0)
    omega = st.slider("Angular Velocity (ω)", 0.1, 2.0, 1.0)
    t = st.slider("Time (t)", 0.0, 10.0, 0.0)
    m = 1.0  # Mass set to 1

    # Calculate position and velocity using circular motion equations
    theta = omega * t
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    v_x = -r * omega * np.sin(theta)
    v_y = r * omega * np.cos(theta)

    # Calculate Angular Momentum (z-component)
    L_z = m * (x * v_y - y * v_x)

    # Create the plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True)

    # Plot the origin
    ax.plot(0, 0, 'ko', label='Origin')

    # Plot the circular path
    theta_vals = np.linspace(0, 2 * np.pi, 100)
    x_path = r * np.cos(theta_vals)
    y_path = r * np.sin(theta_vals)
    ax.plot(x_path, y_path, 'g--', label='Path')

    # Plot position vector (blue)
    ax.arrow(0, 0, x, y, head_width=0.5, head_length=0.5, fc='blue', ec='blue', label='Position Vector')
    # Plot velocity vector (red)
    ax.arrow(x, y, v_x, v_y, head_width=0.5, head_length=0.5, fc='red', ec='red', label='Velocity Vector')
    # Plot particle position
    ax.plot(x, y, 'ro', label='Particle')

    # Display Angular Momentum
    ax.text(-9, 9, f'L_z = {L_z:.2f}', fontsize=12)

    # Add legend
    ax.legend(loc='upper right')
    st.pyplot(fig)