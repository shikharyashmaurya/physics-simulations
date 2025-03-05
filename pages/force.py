import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculate_resultant_force(forces):
    """
    Calculate the resultant force vector from multiple forces.
    
    Args:
    forces (list): List of tuples (magnitude, angle in degrees)
    
    Returns:
    tuple: Resultant force magnitude and angle
    """
    # Convert forces to x and y components
    fx = sum(force[0] * np.cos(np.radians(force[1])) for force in forces)
    fy = sum(force[0] * np.sin(np.radians(force[1])) for force in forces)
    
    # Calculate resultant magnitude and angle
    resultant_magnitude = np.sqrt(fx**2 + fy**2)
    resultant_angle = np.degrees(np.arctan2(fy, fx))
    
    return resultant_magnitude, resultant_angle

def draw_force_diagram(forces):
    """
    Create a force diagram using matplotlib.
    
    Args:
    forces (list): List of tuples (magnitude, angle in degrees)
    
    Returns:
    matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title('Force Diagram')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    
    # Draw origin point
    ax.plot(0, 0, 'ro', markersize=10)
    
    # Colors for different forces
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    
    # Draw individual forces
    for i, (magnitude, angle) in enumerate(forces):
        color = colors[i % len(colors)]
        # Calculate x and y components
        fx = magnitude * np.cos(np.radians(angle))
        fy = magnitude * np.sin(np.radians(angle))
        
        # Draw force vector
        ax.arrow(0, 0, fx, fy, head_width=0.3, head_length=0.5, 
                 fc=color, ec=color, alpha=0.7, 
                 label=f'Force {i+1}: {magnitude} N at {angle}°')
    
    # Calculate and draw resultant force
    resultant_magnitude, resultant_angle = calculate_resultant_force(forces)
    ax.arrow(0, 0, 
             resultant_magnitude * np.cos(np.radians(resultant_angle)),
             resultant_magnitude * np.sin(np.radians(resultant_angle)),
             head_width=0.5, head_length=0.8, 
             fc='black', ec='black', alpha=1, 
             label=f'Resultant: {resultant_magnitude:.2f} N at {resultant_angle:.2f}°')
    
    ax.legend()
    return fig

def main():
    st.title('Force Visualization Simulator')
    
    st.sidebar.header('Force Input')
    
    # Initialize session state for forces
    if 'forces' not in st.session_state:
        st.session_state.forces = []
    
    # Force input
    magnitude = st.sidebar.number_input('Force Magnitude (N)', min_value=0.0, step=0.1, value=5.0)
    angle = st.sidebar.number_input('Force Angle (degrees)', min_value=0.0, max_value=360.0, step=1.0, value=0.0)
    
    # Add force button
    if st.sidebar.button('Add Force'):
        st.session_state.forces.append((magnitude, angle))
    
    # Remove force button
    if st.sidebar.button('Remove Last Force') and st.session_state.forces:
        st.session_state.forces.pop()
    
    # Clear all forces
    if st.sidebar.button('Clear All Forces'):
        st.session_state.forces = []
    
    # Display current forces
    st.sidebar.subheader('Current Forces:')
    for i, (mag, ang) in enumerate(st.session_state.forces, 1):
        st.sidebar.text(f'Force {i}: {mag} N at {ang}°')
    
    # Visualization
    if st.session_state.forces:
        fig = draw_force_diagram(st.session_state.forces)
        st.pyplot(fig)
        
        # Resultant force calculation
        resultant_magnitude, resultant_angle = calculate_resultant_force(st.session_state.forces)
        st.subheader('Resultant Force')
        st.write(f'Magnitude: {resultant_magnitude:.2f} N')
        st.write(f'Angle: {resultant_angle:.2f}°')
    else:
        st.info('Add forces to visualize the force diagram')

    # Physics explanation
    st.sidebar.markdown("""
    ### How to Use
    1. Enter force magnitude and angle
    2. Click 'Add Force' to include in diagram
    3. Visualize vector forces and resultant
    
    ### Force Visualization Concepts
    - **Magnitude**: Strength of the force (Newtons)
    - **Angle**: Direction of the force (0-360 degrees)
    - **Resultant Force**: Combined effect of all forces
    """)

if __name__ == '__main__':
    main()