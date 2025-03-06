import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Quantum Wave Packet Simulation", layout="wide")

st.title("Quantum Wave Packet Evolution Simulation")
st.write("""
This simulation visualizes the time evolution of a free-particle Gaussian wave packet in one dimension.
We assume natural units where ℏ = 1 and m = 1. Adjust the parameters in the sidebar to see how the
probability density evolves with time.
""")

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")
sigma = st.sidebar.slider("Initial width (σ)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
x0 = st.sidebar.slider("Initial position (x₀)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
p0 = st.sidebar.slider("Initial momentum (p₀)", min_value=-5.0, max_value=5.0, value=1.0, step=0.1)
t = st.sidebar.slider("Time (t)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

# Create a range of x values
x = np.linspace(-20, 20, 800)

# Calculate the time-dependent width sigma_t
sigma_t = sigma * np.sqrt(1 + (t / sigma**2)**2)

# Compute the probability density |ψ(x,t)|^2 for a free-particle Gaussian wave packet
# The center of the packet moves with velocity p0 and the packet spreads over time.
prob_density = (1 / (np.sqrt(np.pi) * sigma_t)) * np.exp(-((x - x0 - p0 * t) ** 2) / (sigma_t**2))

# Create the plot
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, prob_density, color="blue", lw=2, label=r"$|\psi(x,t)|^2$")
ax.set_xlabel("Position (x)")
ax.set_ylabel("Probability Density")
ax.set_title("Gaussian Wave Packet Evolution")
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

# Additional explanation
st.write("""
The simulation uses an analytic expression for a Gaussian wave packet. Notice that as time increases,
the packet not only translates (due to the initial momentum *p₀*) but also spreads, which is a hallmark of quantum evolution.
""")
