import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def magnetic_field_of_wire(x, y, z, current, wire_pos):
    """Calculate magnetic field due to infinite straight wire at position wire_pos"""
    r_vec = np.array([x - wire_pos[0], y - wire_pos[1], 0])
    r = np.sqrt(r_vec[0]**2 + r_vec[1]**2)
    
    # Prevent division by zero
    if r < 1e-10:
        return np.array([0, 0, 0])
    
    # Direction: cross product of z unit vector with r_vec
    direction = np.array([-r_vec[1], r_vec[0], 0]) / r
    
    # Magnitude: μ0 * I / (2π * r)
    mu0 = 4 * np.pi * 1e-7  # magnetic permeability
    magnitude = mu0 * current / (2 * np.pi * r)
    
    return magnitude * direction

def magnetic_field_of_loop(x, y, z, current, loop_center, radius):
    """Calculate magnetic field due to a circular current loop in the xy-plane"""
    # Distance from the point to loop center
    r_vec = np.array([x - loop_center[0], y - loop_center[1], z - loop_center[2]])
    r = np.sqrt(r_vec[0]**2 + r_vec[1]**2 + r_vec[2]**2)
    
    # Prevent division by zero
    if r < 1e-10:
        return np.array([0, 0, 0])
    
    # On-axis field calculation (simplified)
    mu0 = 4 * np.pi * 1e-7  # magnetic permeability
    
    if abs(r_vec[0]) < 1e-10 and abs(r_vec[1]) < 1e-10:
        # On the z-axis
        magnitude = mu0 * current * radius**2 / (2 * (radius**2 + r_vec[2]**2)**(3/2))
        return np.array([0, 0, magnitude if r_vec[2] >= 0 else -magnitude])
    
    # For off-axis points, return a more approximate field (full calculation is complex)
    # This is a simplification that gives reasonable visualization
    z_component = mu0 * current * radius**2 / (2 * (radius**2 + r**2)**(3/2))
    r_component = mu0 * current * radius**2 * r_vec[2] / (4 * r * (radius**2 + r**2)**(3/2))
    
    return np.array([
        r_component * r_vec[0]/r,
        r_component * r_vec[1]/r,
        z_component
    ])

def magnetic_field_of_bar_magnet(x, y, z, magnet_center, magnet_length, magnet_strength):
    """Calculate magnetic field due to a simple bar magnet (dipole approximation)"""
    r_vec = np.array([x - magnet_center[0], y - magnet_center[1], z - magnet_center[2]])
    r = np.sqrt(r_vec[0]**2 + r_vec[1]**2 + r_vec[2]**2)
    
    # Prevent division by zero
    if r < 1e-10:
        return np.array([0, 0, 0])
    
    # Dipole moment in the z-direction
    m_vec = np.array([0, 0, magnet_strength * magnet_length])
    
    # Dipole field formula
    mu0 = 4 * np.pi * 1e-7  # magnetic permeability
    constant = mu0 / (4 * np.pi * r**5)
    dot_product = np.dot(m_vec, r_vec)
    
    field = constant * (3 * r_vec * dot_product - r**2 * m_vec)
    
    return field

