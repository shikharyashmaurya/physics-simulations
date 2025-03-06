import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Uncertainty Principle Visualization")
st.write("This simulation demonstrates the trade-off between the localization of a quantum wave packet in position space and its spread in momentum space. Adjust the slider to change the width (σ) of the Gaussian wave packet.")

# Slider for wave packet width (sigma)
sigma = st.slider("Select the width (σ) of the Gaussian wave packet in position space", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

# Set up the spatial grid
N = 1024  # number of points
x = np.linspace(-10, 10, N)
dx = x[1] - x[0]

# Define the Gaussian wave function in position space
psi_x = (1/(2*np.pi*sigma**2)**0.25) * np.exp(-x**2/(4*sigma**2))
prob_x = np.abs(psi_x)**2  # probability density in position space

# Fourier transform to get the momentum space wave function (assuming ħ = 1)
# Use fftshift and ifftshift to center the zero frequency component
psi_p = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(psi_x))) * dx / np.sqrt(2*np.pi)

# Define momentum grid corresponding to the Fourier frequencies
p = np.fft.fftshift(np.fft.fftfreq(N, d=dx)) * 2*np.pi
prob_p = np.abs(psi_p)**2  # probability density in momentum space

# Plot the position probability density
fig1, ax1 = plt.subplots()
ax1.plot(x, prob_x, color='blue')
ax1.set_title("Position Probability Density |ψ(x)|²")
ax1.set_xlabel("Position (x)")
ax1.set_ylabel("Probability Density")
st.pyplot(fig1)

# Plot the momentum probability density
fig2, ax2 = plt.subplots()
ax2.plot(p, prob_p, color='red')
ax2.set_title("Momentum Probability Density |ψ(p)|²")
ax2.set_xlabel("Momentum (p)")
ax2.set_ylabel("Probability Density")
st.pyplot(fig2)

# Calculate standard deviations in position and momentum
sigma_x = np.sqrt(np.sum(x**2 * prob_x) * dx)
dp = p[1] - p[0]
sigma_p = np.sqrt(np.sum(p**2 * prob_p) * dp)
uncertainty_product = sigma_x * sigma_p

st.write(f"Calculated uncertainty product σₓ * σₚ = {uncertainty_product:.3f} (expected ~0.5 for a Gaussian wave packet)")
