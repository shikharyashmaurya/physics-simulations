import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set up the Streamlit page
st.title("Pressure Visualization Simulation")
st.markdown("""
This simulation visualizes how pressure increases with depth in a fluid using the formula:

**P = P0 + ρ g h**

- **P0**: Atmospheric pressure (Pa)
- **ρ**: Fluid density (kg/m³)
- **g**: Gravitational acceleration (m/s²)
- **h**: Depth (m)
""")

# User inputs via interactive sliders
P0 = st.slider("Atmospheric Pressure (P0 in Pa)", min_value=50000, max_value=150000, value=101325, step=100)
density = st.slider("Fluid Density (ρ in kg/m³)", min_value=500, max_value=2000, value=1000, step=50)
g = st.slider("Gravitational Acceleration (g in m/s²)", min_value=1.0, max_value=20.0, value=9.81, step=0.1)
max_depth = st.slider("Maximum Depth (m)", min_value=1, max_value=100, value=10, step=1)
depth_marker = st.slider("Select Depth Marker (m)", min_value=0, max_value=max_depth, value=max_depth // 2, step=1)

# Compute the pressure distribution along the depth
depth = np.linspace(0, max_depth, num=100)
pressure = P0 + density * g * depth

# Create a plot of pressure vs. depth
fig, ax = plt.subplots()
ax.plot(depth, pressure, label="Pressure (Pa)")
ax.set_xlabel("Depth (m)")
ax.set_ylabel("Pressure (Pa)")
ax.set_title("Pressure vs. Depth")
ax.grid(True)

# Mark the pressure at the selected depth marker
selected_pressure = P0 + density * g * depth_marker
ax.plot(depth_marker, selected_pressure, 'ro', markersize=8,
        label=f"At {depth_marker} m: {selected_pressure:.2f} Pa")
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("""
The graph above shows that pressure increases linearly with depth in a fluid. Use the sliders above to adjust the parameters and explore how they affect the pressure distribution.
""")
