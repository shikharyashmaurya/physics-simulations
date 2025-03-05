import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_impulse(force, time):
    """Calculate impulse given force and time."""
    return force * time

def calculate_velocity_change(mass, impulse):
    """Calculate change in velocity using impulse-momentum theorem."""
    return impulse / mass

def plot_force_time_graph(force, time):
    """Create a force-time graph."""
    plt.figure(figsize=(10, 6))
    plt.plot([0, time, time], [force, force, 0], 'b-')
    plt.fill_between([0, time], [force, force], alpha=0.3)
    plt.title('Force-Time Graph')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid(True)
    return plt

def main():
    st.title('Impulse Visualization')
    
    # Sidebar for input parameters
    st.sidebar.header('Simulation Parameters')
    
    # Mass input
    mass = st.sidebar.number_input(
        'Mass of Object (kg)', 
        min_value=0.1, 
        max_value=100.0, 
        value=1.0, 
        step=0.1
    )
    
    # Force input with different input methods
    input_type = st.sidebar.radio(
        'Force Input Method', 
        ['Constant Force', 'Peak Force and Duration']
    )
    
    if input_type == 'Constant Force':
        # Constant force input
        force = st.sidebar.number_input(
            'Constant Force (N)', 
            min_value=-1000.0, 
            max_value=1000.0, 
            value=10.0, 
            step=1.0
        )
        time = st.sidebar.number_input(
            'Duration (s)', 
            min_value=0.01, 
            max_value=10.0, 
            value=0.5, 
            step=0.1
        )
    else:
        # Peak force and duration input
        force = st.sidebar.number_input(
            'Peak Force (N)', 
            min_value=-1000.0, 
            max_value=1000.0, 
            value=50.0, 
            step=1.0
        )
        time = st.sidebar.number_input(
            'Force Duration (s)', 
            min_value=0.01, 
            max_value=10.0, 
            value=0.5, 
            step=0.1
        )
    
    # Calculate impulse and velocity change
    impulse = calculate_impulse(force, time)
    velocity_change = calculate_velocity_change(mass, impulse)
    
    # Display results
    st.header('Impulse Calculation Results')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('Force', f'{force} N')
    with col2:
        st.metric('Duration', f'{time} s')
    with col3:
        st.metric('Mass', f'{mass} kg')
    
    st.markdown('---')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('Impulse', f'{impulse:.2f} N·s')
    with col2:
        st.metric('Velocity Change', f'{velocity_change:.2f} m/s')
    
    # Visualize Force-Time Graph
    st.header('Force-Time Graph')
    fig = plot_force_time_graph(force, time)
    st.pyplot(fig)
    
    # Explanation section
    st.header('Understanding Impulse')
    st.markdown("""
    ### What is Impulse?
    - **Impulse** is defined as the product of force and time: Impulse = Force × Time
    - It represents the total effect of a force acting over a period of time
    - Impulse is equal to the change in momentum of an object
    
    ### Key Concepts
    - The area under a Force-Time graph represents the impulse
    - Larger impulse means a greater change in velocity
    - Impulse can be increased by either increasing force or increasing time of application
    """)

if __name__ == '__main__':
    main()