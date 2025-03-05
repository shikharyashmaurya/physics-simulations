import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def constant_velocity_motion(initial_position, velocity, time):
    """Calculate position for constant velocity motion."""
    return initial_position + velocity * time

def accelerated_motion(initial_position, initial_velocity, acceleration, time):
    """Calculate position for uniformly accelerated motion."""
    return initial_position + initial_velocity * time + 0.5 * acceleration * time**2

def plot_position_graph(times, positions):
    """Create a position vs time graph."""
    plt.figure(figsize=(10, 6))
    plt.plot(times, positions, 'b-', linewidth=2)
    plt.title('Position vs Time Graph', fontsize=15)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Position (m)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    return plt

def main():
    st.title('Physics Motion Visualization: Position')
    
    # Sidebar for motion type selection
    motion_type = st.sidebar.selectbox(
        'Select Motion Type',
        ['Constant Velocity', 'Uniformly Accelerated Motion']
    )
    
    # Input parameters
    st.sidebar.header('Motion Parameters')
    
    if motion_type == 'Constant Velocity':
        initial_position = st.sidebar.number_input('Initial Position (m)', value=0.0, step=0.1)
        velocity = st.sidebar.number_input('Velocity (m/s)', value=1.0, step=0.1)
        
        # Time range for visualization
        time_start = st.sidebar.number_input('Start Time (s)', value=0.0, step=0.1)
        time_end = st.sidebar.number_input('End Time (s)', value=10.0, step=0.1)
        time_step = st.sidebar.number_input('Time Step (s)', value=0.5, step=0.1)
        
        # Calculate positions
        times = np.arange(time_start, time_end + time_step, time_step)
        positions = [constant_velocity_motion(initial_position, velocity, t) for t in times]
        
    else:  # Uniformly Accelerated Motion
        initial_position = st.sidebar.number_input('Initial Position (m)', value=0.0, step=0.1)
        initial_velocity = st.sidebar.number_input('Initial Velocity (m/s)', value=0.0, step=0.1)
        acceleration = st.sidebar.number_input('Acceleration (m/s²)', value=2.0, step=0.1)
        
        # Time range for visualization
        time_start = st.sidebar.number_input('Start Time (s)', value=0.0, step=0.1)
        time_end = st.sidebar.number_input('End Time (s)', value=10.0, step=0.1)
        time_step = st.sidebar.number_input('Time Step (s)', value=0.5, step=0.1)
        
        # Calculate positions
        times = np.arange(time_start, time_end + time_step, time_step)
        positions = [accelerated_motion(initial_position, initial_velocity, acceleration, t) for t in times]
    
    # Display graph
    st.header(f'{motion_type} Visualization')
    
    # Plot the graph
    plt = plot_position_graph(times, positions)
    st.pyplot(plt)
    
    # Display position table
    st.subheader('Position Data')
    position_data = {
        'Time (s)': times,
        'Position (m)': positions
    }
    st.dataframe(position_data)
    
    # Additional explanations
    st.markdown("""
    ### Understanding the Graph
    - **X-axis**: Represents time in seconds
    - **Y-axis**: Represents position in meters
    
    ### Interpretation
    - In constant velocity motion, the position changes linearly with time
    - In uniformly accelerated motion, the position changes quadratically with time
    """)

if __name__ == '__main__':
    main()