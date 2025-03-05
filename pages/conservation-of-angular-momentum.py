import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Set initial parameters
m = 1.0  # mass (kg)
r0 = 1.0  # initial radius (m)
ω0 = 1.0  # initial angular velocity (rad/s)
L = m * r0**2 * ω0  # angular momentum (kg·m²/s, constant)

# Streamlit app title and explanation
st.title("Conservation of Angular Momentum Simulation")
st.write("""
This simulation illustrates the conservation of angular momentum. Angular momentum (L) is conserved in the absence of external torque. For a point mass rotating around an axis, \( L = I \cdot \omega \), where \( I = m \cdot r^2 \) is the moment of inertia, \( m \) is the mass, \( r \) is the radius, and \( \omega \) is the angular velocity. Adjust the radius (\( r \)) using the slider below to see how \( \omega \) changes to keep \( L \) constant, similar to an ice skater spinning faster when pulling their arms in.
""")

# Slider for radius r
r = st.slider("Radius (r)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Compute moment of inertia I and angular velocity ω
I = m * r**2
ω = L / I

# Display current values
st.write(f"**Mass (m):** {m} kg")
st.write(f"**Initial radius (r₀):** {r0} m")
st.write(f"**Initial angular velocity (ω₀):** {ω0} rad/s")
st.write(f"**Angular momentum (L):** {L} kg·m²/s")
st.write(f"**Current radius (r):** {r} m")
st.write(f"**Current moment of inertia (I):** {I} kg·m²")
st.write(f"**Current angular velocity (ω):** {ω:.2f} rad/s")
st.write(f"**Current L = I · ω:** {I * ω:.2f} kg·m²/s")

# Animation setup
placeholder = st.empty()
dt = 0.1  # time step for animation (s)
num_frames = 100  # number of frames

for frame in range(num_frames):
    t = frame * dt
    θ = (ω * t) % (2 * np.pi)  # current angle, wrapped to 0-2π
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    
    # Create figure
    fig, ax = plt.subplots()
    # Plot the circular path
    circle = plt.Circle((0, 0), r, color='blue', fill=False)
    ax.add_artist(circle)
    # Plot the mass
    ax.plot(x, y, 'ro', markersize=10)
    # Plot a line from center to mass
    ax.plot([0, x], [0, y], 'r-')
    # Set axis limits and aspect
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(f"ω = {ω:.2f} rad/s")
    
    # Update the placeholder with the new figure
    placeholder.pyplot(fig)
    plt.close(fig)  # Free memory
    
    # Control animation speed
    time.sleep(0.05)