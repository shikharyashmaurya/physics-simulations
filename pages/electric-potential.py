import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.constants import k as coulomb_k

# Title of the app
st.title("Electric Potential Visualization")

# Sidebar for user inputs
st.sidebar.header("Charge Configuration")
num_charges = st.sidebar.selectbox("Number of charges", [1, 2, 3, 4, 5])

charges = []
for i in range(num_charges):
    st.sidebar.subheader(f"Charge {i+1}")
    # Sliders for charge magnitude and position
    Q = st.sidebar.slider(f"Q_{i+1} (arbitrary units)", min_value=-10.0, max_value=10.0, value=1.0, key=f"Q{i}")
    x = st.sidebar.slider(f"x_{i+1}", min_value=-5.0, max_value=5.0, value=0.0, key=f"x{i}")
    y = st.sidebar.slider(f"y_{i+1}", min_value=-5.0, max_value=5.0, value=0.0, key=f"y{i}")
    charges.append({'Q': Q, 'x': x, 'y': y})

# Define the 2D grid for calculation
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Calculate total electric potential
V = np.zeros_like(X)
for charge in charges:
    r = np.sqrt((X - charge['x'])**2 + (Y - charge['y'])**2)
    # Avoid division by zero at charge location
    r = np.where(r == 0, 1e-6, r)
    V += coulomb_k * charge['Q'] / r

# Create interactive Plotly contour plot
fig = go.Figure(data=go.Contour(x=x, y=y, z=V, colorscale='RdBu', colorbar=dict(title='Potential')))

# Add charge markers
for charge in charges:
    color = 'red' if charge['Q'] > 0 else 'blue'
    fig.add_trace(go.Scatter(x=[charge['x']], y=[charge['y']], mode='markers', 
                             marker=dict(color=color, size=10)))

# Customize plot layout
fig.update_layout(title='Electric Potential', xaxis_title='x', yaxis_title='y')
fig.update_yaxes(scaleanchor="x", scaleratio=1)  # Equal aspect ratio

# Display the plot in Streamlit
st.plotly_chart(fig)