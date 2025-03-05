import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

class MotionSimulation:
    def __init__(self):
        # Set up the main page
        st.title("Physics Motion Visualization")
        
        # Sidebar for motion type selection
        self.motion_type = st.sidebar.selectbox(
            "Select Motion Type",
            [
                "Uniform Motion", 
                "Uniformly Accelerated Motion", 
                "Projectile Motion", 
                "Simple Harmonic Motion",
                "Circular Motion"
            ]
        )
        
        # Call the appropriate visualization method
        if hasattr(self, self.motion_type.replace(" ", "_").lower()):
            getattr(self, self.motion_type.replace(" ", "_").lower())()
    
    def uniform_motion(self):
        """Visualize uniform motion with constant velocity"""
        st.header("Uniform Motion Simulation")
        
        # User inputs
        velocity = st.slider("Velocity (m/s)", min_value=1, max_value=20, value=5)
        time_range = st.slider("Time Range (s)", min_value=1, max_value=20, value=10)
        
        # Calculations
        time = np.linspace(0, time_range, 100)
        position = velocity * time
        
        # Plotting
        fig, ax = plt.subplots()
        ax.plot(time, position)
        ax.set_title("Position vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Position (m)")
        ax.grid(True)
        
        st.pyplot(fig)
        
        # Explanation
        st.markdown("""
        ### Uniform Motion Explanation
        - In uniform motion, the velocity remains constant
        - Position changes linearly with time
        - The graph is a straight line with slope equal to velocity
        """)
    
    def uniformly_accelerated_motion(self):
        """Visualize motion with constant acceleration"""
        st.header("Uniformly Accelerated Motion")
        
        # User inputs
        initial_velocity = st.slider("Initial Velocity (m/s)", min_value=0, max_value=10, value=0)
        acceleration = st.slider("Acceleration (m/s²)", min_value=-10, max_value=10, value=2)
        time_range = st.slider("Time Range (s)", min_value=1, max_value=20, value=10)
        
        # Calculations
        time = np.linspace(0, time_range, 100)
        position = initial_velocity * time + 0.5 * acceleration * time**2
        velocity = initial_velocity + acceleration * time
        
        # Create two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        # Position plot
        ax1.plot(time, position)
        ax1.set_title("Position vs Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Position (m)")
        ax1.grid(True)
        
        # Velocity plot
        ax2.plot(time, velocity)
        ax2.set_title("Velocity vs Time")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Velocity (m/s)")
        ax2.grid(True)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Explanation
        st.markdown("""
        ### Uniformly Accelerated Motion Explanation
        - Velocity changes linearly with time
        - Position changes quadratically with time
        - Follows equations:
          * v = v₀ + at
          * x = x₀ + v₀t + ½at²
        """)
    
    def projectile_motion(self):
        """Simulate projectile motion"""
        st.header("Projectile Motion Simulation")
        
        # User inputs
        initial_velocity = st.slider("Initial Velocity (m/s)", min_value=1, max_value=50, value=20)
        angle = st.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45)
        
        # Convert angle to radians
        theta = math.radians(angle)
        
        # Gravity constant
        g = 9.8
        
        # Calculate flight parameters
        time_of_flight = 2 * initial_velocity * math.sin(theta) / g
        max_height = (initial_velocity * math.sin(theta))**2 / (2 * g)
        range_distance = initial_velocity**2 * math.sin(2*theta) / g
        
        # Create time array
        time = np.linspace(0, time_of_flight, 100)
        
        # Calculate x and y positions
        x = initial_velocity * math.cos(theta) * time
        y = initial_velocity * math.sin(theta) * time - 0.5 * g * time**2
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y)
        ax.set_title("Projectile Motion Trajectory")
        ax.set_xlabel("Horizontal Distance (m)")
        ax.set_ylabel("Vertical Distance (m)")
        ax.grid(True)
        
        st.pyplot(fig)
        
        # Display flight parameters
        st.write(f"Time of Flight: {time_of_flight:.2f} s")
        st.write(f"Maximum Height: {max_height:.2f} m")
        st.write(f"Range: {range_distance:.2f} m")
        
        # Explanation
        st.markdown("""
        ### Projectile Motion Explanation
        - Combination of horizontal and vertical motion
        - Horizontal velocity remains constant
        - Vertical motion affected by gravity
        - Trajectory is a parabola
        """)
    
    def simple_harmonic_motion(self):
        """Simulate simple harmonic motion"""
        st.header("Simple Harmonic Motion")
        
        # User inputs
        amplitude = st.slider("Amplitude (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        frequency = st.slider("Frequency (Hz)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        
        # Calculations
        time = np.linspace(0, 10, 300)
        displacement = amplitude * np.sin(2 * np.pi * frequency * time)
        velocity = amplitude * 2 * np.pi * frequency * np.cos(2 * np.pi * frequency * time)
        acceleration = -amplitude * (2 * np.pi * frequency)**2 * np.sin(2 * np.pi * frequency * time)
        
        # Create three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))
        
        # Displacement plot
        ax1.plot(time, displacement)
        ax1.set_title("Displacement vs Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Displacement (m)")
        ax1.grid(True)
        
        # Velocity plot
        ax2.plot(time, velocity)
        ax2.set_title("Velocity vs Time")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Velocity (m/s)")
        ax2.grid(True)
        
        # Acceleration plot
        ax3.plot(time, acceleration)
        ax3.set_title("Acceleration vs Time")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Acceleration (m/s²)")
        ax3.grid(True)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Explanation
        st.markdown("""
        ### Simple Harmonic Motion Explanation
        - Oscillatory motion around an equilibrium position
        - Displacement follows a sine wave
        - Velocity follows a cosine wave
        - Acceleration follows a negative sine wave
        """)
    
    def circular_motion(self):
        """Simulate circular motion"""
        st.header("Circular Motion Simulation")
        
        # User inputs
        radius = st.slider("Radius (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        angular_velocity = st.slider("Angular Velocity (rad/s)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        
        # Calculations
        time = np.linspace(0, 10, 300)
        x = radius * np.cos(angular_velocity * time)
        y = radius * np.sin(angular_velocity * time)
        
        # Plotting
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x, y)
        ax.set_title("Circular Motion Trajectory")
        ax.set_xlabel("X Position (m)")
        ax.set_ylabel("Y Position (m)")
        ax.set_aspect('equal')
        ax.grid(True)
        
        # Draw the circle
        circle = plt.Circle((0, 0), radius, fill=False, color='r', linestyle='--')
        ax.add_artist(circle)
        
        st.pyplot(fig)
        
        # Instantaneous quantities
        st.write(f"Radius: {radius} m")
        st.write(f"Angular Velocity: {angular_velocity} rad/s")
        st.write(f"Linear Velocity: {radius * angular_velocity:.2f} m/s")
        st.write(f"Centripetal Acceleration: {(radius * angular_velocity**2):.2f} m/s²")
        
        # Explanation
        st.markdown("""
        ### Circular Motion Explanation
        - Object moves in a circular path
        - Constant speed but changing velocity direction
        - Requires centripetal acceleration towards the center
        - Angular velocity determines rotation speed
        """)

def main():
    MotionSimulation()

if __name__ == "__main__":
    main()

# How to run:
# 1. Save this script as motion_simulation.py
# 2. Install required libraries:
#    pip install streamlit numpy matplotlib
# 3. Run the simulation:
#    streamlit run motion_simulation.py