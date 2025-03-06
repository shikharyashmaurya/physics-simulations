import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Quantization Visualization", layout="centered")

st.title("Visualization of Quantization: Particle in a Box")

# Sidebar controls for interactive parameters
st.sidebar.header("Simulation Parameters")
L = st.sidebar.slider("Length of the Box (L)", min_value=1.0, max_value=10.0, value=1.0, step=0.1)
n = st.sidebar.slider("Quantum Number (n)", min_value=1, max_value=10, value=1, step=1)

# Define spatial domain inside the box
x = np.linspace(0, L, 1000)

# Compute the wavefunction for a particle in an infinite potential well:
# ψ_n(x) = sqrt(2/L) * sin(nπx/L)
psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
# Probability density is |ψ(x)|²
prob_density = psi**2

# Display an energy estimate (in arbitrary units, since E ∝ n² for a particle in a box)
E_n = n**2
st.write(f"Energy of level n = {n} is proportional to {E_n} (arbitrary units)")

# Plot the probability density
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, prob_density, label=f"|ψ(x)|² for n = {n}")
ax.set_xlabel("Position x")
ax.set_ylabel("Probability Density")
ax.set_title("Particle in a Box: Probability Density")
ax.legend()
st.pyplot(fig)
