import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Viscosity Simulation: Falling Sphere in a Viscous Fluid")

st.sidebar.header("Simulation Parameters")
eta = st.sidebar.slider("Viscosity (η) [Pa·s]", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
radius = st.sidebar.slider("Ball Radius (r) [m]", min_value=0.01, max_value=0.1, value=0.05, step=0.005)
mass = st.sidebar.slider("Ball Mass (m) [kg]", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
total_time = st.sidebar.slider("Total Simulation Time [s]", min_value=5.0, max_value=30.0, value=10.0, step=1.0)

gravity = 9.81  # m/s^2
dt = 0.05       # time step (s)

def simulate(m, r, eta, g, dt, T):
    """
    Simulate the fall of a sphere in a viscous fluid using Euler's method.
    The drag force is given by F_drag = 6*pi*eta*r*v.
    """
    num_steps = int(T / dt)
    t_vals = np.linspace(0, T, num_steps)
    v = 0.0
    x = 0.0
    positions = []
    velocities = []
    drag_coeff = 6 * np.pi * eta * r  # constant from Stokes' drag
    
    for _ in t_vals:
        # Compute acceleration from gravity and drag force:
        a = g - (drag_coeff / m) * v
        v = v + a * dt
        x = x + v * dt
        positions.append(x)
        velocities.append(v)
    return t_vals, positions, velocities

simulate_button = st.button("Run Simulation")

if simulate_button:
    t_vals, positions, velocities = simulate(mass, radius, eta, gravity, dt, total_time)
    
    # Plot position and velocity vs. time
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    
    ax1.plot(t_vals, positions, label="Position (m)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position (m)")
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(t_vals, velocities, label="Velocity (m/s)", color="orange")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (m/s)")
    ax2.legend()
    ax2.grid(True)
    
    st.pyplot(fig)
    
    # Animation of the falling ball
    st.subheader("Ball Animation")
    placeholder = st.empty()
    # Determine the plot limits based on the simulation
    max_height = max(positions) * 1.1 if positions else 10
    for i in range(len(t_vals)):
        fig_anim, ax_anim = plt.subplots(figsize=(3, 6))
        ax_anim.set_xlim(-1, 1)
        ax_anim.set_ylim(0, max_height)
        ax_anim.set_xticks([])
        ax_anim.set_ylabel("Height (m)")
        # Draw the ball as a circle
        ball = plt.Circle((0, positions[i]), radius*20, color="blue", alpha=0.7)
        ax_anim.add_artist(ball)
        ax_anim.set_title(f"Time: {t_vals[i]:.2f} s")
        placeholder.pyplot(fig_anim)
        plt.close(fig_anim)
        time.sleep(0.05)
