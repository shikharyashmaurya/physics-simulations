import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34  # Planck's constant (J·s)
c = 299792458       # Speed of light (m/s)
k_B = 1.380649e-23  # Boltzmann constant (J/K)
b = 2.897e-3        # Wien's displacement constant (m·K)

# Planck's law function: Spectral radiance as a function of wavelength (in meters) and temperature
def planck(lambda_m, T):
    """Calculate spectral radiance B(lambda, T) in W/m²/sr/m."""
    return (2 * h * c**2 / lambda_m**5) / (np.exp(h * c / (lambda_m * k_B * T)) - 1)

# Streamlit app
st.title("Blackbody Radiation Simulation")

# Educational explanation
st.write("""
### Understanding Blackbody Radiation
A **blackbody** is an idealized object that absorbs all incoming radiation and re-emits it based solely on its temperature. The emitted radiation's intensity and wavelength distribution are described by **Planck's law**:

\[ B(\lambda, T) = \frac{2hc^2}{\lambda^5} \cdot \frac{1}{e^{\frac{hc}{\lambda k_B T}} - 1} \]

- \( \lambda \): Wavelength (m)
- \( T \): Temperature (K)
- \( h \): Planck's constant
- \( c \): Speed of light
- \( k_B \): Boltzmann constant

The **peak wavelength** (\( \lambda_{\text{peak}} \)) shifts with temperature according to **Wien's displacement law**:

\[ \lambda_{\text{peak}} = \frac{b}{T} \]

where \( b \approx 2.897 \times 10^{-3} \, \text{m·K} \). This simulation plots the spectrum and marks the peak.
""")

# User input
T = st.slider("Temperature (K)", min_value=300, max_value=10000, value=5000, step=100,
              help="Adjust the temperature to see how the radiation spectrum changes.")
normalize = st.checkbox("Normalize to maximum", value=True,
                       help="Normalize the curve to its peak value for shape comparison.")

# Wavelength array (in meters, from 50 nm to 50,000 nm)
lambda_m = np.linspace(5e-8, 5e-5, 1000)
# Calculate spectral radiance in W/m²/sr/m
B_m = planck(lambda_m, T)
# Convert to nanometers for plotting
lambda_nm = lambda_m * 1e9
# Convert spectral radiance to W/m²/sr/nm
B_nm = B_m / 1e9

# Prepare data for plotting
if normalize:
    B_plot = B_nm / B_nm.max()
    y_label = "Normalized Spectral Radiance"
else:
    B_plot = B_nm
    y_label = "Spectral Radiance (W/m²/sr/nm)"

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(lambda_nm, B_plot, label=f"T = {T} K")
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel(y_label)
ax.set_title(f"Blackbody Radiation Spectrum at T = {T} K")
ax.grid(True)

# Highlight visible spectrum (400 nm to 700 nm)
ax.axvspan(400, 700, color='yellow', alpha=0.3, label="Visible Range")

# Calculate and mark peak wavelength
lambda_peak_m = b / T
lambda_peak_nm = lambda_peak_m * 1e9
ax.axvline(lambda_peak_nm, color='red', linestyle='--', label=f"Peak: {lambda_peak_nm:.2f} nm")

# Add legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Display peak wavelength
st.write(f"**Peak wavelength**: {lambda_peak_nm:.2f} nm")