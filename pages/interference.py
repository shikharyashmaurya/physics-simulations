import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def interference_pattern(lambda_, d, grid_size=200, x_range=5):
    """
    Compute the interference pattern for two point sources.

    Parameters:
    - lambda_: Wavelength of the waves (float).
    - d: Separation distance between the two sources (float).
    - grid_size: Number of points in the grid (int, default=200).
    - x_range: Range of x and y coordinates (float, default=5).

    Returns:
    - I: 2D array of interference intensity.
    - x: 1D array of x coordinates.
    - y: 1D array of y coordinates.
    - S1: Position of the first source (list).
    - S2: Position of the second source (list).
    """
    # Create a 2D grid
    x = np.linspace(-x_range, x_range, grid_size)
    y = np.linspace(-x_range, x_range, grid_size)
    X, Y = np.meshgrid(x, y)

    # Define source positions
    S1 = [-d/2, 0]  # First source at (-d/2, 0)
    S2 = [d/2, 0]   # Second source at (d/2, 0)

    # Calculate distances from each source to every point on the grid
    r1 = np.sqrt((X - S1[0])**2 + (Y - S1[1])**2)
    r2 = np.sqrt((X - S2[0])**2 + (Y - S2[1])**2)

    # Compute path difference
    delta = r2 - r1

    # Calculate intensity (proportional to cos^2(π * Δ / λ))
    I = np.cos(np.pi * delta / lambda_)**2

    return I, x, y, S1, S2

# Streamlit app setup
st.title("Interference Pattern Simulation")

# Explanatory text
st.write("""
This simulation visualizes the interference pattern created by two point sources emitting waves.
- **Bright regions**: Constructive interference, where waves reinforce each other.
- **Dark regions**: Destructive interference, where waves cancel out.
Use the sliders below to adjust the **wavelength (λ)** and **source separation (d)** to see how the pattern changes.
""")

# Interactive sliders
lambda_ = st.slider("Wavelength λ", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
d = st.slider("Source Separation d", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

# Compute the interference pattern
I, x, y, S1, S2 = interference_pattern(lambda_, d)

# Create and display the plot
fig, ax = plt.subplots()
ax.imshow(I, cmap='hot', extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
ax.plot([S1[0], S2[0]], [S1[1], S2[1]], 'wo', markersize=5)  # Mark sources with white dots
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Interference Pattern")
st.pyplot(fig)