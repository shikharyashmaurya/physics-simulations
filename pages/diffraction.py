import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Single-Slit Diffraction Simulation")
st.write("Adjust the parameters below to explore how the diffraction pattern changes.")

# Theory section
st.markdown("### Theory")
st.write("In single-slit diffraction, light passing through a slit of width \(a\) produces an intensity pattern on a screen at distance \(D\). The intensity as a function of position \(y\) on the screen is given by:")
st.latex(r"I(y) = I_0 \left( \frac{\sin \beta}{\beta} \right)^2")
st.write("where")
st.latex(r"\beta = \frac{\pi a y}{\lambda D}")
st.write("- \(I_0\): maximum intensity at the center (set to 1 for relative intensity)")
st.write("- \(\lambda\): wavelength of the light")
st.write("- \(a\): slit width")
st.write("- \(D\): distance from slit to screen")
st.write("- \(y\): position on the screen")
st.write("The minima (dark bands) occur at:")
st.latex(r"y = \pm \frac{m \lambda D}{a}, \quad m = 1, 2, 3, \dots")
st.write("This simulation plots \(I(y)\) vs. \(y\), showing how the pattern spreads or narrows based on your inputs.")

# Parameter sliders
lambda_nm = st.slider("Wavelength λ (nm)", 300, 800, 500, help="Wavelength of light in nanometers (visible range: 400-700 nm)")
a_um = st.slider("Slit width a (μm)", 10, 1000, 100, help="Width of the slit in micrometers")
D_m = st.slider("Distance to screen D (m)", 0.5, 5.0, 1.0, help="Distance from slit to screen in meters")

# Convert units to meters
lambda_m = lambda_nm * 1e-9  # nm to m
a_m = a_um * 1e-6           # μm to m
D_m = D_m                   # already in m

# Generate position array (y) in meters
y_m = np.linspace(-0.02, 0.02, 1000)  # -20 mm to 20 mm in meters

# Compute the diffraction parameter β and intensity I(y)
z = (a_m * y_m) / (lambda_m * D_m)
I = (np.sinc(z))**2  # np.sinc(x) = sin(πx)/(πx), and I = [sin(β)/β]^2

# Convert y to millimeters for plotting
y_mm = y_m * 1e3  # m to mm

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_mm, I, color='blue')
ax.set_xlabel("Position on Screen (mm)")
ax.set_ylabel("Relative Intensity")
ax.set_ylim(0, 1.05)  # Intensity from 0 to just above 1
ax.grid(True)
st.pyplot(fig)

# Calculate and display the position of the first minimum
y_min_m = lambda_m * D_m / a_m  # in meters
y_min_mm = y_min_m * 1e3        # in millimeters
st.write(f"First minimum at y = ± {y_min_mm:.2f} mm")