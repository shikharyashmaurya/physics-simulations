import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set the title and description for the simulation
st.title("Ideal Gas Law Visualization")
st.write("""
This simulation visualizes the relationship between pressure, volume, and temperature of an ideal gas using the equation:
\[ P = \frac{nRT}{V} \]
Adjust the parameters in the sidebar to see how the pressure changes.
""")

# Constants
R = 8.314  # Ideal gas constant in J/(mol*K)

# Sidebar for user inputs
st.sidebar.header("Gas Parameters")
n = st.sidebar.slider("Number of moles (n)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
T = st.sidebar.slider("Temperature (T in Kelvin)", min_value=100, max_value=1000, value=300, step=50)
V = st.sidebar.slider("Volume (V in cubic meters)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Calculate pressure using the ideal gas law
P = n * R * T / V
st.write(f"### Computed Pressure:")
st.write(f"The pressure of the gas is **{P:.2f} Pascals**.")

# Create a range of volumes to plot the Pressure vs Volume curve
volumes = np.linspace(0.1, 10, 200)
pressures = n * R * T / volumes

# Plotting the curve
fig, ax = plt.subplots()
ax.plot(volumes, pressures, color='b', label=f"T = {T} K, n = {n} mol")
ax.set_xlabel("Volume (m³)")
ax.set_ylabel("Pressure (Pascals)")
ax.set_title("Pressure vs Volume")
ax.legend()
ax.grid(True)

st.pyplot(fig)
