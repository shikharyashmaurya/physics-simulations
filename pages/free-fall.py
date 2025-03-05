import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_free_fall(initial_height, gravity=9.8):
    """
    Calculate free fall motion parameters
    
    Args:
    initial_height (float): Starting height in meters
    gravity (float): Acceleration due to gravity (default 9.8 m/s²)
    
    Returns:
    tuple: Time of fall, position array, velocity array
    """
    # Calculate time to hit ground
    time_to_ground = np.sqrt(2 * initial_height / gravity)
    
    # Create time array
    time = np.linspace(0, time_to_ground, 100)
    
    # Calculate position and velocity
    position = initial_height - 0.5 * gravity * time**2
    velocity = -gravity * time
    
    return time, position, velocity

def plot_free_fall(time, position, velocity):
    """
    Create plots for free fall motion
    
    Args:
    time (array): Time array
    position (array): Position array
    velocity (array): Velocity array
    
    Returns:
    matplotlib figure
    """
    # Create figure and axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), 
                                   gridspec_kw={'height_ratios': [2, 1]})
    
    # Position plot
    ax1.plot(time, position, 'b-')
    ax1.scatter(time[-1], position[-1], color='red', s=100)
    ax1.set_title('Free Fall - Position vs Time')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Height (m)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Velocity plot
    ax2.plot(time, velocity, 'g-')
    ax2.scatter(time[-1], velocity[-1], color='red', s=100)
    ax2.set_title('Free Fall - Velocity vs Time')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    return fig

def main():
    """
    Streamlit app for Free Fall Simulation
    """
    st.title('Free Fall Motion Simulator')
    
    # Sidebar for inputs
    st.sidebar.header('Simulation Parameters')
    
    # Initial height input
    initial_height = st.sidebar.slider(
        'Initial Height (m)', 
        min_value=1.0, 
        max_value=100.0, 
        value=10.0, 
        step=0.5
    )
    
    # Gravity selection (optional)
    gravity_options = [
        ('Earth (9.8 m/s²)', 9.8),
        ('Moon (1.6 m/s²)', 1.6),
        ('Mars (3.7 m/s²)', 3.7),
    ]
    gravity = st.sidebar.selectbox(
        'Planet/Location', 
        gravity_options,
        format_func=lambda x: x[0]
    )[1]
    
    # Calculate free fall motion
    time, position, velocity = calculate_free_fall(initial_height, gravity)
    
    # Create columns for information display
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('Initial Height', f'{initial_height} m')
        st.metric('Time to Ground', f'{time[-1]:.2f} s')
    
    with col2:
        st.metric('Gravity', f'{gravity} m/s²')
        st.metric('Final Velocity', f'{velocity[-1]:.2f} m/s')
    
    # Create and display plots
    st.header('Motion Visualization')
    fig = plot_free_fall(time, position, velocity)
    
    # Display matplotlib figure
    st.pyplot(fig)
    
    # Detailed explanation
    st.markdown("""
    ### Physics Behind Free Fall

    In free fall motion:
    - The object falls under the influence of gravity
    - Acceleration is constant (9.8 m/s² on Earth)
    - Air resistance is neglected
    - Position follows quadratic equation: 
      $h(t) = h_0 - \\frac{1}{2}gt^2$
    - Velocity follows linear equation: 
      $v(t) = -gt$
    
    ### How to Interpret the Graphs
    - Top Graph: Shows object's height decreasing over time
    - Bottom Graph: Shows velocity increasing in magnitude 
      (becoming more negative) as the object falls
    - Red dot indicates final position/velocity
    """)

if __name__ == '__main__':
    main()

# Installation requirements
# Run in terminal:
# pip install streamlit numpy matplotlib
# streamlit run free_fall_simulation.py