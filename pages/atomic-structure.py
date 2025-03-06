import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Dictionary of elements (atomic number: (name, symbol))
elements = {
    1: ("Hydrogen", "H"),
    2: ("Helium", "He"),
    3: ("Lithium", "Li"),
    4: ("Beryllium", "Be"),
    5: ("Boron", "B"),
    6: ("Carbon", "C"),
    7: ("Nitrogen", "N"),
    8: ("Oxygen", "O"),
    9: ("Fluorine", "F"),
    10: ("Neon", "Ne"),
    # Add more elements as needed
}

# Function to calculate electron shells
def get_electron_shells(electrons):
    shells = []
    n = 1
    while electrons > 0:
        max_electrons = 2 * n**2
        if electrons >= max_electrons:
            shells.append(max_electrons)
            electrons -= max_electrons
        else:
            shells.append(electrons)
            electrons = 0
        n += 1
    return shells

# Streamlit app
st.title("Atomic Structure Visualizer")

# User inputs
col1, col2, col3 = st.columns(3)
with col1:
    Z = st.number_input("Number of protons (Z)", min_value=1, max_value=118, value=6)
with col2:
    N = st.number_input("Number of neutrons (N)", min_value=0, value=6)
with col3:
    E = st.number_input("Number of electrons (E)", min_value=0, value=Z)

# Calculate atomic properties
A = Z + N  # Mass number
charge = Z - E  # Charge of the ion
name, symbol = elements.get(Z, ("Unknown", "?"))

# Display atomic information
st.subheader("Atomic Information")
st.write(f"**Element**: {name} ({symbol})")
st.write(f"**Atomic Number**: {Z}")
st.write(f"**Mass Number**: {A}")
st.write(f"**Number of Electrons**: {E}")
st.write(f"**Charge**: {'+' if charge > 0 else ''}{charge}" if charge != 0 else "Neutral atom")

# Calculate electron shells
shells = get_electron_shells(E)

# Nucleus parameters
nucleus_radius = 0.1

# Generate proton positions
proton_theta = np.random.uniform(0, 2 * np.pi, Z)
proton_r = np.random.uniform(0, nucleus_radius, Z)
proton_x = proton_r * np.cos(proton_theta)
proton_y = proton_r * np.sin(proton_theta)

# Generate neutron positions
neutron_theta = np.random.uniform(0, 2 * np.pi, N)
neutron_r = np.random.uniform(0, nucleus_radius, N)
neutron_x = neutron_r * np.cos(neutron_theta)
neutron_y = neutron_r * np.sin(neutron_theta)

# Generate electron positions
electron_x = []
electron_y = []
r_shell = 1.0  # Radius increment per shell
for n, k in enumerate(shells, start=1):
    r = n * r_shell
    angles = np.linspace(0, 2 * np.pi, k, endpoint=False)
    for angle in angles:
        electron_x.append(r * np.cos(angle))
        electron_y.append(r * np.sin(angle))

# Create Plotly figure
fig = go.Figure()

# Add protons
fig.add_trace(go.Scatter(
    x=proton_x, y=proton_y,
    mode='markers',
    name='Protons',
    marker=dict(color='red', size=8)
))

# Add neutrons
fig.add_trace(go.Scatter(
    x=neutron_x, y=neutron_y,
    mode='markers',
    name='Neutrons',
    marker=dict(color='blue', size=8)
))

# Add electrons
fig.add_trace(go.Scatter(
    x=electron_x, y=electron_y,
    mode='markers',
    name='Electrons',
    marker=dict(color='green', size=10)
))

# Add shell circles
for n in range(1, len(shells) + 1):
    fig.add_shape(
        type="circle",
        x0=-n * r_shell, y0=-n * r_shell,
        x1=n * r_shell, y1=n * r_shell,
        line=dict(color="gray", width=1, dash="dash")
    )

# Set plot limits and aspect ratio
max_r = max(0.5, len(shells) * r_shell)
fig.update_xaxes(range=[-max_r, max_r])
fig.update_yaxes(range=[-max_r, max_r], scaleanchor="x", scaleratio=1)

# Update layout
fig.update_layout(
    title="Atomic Structure",
    width=600,
    height=600,
    showlegend=True
)

# Display plot in Streamlit
st.plotly_chart(fig)

# Instructions
st.markdown("""
### How to Use
- **Protons (Z)**: Defines the element (e.g., Z=6 for Carbon).
- **Neutrons (N)**: Affects the mass number (A = Z + N).
- **Electrons (E)**: Determines if it's an ion (Charge = Z - E).
- Adjust the inputs to visualize different atoms or ions!
""")