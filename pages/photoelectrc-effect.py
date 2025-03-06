import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title and explanation
st.title("Photoelectric Effect Simulation")

st.write("""
### Explanation
The **photoelectric effect** occurs when light of frequency ν strikes a metal surface, causing electrons to be emitted if ν exceeds the threshold frequency ν₀ = φ / h, where:
- **φ** is the work function of the metal (energy required to eject an electron),
- **h** is Planck's constant.

The **kinetic energy (KE)** of the emitted electrons is:
- KE = h(ν - ν₀) if ν > ν₀,
- KE = 0 otherwise.

The **photoelectric current** (number of electrons emitted per second) is proportional to the light intensity I when ν > ν₀, and zero otherwise.

For simplicity, this simulation sets h = 1 (arbitrary units), so ν₀ = φ. All quantities (frequency, work function, energy, intensity, current) are in arbitrary units to focus on the relationships.
""")

# Sidebar with input sliders
st.sidebar.header("Adjust Parameters")
ν = st.sidebar.slider('Frequency ν', min_value=0.0, max_value=10.0, value=5.0, step=0.1)
φ = st.sidebar.slider('Work function φ', min_value=0.0, max_value=5.0, value=2.0, step=0.1)
I = st.sidebar.slider('Intensity I', min_value=0.0, max_value=10.0, value=5.0, step=0.1)

# Constants and calculations
# h = 1.0  # Planck's constant in arbitrary units
# ν₀ = φ / h  # Threshold frequency (since h=1, ν₀=φ)
# KE = max(ν - φ, 0)  # Kinetic energy of emitted electrons
# current = I if ν > φ else 0  # Photoelectric current

# Constants and calculations
h = 1.0  # Planck's constant in arbitrary units
nu0 = φ / h  # Threshold frequency (since h=1, nu0=φ)
KE = max(ν - φ, 0)  # Kinetic energy of emitted electrons
current = I if ν > φ else 0  # Photoelectric current


# Generate data for plotting
ν_range = np.linspace(0, 10, 100)
KE_range = np.maximum(ν_range - φ, 0)  # KE for the range of frequencies
current_range = np.where(ν_range > φ, I, 0)  # Current for the range of frequencies

# Create interactive plot with Plotly
fig = go.Figure()

# Add trace for Kinetic Energy
fig.add_trace(go.Scatter(x=ν_range, y=KE_range, name='Kinetic Energy', line=dict(color='blue')))

# Add trace for Current (using step-like behavior)
fig.add_trace(go.Scatter(x=ν_range, y=current_range, name='Current', yaxis='y2', line=dict(color='green', shape='hv')))

# Add vertical line at selected frequency
fig.add_vline(x=ν, line_dash='dash', line_color='red')

# Add shaded region for ν < φ (no emission)
fig.add_shape(type='rect', x0=0, x1=φ, y0=0, y1=10, fillcolor='lightgray', opacity=0.5, layer='below')

# Update layout with titles and axis ranges
fig.update_layout(
    title='Photoelectric Effect',
    xaxis_title='Frequency ν',
    xaxis_range=[0, 10],
    yaxis=dict(title='Kinetic Energy', range=[0, 10], titlefont=dict(color='blue'), tickfont=dict(color='blue')),
    yaxis2=dict(title='Current', range=[0, 10], overlaying='y', side='right', titlefont=dict(color='green'), tickfont=dict(color='green')),
    legend=dict(x=0.75, y=0.95),
)

# Display the plot in Streamlit
st.plotly_chart(fig)

# Display simulation results
st.subheader("Simulation Results")
st.write(f"Selected frequency ν = {ν}")
st.write(f"Work function φ = {φ}")
st.write(f"Intensity I = {I}")

if ν > φ:
    st.write("**Electrons are emitted**")
    st.write(f"Kinetic energy of emitted electrons: {KE:.2f}")
    st.write(f"Photoelectric current: {current:.2f}")
else:
    st.write("**No electrons are emitted**")