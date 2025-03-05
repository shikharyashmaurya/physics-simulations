import streamlit as st
import matplotlib.pyplot as plt
from simulations.projectile import simulate_projectile  # Import simulation logic (create this module)

# Page setup
st.title("Projectile Motion Simulation")
st.write("Simulate the trajectory of a projectile launched with given initial conditions.")

# Input widgets
initial_velocity = st.slider("Initial Velocity (m/s)", 0.0, 100.0, 50.0)
launch_angle = st.slider("Launch Angle (degrees)", 0, 90, 45)
air_resistance = st.checkbox("Include Air Resistance")

# Run simulation
if st.button("Run Simulation"):
    try:
        t, x, y = simulate_projectile(initial_velocity, launch_angle, air_resistance)
        
        # Create and display plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Height (m)")
        ax.grid(True)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")