import streamlit as st
import matplotlib.pyplot as plt
from simulations.pendulum import simulate_pendulum  # Import simulation logic (create this module)

# Page setup
st.title("Pendulum Simulation")
st.write("This simulation models a simple pendulum using the small-angle approximation. Adjust the parameters below to see how they affect the motion.")

# Input widgets
length = st.slider("Pendulum Length (m)", 0.1, 2.0, 1.0)
gravity = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.8)
initial_angle = st.slider("Initial Angle (degrees)", 0, 90, 10)
time_span = st.slider("Time Span (s)", 1, 10, 5)

# Run simulation on button click
if st.button("Run Simulation"):
    if length <= 0:
        st.error("Length must be positive.")
    else:
        try:
            # Convert angle to radians and run simulation
            t, angle = simulate_pendulum(length, gravity, initial_angle * (3.1416 / 180), time_span)
            
            # Create and display plot
            fig, ax = plt.subplots()
            ax.plot(t, angle)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Angle (radians)")
            ax.grid(True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")