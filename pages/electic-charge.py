import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Initialize session state to store charges
if 'charges' not in st.session_state:
    st.session_state.charges = []

# User interface
st.title("Electric Charge Simulation")
st.write("Add charges and visualize the forces between them.")

# Input fields for adding a charge
x = st.number_input("X position", min_value=-10.0, max_value=10.0, value=0.0)
y = st.number_input("Y position", min_value=-10.0, max_value=10.0, value=0.0)
q = st.selectbox("Charge", [1, -1])

# Button to add a charge
if st.button("Add Charge"):
    st.session_state.charges.append({'x': x, 'y': y, 'q': q})

# Button to clear all charges
if st.button("Clear All Charges"):
    st.session_state.charges = []

# Slider to adjust force arrow scale
force_scale = st.slider("Force scale", min_value=0.1, max_value=10.0, value=1.0)

# Create Plotly figure
fig = go.Figure()

# Plot all charges
for charge in st.session_state.charges:
    fig.add_trace(go.Scatter(
        x=[charge['x']], 
        y=[charge['y']], 
        mode='markers+text', 
        text=[str(charge['q'])], 
        textposition='top right', 
        marker=dict(size=10, color='red' if charge['q'] > 0 else 'blue')
    ))

# Calculate and plot forces
k = 1.0  # Coulomb's constant (simplified for visualization)
for charge in st.session_state.charges:
    Fx, Fy = 0, 0
    for other in st.session_state.charges:
        if other != charge:  # Skip self-interaction
            dx = other['x'] - charge['x']
            dy = other['y'] - charge['y']
            r = np.sqrt(dx**2 + dy**2)
            if r > 0:  # Avoid division by zero
                # Force magnitude: F = k * q1 * q2 / r^2
                F = k * charge['q'] * other['q'] / (r**2)
                # Force components along unit vector from other to charge
                Fx += F * (-dx / r)
                Fy += F * (-dy / r)
    # Draw force arrow
    arrow_dx = Fx * force_scale
    arrow_dy = Fy * force_scale
    if np.sqrt(arrow_dx**2 + arrow_dy**2) > 0:  # Only draw if force exists
        fig.add_annotation(
            x=charge['x'] + arrow_dx,
            y=charge['y'] + arrow_dy,
            ax=charge['x'],
            ay=charge['y'],
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='green'
        )

# Configure plot layout
fig.update_layout(
    xaxis_range=[-10, 10],
    yaxis_range=[-10, 10],
    width=600,
    height=600,
    showlegend=False,
    title="Charge Interactions"
)

# Display the plot in Streamlit
st.plotly_chart(fig)