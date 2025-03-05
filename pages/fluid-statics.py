import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Fluid Statics Simulation")
st.markdown("""
This simulation visualizes how pressure varies in a fluid column at rest. 
According to fluid statics, the pressure increases with depth according to:
\[ P = P_0 + \rho g h \]
where:
- \(P_0\) is the surface pressure,
- \(\rho\) is the fluid density,
- \(g\) is the gravitational acceleration,
- \(h\) is the depth.
""")

# User input for simulation parameters
density = st.slider("Fluid Density (kg/m³)", min_value=500, max_value=2000, value=1000, step=50)
gravity = st.slider("Gravitational Acceleration (m/s²)", min_value=1.0, max_value=20.0, value=9.81, step=0.1)
column_height = st.slider("Fluid Column Height (m)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
P0 = st.slider("Surface Pressure (Pa)", min_value=0, max_value=200000, value=101325, step=1000)

# Calculate pressures at various depths
depths = np.linspace(0, column_height, 200)
pressures = P0 + density * gravity * depths

# Plot Pressure vs. Depth
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(pressures, depths, color="blue")
ax.set_xlabel("Pressure (Pa)")
ax.set_ylabel("Depth (m)")
ax.set_title("Pressure Variation with Depth")
ax.invert_yaxis()  # so that the plot displays depth increasing downward
st.pyplot(fig)

# Visualize the fluid column using a color gradient
fig2, ax2 = plt.subplots(figsize=(2, 6))
# Create a vertical gradient image
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
ax2.imshow(gradient, extent=[0, 1, 0, column_height], aspect='auto', cmap='Blues')
ax2.set_title("Fluid Column (Pressure Gradient)")
ax2.set_ylabel("Depth (m)")
ax2.set_xticks([])
st.pyplot(fig2)
