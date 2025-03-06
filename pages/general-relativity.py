import streamlit as st
import numpy as np
import plotly.graph_objects as go

def generate_surface(mass, grid_size=100, range_val=10):
    """
    Generates a grid and calculates a "curvature" value for each point,
    using a simplified gravitational potential analogy:
    
      Z = - mass / sqrt(x^2 + y^2 + epsilon)
    
    The epsilon is added to avoid singularity at (0,0).
    """
    x = np.linspace(-range_val, range_val, grid_size)
    y = np.linspace(-range_val, range_val, grid_size)
    X, Y = np.meshgrid(x, y)
    epsilon = 0.1  # small constant to prevent division by zero
    Z = -mass / np.sqrt(X**2 + Y**2 + epsilon)
    return X, Y, Z

def main():
    st.title("General Relativity Visualization")
    st.write("""
    This simulation visualizes a simplified model of space-time curvature due to a massive object.
    Although general relativity is much more complex, the following "rubber-sheet" analogy
    helps illustrate how mass can curve space.
    """)

    # Sidebar controls for interactivity
    mass = st.sidebar.slider("Mass", min_value=1.0, max_value=10.0, value=5.0, step=0.5,
                             help="Increase mass to deepen the gravitational well.")
    grid_size = st.sidebar.slider("Grid Resolution", min_value=50, max_value=200, value=100, step=10,
                                  help="Adjust the grid resolution of the visualization.")
    range_val = st.sidebar.slider("Range", min_value=5, max_value=20, value=10, step=1,
                                  help="Set the spatial range for the grid (in arbitrary units).")

    # Generate the grid and curvature data
    X, Y, Z = generate_surface(mass, grid_size, range_val)

    # Create a 3D surface plot using Plotly
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis")])
    fig.update_layout(
        title="Space-time Curvature",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Curvature (analogy)",
            aspectratio=dict(x=1, y=1, z=0.5)
        ),
        autosize=True
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
