import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set up the title and description for the app
st.title("Quantum Decoherence Simulation: Double-Slit Interference")
st.write(
    """
    This simulation demonstrates how quantum decoherence affects an interference pattern.
    The two wave functions represent paths through two slits. Their interference term is
    scaled by a decoherence factor (D). When D = 1 the interference is maximal (fully coherent),
    and when D = 0, decoherence has washed out the interference.
    """
)

# Sidebar controls for simulation parameters
sigma = st.sidebar.slider("Gaussian width (sigma)", 0.5, 2.0, 1.0, help="Controls the spread of each wave packet.")
d = st.sidebar.slider("Slit separation (d)", 1.0, 5.0, 2.0, help="Distance of the centers of the two slits from the origin.")
k = st.sidebar.slider("Wave number (k)", 1.0, 10.0, 5.0, help="Determines the oscillation frequency of the waves.")
decoherence_factor = st.sidebar.slider("Decoherence factor (D)", 0.0, 1.0, 1.0, help="1.0 = full coherence, 0.0 = complete decoherence.")

# Generate an array of positions along which we calculate the intensity
x = np.linspace(-10, 10, 500)

# Define the two Gaussian wave functions with a phase factor
psi1 = np.exp(-((x - d)**2) / (2 * sigma**2)) * np.exp(1j * k * x)
psi2 = np.exp(-((x + d)**2) / (2 * sigma**2)) * np.exp(1j * k * x)

# Compute the intensity. The interference term is scaled by the decoherence factor.
intensity = np.abs(psi1)**2 + np.abs(psi2)**2 + 2 * decoherence_factor * np.real(psi1 * np.conj(psi2))

# Plot the resulting interference pattern
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, intensity, label=f"Decoherence factor = {decoherence_factor:.2f}")
ax.set_xlabel("Position (x)")
ax.set_ylabel("Intensity")
ax.set_title("Interference Pattern with Quantum Decoherence")
ax.legend()
ax.grid(True)

# Render the plot in the Streamlit app
st.pyplot(fig)
