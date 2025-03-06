import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Scaling Laws and Similarity Visualization")
st.markdown(
    """
This simulation demonstrates how geometric properties scale with size.
Select a shape, adjust the baseline dimension, and change the scale factor to see how the surface area and volume change.
"""
)

# Choose the shape for the simulation.
shape = st.selectbox("Select a shape", ["Cube", "Sphere"])

# Select the scale factor and baseline dimension.
scale_factor = st.slider("Scale Factor", min_value=0.1, max_value=5.0, step=0.1, value=1.0)
baseline = st.slider("Baseline Dimension", min_value=0.1, max_value=10.0, step=0.1, value=1.0)

# Compute properties based on selected shape.
if shape == "Cube":
    # For a cube, side length L = baseline * scale_factor.
    L = baseline * scale_factor
    area = 6 * L**2
    volume = L**3
    
    st.write(f"**Side Length:** {L:.2f}")
    st.write(f"**Surface Area:** {area:.2f}")
    st.write(f"**Volume:** {volume:.2f}")
    
    # Prepare data for scaling plot.
    scale_vals = np.linspace(0.1, 5, 100)
    side_vals = baseline * scale_vals
    area_vals = 6 * side_vals**2
    volume_vals = side_vals**3

elif shape == "Sphere":
    # For a sphere, radius R = baseline * scale_factor.
    R = baseline * scale_factor
    area = 4 * np.pi * R**2
    volume = (4/3) * np.pi * R**3
    
    st.write(f"**Radius:** {R:.2f}")
    st.write(f"**Surface Area:** {area:.2f}")
    st.write(f"**Volume:** {volume:.2f}")
    
    # Prepare data for scaling plot.
    scale_vals = np.linspace(0.1, 5, 100)
    radius_vals = baseline * scale_vals
    area_vals = 4 * np.pi * radius_vals**2
    volume_vals = (4/3) * np.pi * radius_vals**3

# Create log-log plots to visualize the power-law relationships.
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].loglog(scale_vals, area_vals, label="Area", lw=2)
ax[0].set_title("Area vs Scale Factor (log–log)")
ax[0].set_xlabel("Scale Factor")
ax[0].set_ylabel("Area")
ax[0].legend()

ax[1].loglog(scale_vals, volume_vals, label="Volume", color="red", lw=2)
ax[1].set_title("Volume vs Scale Factor (log–log)")
ax[1].set_xlabel("Scale Factor")
ax[1].set_ylabel("Volume")
ax[1].legend()

st.pyplot(fig)

st.markdown(
    """
The plots above illustrate that the surface area scales as the square of the length (slope of 2 on a log–log plot) and the volume scales as the cube of the length (slope of 3).
Adjust the sliders to see how these scaling laws manifest for different baseline dimensions and scale factors.
"""
)