def plot_magnetic_field(field_type, parameters):
    """Generate the magnetic field plot"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create grid of points
    n = 20
    x = np.linspace(-5, 5, n)
    y = np.linspace(-5, 5, n)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)  # Z=0 plane
    
    # Calculate field at each point
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    W = np.zeros_like(Z)
    
    for i in range(n):
        for j in range(n):
            if field_type == "Wire":
                field = magnetic_field_of_wire(
                    X[i, j], Y[i, j], Z[i, j], 
                    parameters["current"], 
                    parameters["position"]
                )
            elif field_type == "Loop":
                field = magnetic_field_of_loop(
                    X[i, j], Y[i, j], Z[i, j], 
                    parameters["current"], 
                    parameters["center"], 
                    parameters["radius"]
                )
            elif field_type == "Bar Magnet":
                field = magnetic_field_of_bar_magnet(
                    X[i, j], Y[i, j], Z[i, j], 
                    parameters["center"], 
                    parameters["length"], 
                    parameters["strength"]
                )
            
            # Normalize the field for better visualization
            field_magnitude = np.sqrt(field[0]**2 + field[1]**2 + field[2]**2)
            if field_magnitude > 0:
                normalized_field = field / field_magnitude
            else:
                normalized_field = field
            
            U[i, j] = normalized_field[0]
            V[i, j] = normalized_field[1]
            W[i, j] = normalized_field[2]
    
    # Plot the magnetic field
    ax.streamplot(X, Y, U, V, density=2, color='b', linewidth=1, arrowsize=1)
    
    # Draw the source of the field
    if field_type == "Wire":
        ax.plot(parameters["position"][0], parameters["position"][1], 'ro', markersize=10)
        ax.annotate('Current into page' if parameters["current"] > 0 else 'Current out of page', 
                  xy=(parameters["position"][0], parameters["position"][1]), 
                  xytext=(parameters["position"][0] + 0.5, parameters["position"][1] + 0.5))
    elif field_type == "Loop":
        circle = Circle(parameters["center"][:2], parameters["radius"], fill=False, color='r')
        ax.add_patch(circle)
        ax.annotate('Current loop', 
                  xy=(parameters["center"][0], parameters["center"][1]), 
                  xytext=(parameters["center"][0] + 0.5, parameters["center"][1] + 0.5))
    elif field_type == "Bar Magnet":
        half_length = parameters["length"] / 2
        ax.plot([parameters["center"][0] - half_length, parameters["center"][0] + half_length], 
              [parameters["center"][1], parameters["center"][1]], 'r-', linewidth=4)
        ax.text(parameters["center"][0] - half_length - 0.3, parameters["center"][1], 'S')
        ax.text(parameters["center"][0] + half_length + 0.1, parameters["center"][1], 'N')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Magnetic Field of {field_type}')
    ax.grid(True)
    ax.set_aspect('equal')
    
    return fig

def main():
    st.title("Magnetic Field Visualization")
    st.write("""
    This app visualizes the magnetic field created by different sources.
    Choose a magnetic field source below and adjust the parameters to see how the field changes.
    """)
    
    # Sidebar for parameters
    st.sidebar.header("Field Source Parameters")
    
    # Select field type
    field_type = st.sidebar.selectbox(
        "Select a magnetic field source:",
        ["Wire", "Loop", "Bar Magnet"]
    )
    
    # Parameters based on field type
    if field_type == "Wire":
        current = st.sidebar.slider("Current (A)", -10.0, 10.0, 5.0)
        wire_x = st.sidebar.slider("Wire X Position", -3.0, 3.0, 0.0)
        wire_y = st.sidebar.slider("Wire Y Position", -3.0, 3.0, 0.0)
        
        parameters = {
            "current": current,
            "position": [wire_x, wire_y]
        }
        
        st.write("""
        ### Infinite Straight Wire
        
        The magnetic field around a long straight wire forms concentric circles around the wire.
        - Direction: determined by the right-hand rule (thumb points in the current direction)
        - Magnitude: proportional to the current and inversely proportional to the distance from the wire
        
        Mathematical formula: B = (μ₀ × I) / (2π × r)
        """)
        
    elif field_type == "Loop":
        current = st.sidebar.slider("Current (A)", -10.0, 10.0, 5.0)
        loop_x = st.sidebar.slider("Loop Center X", -3.0, 3.0, 0.0)
        loop_y = st.sidebar.slider("Loop Center Y", -3.0, 3.0, 0.0)
        loop_z = st.sidebar.slider("Loop Center Z", -3.0, 3.0, 0.0)
        radius = st.sidebar.slider("Loop Radius", 0.5, 3.0, 1.0)
        
        parameters = {
            "current": current,
            "center": [loop_x, loop_y, loop_z],
            "radius": radius
        }
        
        st.write("""
        ### Current Loop
        
        A current loop creates a magnetic field similar to a bar magnet.
        - Near the center of the loop, the field lines are nearly parallel
        - Far from the loop, the field approximates that of a dipole
        
        This is the basic principle behind electromagnets and solenoids.
        """)
        
    elif field_type == "Bar Magnet":
        magnet_x = st.sidebar.slider("Magnet Center X", -3.0, 3.0, 0.0)
        magnet_y = st.sidebar.slider("Magnet Center Y", -3.0, 3.0, 0.0)
        magnet_z = st.sidebar.slider("Magnet Center Z", -3.0, 3.0, 0.0)
        length = st.sidebar.slider("Magnet Length", 0.5, 3.0, 2.0)
        strength = st.sidebar.slider("Magnet Strength", 1.0, 10.0, 5.0)
        
        parameters = {
            "center": [magnet_x, magnet_y, magnet_z],
            "length": length,
            "strength": strength
        }
        
        st.write("""
        ### Bar Magnet
        
        A bar magnet produces a dipole magnetic field.
        - Field lines emerge from the north pole and enter the south pole
        - The field strength decreases with the cube of the distance from the magnet
        
        This simulation uses a simplified dipole approximation.
        """)
    
    # Generate and display plot
    fig = plot_magnetic_field(field_type, parameters)
    st.pyplot(fig)
    
    # Additional explanations
    st.write("""
    ### About Magnetic Fields
    
    Magnetic fields are vector fields that describe the magnetic influence on moving electric charges, electric currents, and magnetic materials.
    
    Key concepts:
    - Magnetic field lines are continuous loops
    - The density of field lines indicates the strength of the field
    - The direction of the field is determined by the right-hand rule
    
    The visualization shows a 2D slice (Z=0 plane) of the magnetic field, with arrows indicating the field direction.
    """)

if __name__ == "__main__":
    main()