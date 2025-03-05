import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def inertia_simulation():
    st.title('Inertia Visualization Simulation')
    
    # Sidebar controls
    st.sidebar.header('Simulation Parameters')
    
    # Object mass
    mass = st.sidebar.slider('Object Mass (kg)', min_value=1, max_value=25, value=10)
    
    # Initial velocity
    initial_velocity = st.sidebar.slider('Initial Velocity (m/s)', min_value=0, max_value=20, value=10)
    
    # Friction coefficient
    friction = st.sidebar.slider('Friction Coefficient', min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    
    # Explanation
    st.markdown("""
    ## Understanding Inertia
    
    Inertia is an object's resistance to change in its state of motion. 
    This simulation shows how:
    - Heavier objects maintain their motion longer
    - Friction gradually reduces an object's speed
    - Objects tend to continue moving unless stopped
    """)
    
    # Simulation calculations
    def calculate_motion(mass, initial_velocity, friction, time):
    # Gravitational acceleration
        g = 9.8
        
        # Deceleration due to friction
        deceleration = friction * g *mass
        
        # Calculate position and velocity
        if time <= initial_velocity / deceleration:
            # Object is still moving forward
            position = initial_velocity * time - 0.5 * deceleration * time**2
            velocity = initial_velocity - deceleration * time
        else:
            # Object has come to a stop
            # Find the time when object stops
            stop_time = initial_velocity / deceleration
            
            # Calculate final position
            final_position = initial_velocity * stop_time - 0.5 * deceleration * stop_time**2
            
            # Position after stopping point remains constant
            position = final_position
            velocity = 0
        
        return position, velocity
    
    # Prepare plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Time array
    time = np.linspace(0, 5, 100)
    
    # Calculate motion
    positions = []
    velocities = []
    for t in time:
        pos, vel = calculate_motion(mass, initial_velocity, friction, t)
        positions.append(pos)
        velocities.append(vel)
    
    # Position plot
    ax1.plot(time, positions, label='Position')
    ax1.set_title(f'Position over Time (Mass: {mass} kg)')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Distance (m)')
    ax1.legend()
    ax1.grid(True)
    
    # Velocity plot
    ax2.plot(time, velocities, label='Velocity', color='red')
    ax2.set_title(f'Velocity over Time (Initial Velocity: {initial_velocity} m/s)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.legend()
    ax2.grid(True)
    
    # Adjust layout and display
    plt.tight_layout()
    st.pyplot(fig)
    
    # Detailed explanation
    st.markdown(f"""
    ### Simulation Details
    - **Mass of Object:** {mass} kg
    - **Initial Velocity:** {initial_velocity} m/s
    - **Friction Coefficient:** {friction}
    
    #### Observation
    The graphs show how:
    1. Position changes over time (distance traveled)
    2. Velocity decreases due to friction
    """)



# Streamlit page configuration
if __name__ == '__main__':
    # Run the simulation
    inertia_simulation()