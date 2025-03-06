import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
epsilon_0 = 8.85e-12  # Permittivity of free space in F/m

# Streamlit UI
st.title("Capacitance Simulation")
st.markdown("""
This simulation demonstrates the capacitance of a parallel plate capacitor.
- **Capacitance (C)** is calculated as \( C = \epsilon_0 \frac{A}{d} \), where \(\epsilon_0 = 8.85 \times 10^{-12} \, \text{F/m}\).
- **Charge (Q)** is calculated as \( Q = C \times V \).
Adjust the sliders below to explore how \(A\), \(d\), and \(V\) affect \(C\) and \(Q\).
""")

# Inputs
A = st.slider("Plate Area (m²)", 0.01, 1.0, 0.1, step=0.01)
d = st.slider("Plate Separation (m)", 0.001, 0.1, 0.01, step=0.001)
V = st.slider("Voltage (V)", 0.0, 10.0, 5.0, step=0.1)

# Calculations
C = epsilon_0 * A / d
Q = C * V

# Display results
st.write(f"**Capacitance (C):** {C:.2e} F")
st.write(f"**Charge (Q):** {Q:.2e} C")

# Visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Capacitor diagram
h = 0.05  # Fixed height of plates
# Scale width based on sqrt(A) for visual representation
w = 0.1 + 0.4 * (np.sqrt(A) - np.sqrt(0.01)) / (np.sqrt(1) - np.sqrt(0.01))
# Scale separation based on d
d_scaled = 0.1 + 0.4 * (d - 0.001) / (0.1 - 0.001)

# Draw bottom plate
ax1.add_patch(plt.Rectangle((0.5 - w/2, 0), w, h, color='blue'))
# Draw top plate
ax1.add_patch(plt.Rectangle((0.5 - w/2, d_scaled), w, h, color='red'))
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.set_title("Parallel Plate Capacitor")
ax1.axis('off')
# Add labels
ax1.text(0.5, -0.1, f'A = {A:.2f} m²', ha='center')
ax1.text(0.5, d_scaled/2, f'd = {d:.3f} m', ha='center', va='center')

# Q vs V plot
V_range = np.linspace(0, 10, 100)
Q_range = C * V_range
ax2.plot(V_range, Q_range, label=f'C = {C:.2e} F')
ax2.plot(V, Q, 'ro', label='Current point')
ax2.set_xlabel('Voltage (V)')
ax2.set_ylabel('Charge (C)')
ax2.set_title('Q vs V')
ax2.legend()
ax2.grid(True)

# Display the plot
st.pyplot(fig)