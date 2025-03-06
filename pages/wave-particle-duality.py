import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Wave-Particle Duality: Double-Slit Experiment Simulation")

# Sidebar controls for parameters
st.sidebar.header("Experiment Parameters")
wavelength = st.sidebar.slider("Wavelength (λ) [m]", 0.1, 2.0, 0.5, step=0.1)
slit_separation = st.sidebar.slider("Slit Separation (d) [m]", 0.5, 5.0, 1.0, step=0.1)
screen_distance = st.sidebar.slider("Distance to Screen (L) [m]", 10, 100, 50, step=1)
num_particles = st.sidebar.slider("Number of Particles", 100, 10000, 1000, step=100)
simulate_particles = st.sidebar.button("Simulate Particle Impacts")

# Define spatial domain on the screen (in meters)
x = np.linspace(-0.05, 0.05, 500)

# Calculate the phase difference for the two slits
# Under the small-angle approximation: sin(theta) ~ x / L
phase = (np.pi * slit_separation * x) / (wavelength * screen_distance)
# Intensity from two-slit interference (ignoring single-slit envelope)
intensity = np.cos(phase) ** 2

st.subheader("Wave Interference Pattern")
fig_wave, ax_wave = plt.subplots(figsize=(8, 4))
ax_wave.plot(x, intensity, color='blue', lw=2)
ax_wave.set_xlabel("Position on Screen (m)")
ax_wave.set_ylabel("Intensity (a.u.)")
ax_wave.set_title("Theoretical Interference Pattern")
st.pyplot(fig_wave)

st.subheader("Particle Detection Simulation")
if simulate_particles:
    # Normalize the intensity to create a probability distribution
    prob_distribution = intensity / np.sum(intensity)
    # Sample particle landing positions based on the intensity distribution
    particle_positions = np.random.choice(x, size=num_particles, p=prob_distribution)
    
    # Plot the histogram of particle impacts
    fig_particles, ax_particles = plt.subplots(figsize=(8, 4))
    bins = np.linspace(x.min(), x.max(), 50)
    ax_particles.hist(particle_positions, bins=bins, density=True, alpha=0.6, color='red', label="Particle Hits")
    
    # Overlay the normalized theoretical intensity pattern
    norm_intensity = intensity / intensity.max()
    ax_particles.plot(x, norm_intensity, color='blue', lw=2, label="Wave Intensity (normalized)")
    ax_particles.set_xlabel("Position on Screen (m)")
    ax_particles.set_ylabel("Probability Density (normalized)")
    ax_particles.set_title("Accumulated Particle Impacts vs. Wave Intensity")
    ax_particles.legend()
    st.pyplot(fig_particles)
else:
    st.write("Use the sidebar button to simulate particle impacts based on the interference pattern.")
