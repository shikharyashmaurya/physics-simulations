import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class FallingObject:
    def __init__(self, mass, drag_coefficient, cross_sectional_area, 
                 initial_height, initial_velocity=0, air_density=1.225):
        """
        Simulate a falling object with air resistance
        
        Parameters:
        - mass: mass of the object (kg)
        - drag_coefficient: coefficient of drag 
        - cross_sectional_area: frontal area of the object (m²)
        - initial_height: starting height of the object (m)
        - initial_velocity: initial velocity (m/s), default is 0
        - air_density: density of air (kg/m³), default is sea level air density
        """
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area
        self.height = initial_height
        self.velocity = initial_velocity
        self.air_density = air_density
        self.gravity = 9.81  # m/s²
        
    def calculate_trajectory(self, time_step=0.01, max_time=10):
        """
        Calculate the trajectory of the falling object
        
        Returns:
        - times: list of time points
        - heights: list of corresponding heights
        - velocities: list of corresponding velocities
        """
        times = [0]
        heights = [self.height]
        velocities = [self.velocity]
        
        current_time = 0
        current_height = self.height
        current_velocity = self.velocity
        
        while current_height > 0 and current_time < max_time:
            # Calculate drag force
            drag_force = 0.5 * self.drag_coefficient * self.air_density * \
                         self.cross_sectional_area * abs(current_velocity)**2
            
            # Determine drag direction (opposite to velocity)
            drag_direction = 1 if current_velocity > 0 else -1
            
            # Calculate net force
            net_force = self.mass * self.gravity - drag_direction * drag_force
            
            # Calculate acceleration
            acceleration = net_force / self.mass
            
            # Update velocity
            current_velocity += acceleration * time_step
            
            # Update height (now decreasing)
            current_height -= current_velocity * time_step
            
            # Update time
            current_time += time_step
            
            # Store results
            times.append(current_time)
            heights.append(max(0, current_height))
            velocities.append(current_velocity)
        
        return times, heights, velocities

def plot_trajectory(times, heights, velocities):
    """
    Create a matplotlib figure with two subplots
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Height vs Time plot
    ax1.plot(times, heights, label='Height')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Height (m)')
    ax1.set_title('Object Height over Time')
    ax1.invert_yaxis()  # Invert y-axis to show falling
    ax1.legend()
    ax1.grid(True)
    
    # Velocity vs Time plot
    ax2.plot(times, velocities, label='Velocity', color='r')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.set_title('Velocity over Time')
    ax2.legend()
    ax2.grid(True)
    
    return fig

def main():
    st.title('Air Resistance Simulation')
    
    # Sidebar for input parameters
    st.sidebar.header('Object Properties')
    
    # Input sliders
    mass = st.sidebar.slider('Mass (kg)', min_value=0.1, max_value=100.0, value=1.0, step=0.1)
    initial_height = st.sidebar.slider('Initial Height (m)', min_value=1, max_value=500, value=100)
    drag_coefficient = st.sidebar.slider('Drag Coefficient', min_value=0.1, max_value=2.0, value=0.47, step=0.01)
    cross_sectional_area = st.sidebar.slider('Cross-Sectional Area (m²)', 
                                             min_value=0.01, max_value=10.0, value=0.1, step=0.01)
    
    # Create falling object
    falling_object = FallingObject(
        mass=mass, 
        drag_coefficient=drag_coefficient, 
        cross_sectional_area=cross_sectional_area, 
        initial_height=initial_height
    )
    
    # Calculate trajectory
    times, heights, velocities = falling_object.calculate_trajectory()
    
    # Plot results
    fig = plot_trajectory(times, heights, velocities)
    st.pyplot(fig)
    
    # Display some key metrics
    st.subheader('Simulation Results')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('Fall Time', f'{times[-1]:.2f} s')
    
    with col2:
        st.metric('Max Velocity', f'{max(abs(v) for v in velocities):.2f} m/s')
    
    with col3:
        terminal_velocity = np.sqrt((2 * mass * 9.81) / (drag_coefficient * 1.225 * cross_sectional_area))
        st.metric('Terminal Velocity', f'{terminal_velocity:.2f} m/s')
    
    # Explanation
    st.markdown("""
    ### How Air Resistance Works
    
    This simulation demonstrates how air resistance affects a falling object:
    
    - **Drag Force**: Opposes the motion of the object through the air
    - **Factors Affecting Drag**:
      * Object's mass
      * Drag coefficient
      * Cross-sectional area
      * Air density
    
    As the object falls, air resistance increases with velocity, eventually 
    leading to terminal velocity where gravitational force equals air resistance.
    """)

if __name__ == '__main__':
    main()