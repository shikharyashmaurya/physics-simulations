import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_work(force, displacement, angle):
    """
    Calculate work done by a force
    
    Parameters:
    force (float): Magnitude of force (Newtons)
    displacement (float): Distance moved (meters)
    angle (float): Angle between force and displacement (degrees)
    
    Returns:
    float: Work done (Joules)
    """
    # Convert angle to radians
    angle_rad = np.deg2rad(angle)
    
    # Calculate work: W = F * d * cos(θ)
    work = force * displacement * np.cos(angle_rad)
    
    return work

def plot_work_visualization(force, displacement, angle):
    """
    Create a visual representation of work
    
    Parameters:
    force (float): Magnitude of force (Newtons)
    displacement (float): Distance moved (meters)
    angle (float): Angle between force and displacement (degrees)
    
    Returns:
    matplotlib figure
    """
    # Calculate work
    work = calculate_work(force, displacement, angle)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw displacement vector
    ax.arrow(0, 0, displacement, 0, head_width=0.2, head_length=0.3, fc='blue', ec='blue', label='Displacement')
    
    # Draw force vector
    force_x = force * np.cos(np.deg2rad(angle))
    force_y = force * np.sin(np.deg2rad(angle))
    ax.arrow(0, 0, force_x, force_y, head_width=0.2, head_length=0.3, fc='red', ec='red', label='Force')
    
    # Set plot properties
    ax.set_xlim(-1, displacement + 1)
    ax.set_ylim(-1, max(force_y, displacement) + 1)
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Force (N)')
    ax.set_title('Work Visualization')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Annotate work
    ax.text(displacement/2, max(force_y, displacement)/2, 
            f'Work = {work:.2f} J\nW = F * d * cos(θ)', 
            bbox=dict(facecolor='white', alpha=0.5))
    
    return fig

def main():
    # Set up the Streamlit app
    st.title('Work Visualization in Physics')
    
    # Sidebar for inputs
    st.sidebar.header('Work Parameters')
    force = st.sidebar.slider('Force (Newtons)', min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    displacement = st.sidebar.slider('Displacement (meters)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    angle = st.sidebar.slider('Angle between Force and Displacement (degrees)', 
                               min_value=0, max_value=180, value=0, step=1)
    
    # Calculate work
    work = calculate_work(force, displacement, angle)
    
    # Display results
    st.header('Work Calculation')
    st.write(f'Force: {force} N')
    st.write(f'Displacement: {displacement} m')
    st.write(f'Angle: {angle}°')
    st.write(f'Work Done: {work:.2f} J')
    
    # Explain work formula
    st.markdown("""
    ### Work Formula Explanation
    Work is calculated using the formula: 
    **W = F * d * cos(θ)**
    
    Where:
    - W is Work (in Joules, J)
    - F is Force (in Newtons, N)
    - d is Displacement (in meters, m)
    - θ is the angle between the force and displacement vectors
    """)
    
    # Work visualization
    st.header('Work Visualization')
    fig = plot_work_visualization(force, displacement, angle)
    st.pyplot(fig)
    
    # Interactive explanation
    st.markdown("""
    ### Key Insights
    - When the force is parallel to displacement (0°), work is maximum
    - When the force is perpendicular to displacement (90°), no work is done
    - When the force is opposite to displacement (180°), work is negative
    """)

# Run the app
if __name__ == '__main__':
    main()

# Save instructions for running the app
'''
To run this Streamlit app:
1. Save this script as work_visualization.py
2. Install required libraries:
   pip install streamlit numpy matplotlib
3. Run the app:
   streamlit run work_visualization.py
'''