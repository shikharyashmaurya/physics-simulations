import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set up the page
st.set_page_config(page_title="Faraday's Law Visualization", layout="wide")
st.title("Visualization of Faraday's Law of Electromagnetic Induction")

# Theory section
st.markdown("""
## Faraday's Law
Faraday's Law states that the induced electromotive force (EMF) in a closed circuit is equal to:
""")
st.latex(r'''\varepsilon = -N \frac{d\Phi_B}{dt}''')
st.markdown("""
Where:
- ε = Induced EMF (Volts)
- N = Number of turns in coil
- Φ_B = Magnetic flux (Weber)
- t = Time (seconds)

Magnetic flux is given by:
""")
st.latex(r'''\Phi_B = B \cdot A \cdot \cos(\theta)''')

# Sidebar controls
st.sidebar.header("Simulation Parameters")
B0 = st.sidebar.slider("Peak Magnetic Field (T)", 0.1, 10.0, 2.0)
N = st.sidebar.slider("Number of Turns", 1, 100, 50)
radius = st.sidebar.slider("Coil Radius (m)", 0.1, 2.0, 0.5)
theta_deg = st.sidebar.slider("Angle between B and Normal (degrees)", 0, 180, 45)
freq = st.sidebar.slider("Oscillation Frequency (Hz)", 0.1, 10.0, 1.0)

# Convert angle to radians
theta = np.deg2rad(theta_deg)

# Time array
t = np.linspace(0, 2, 1000)  # 2 seconds simulation

# Calculations
B = B0 * np.sin(2 * np.pi * freq * t)  # Time-varying magnetic field
A = np.pi * radius**2  # Coil area
flux = N * B * A * np.cos(theta)  # Magnetic flux
emf = -np.gradient(flux, t)  # Induced EMF

# Create figure for plots
fig = plt.figure(figsize=(12, 10))

# Magnetic field plot
ax1 = plt.subplot(311)
ax1.plot(t, B, color='tab:red')
ax1.set_ylabel('Magnetic Field (T)')
ax1.set_title('Time-varying Magnetic Field')
ax1.grid(True)

# Magnetic flux plot
ax2 = plt.subplot(312)
ax2.plot(t, flux, color='tab:green')
ax2.set_ylabel('Magnetic Flux (Wb)')
ax2.set_title('Magnetic Flux Through Coil')
ax2.grid(True)

# Induced EMF plot
ax3 = plt.subplot(313)
ax3.plot(t, emf, color='tab:blue')
ax3.set_ylabel('Induced EMF (V)')
ax3.set_xlabel('Time (s)')
ax3.set_title('Induced Electromotive Force')
ax3.grid(True)

plt.tight_layout()
st.pyplot(fig)

# 3D Visualization
st.markdown("### 3D Visualization of Coil Orientation")

fig3d = plt.figure(figsize=(8, 8))
ax3d = fig3d.add_subplot(111, projection='3d')

# Generate coil coordinates
theta_coil = np.linspace(0, 2*np.pi, 100)
x = radius * np.cos(theta_coil)
y = radius * np.sin(theta_coil) * np.cos(theta)
z = radius * np.sin(theta_coil) * np.sin(theta)

# Plot coil
ax3d.plot(x, y, z, color='blue', linewidth=2, label='Coil')

# Plot magnetic field direction
ax3d.quiver(0, 0, -1, 0, 0, 2, color='red', 
           linewidth=3, arrow_length_ratio=0.1, label='Magnetic Field (B)')

# Set plot limits and labels
ax3d.set_xlim([-radius*1.5, radius*1.5])
ax3d.set_ylim([-radius*1.5, radius*1.5])
ax3d.set_zlim([-radius*1.5, radius*1.5])
ax3d.set_xlabel('X-axis')
ax3d.set_ylabel('Y-axis')
ax3d.set_zlabel('Z-axis')
ax3d.set_title('Coil Orientation Relative to Magnetic Field')
ax3d.legend()

st.pyplot(fig3d)

# Explanation
st.markdown("""
## Explanation
1. **Magnetic Field (Red Plot):** Shows the sinusoidal variation of the external magnetic field
2. **Magnetic Flux (Green Plot):** Demonstrates the flux through the coil depending on angle θ
3. **Induced EMF (Blue Plot):** Shows the EMF generated by the changing magnetic flux

The 3D visualization shows:
- Blue coil in its orientation relative to the magnetic field (red arrow)
- The angle θ between the coil's normal vector and magnetic field direction
""")