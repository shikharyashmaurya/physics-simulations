import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class FrictionSimulation:
    def __init__(self):
        # Constants for simulation
        self.g = 9.8  # Acceleration due to gravity (m/s^2)
        self.mass = 10.0  # Mass of the object (kg)
        self.angle = 0.0  # Angle of the inclined plane (degrees)
        self.coefficient_static = 0.5  # Static friction coefficient
        self.coefficient_kinetic = 0.3  # Kinetic friction coefficient

    def calculate_forces(self):
        """
        Calculate forces acting on an object on an inclined plane
        """
        # Convert angle to radians
        theta = np.deg2rad(self.angle)
        
        # Normal force
        normal_force = self.mass * self.g * np.cos(theta)
        
        # Weight components
        weight_parallel = self.mass * self.g * np.sin(theta)
        weight_perpendicular = self.mass * self.g * np.cos(theta)
        
        # Maximum static friction
        max_static_friction = self.coefficient_static * normal_force
        
        # Kinetic friction
        kinetic_friction = self.coefficient_kinetic * normal_force
        
        return {
            'Normal Force': normal_force,
            'Weight Parallel': weight_parallel,
            'Weight Perpendicular': weight_perpendicular,
            'Max Static Friction': max_static_friction,
            'Kinetic Friction': kinetic_friction
        }

    def plot_force_diagram(self, forces):
        """
        Create a force diagram visualization
        """
        plt.figure(figsize=(10, 6))
        
        # Create a bar plot of forces
        force_names = list(forces.keys())
        force_values = list(forces.values())
        
        plt.bar(force_names, force_values)
        plt.title('Forces Acting on Object')
        plt.xlabel('Force Types')
        plt.ylabel('Force Magnitude (N)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return plt

def main():
    st.title('Interactive Friction Simulation')
    
    # Sidebar for inputs
    st.sidebar.header('Simulation Parameters')
    
    # Create simulation instance
    sim = FrictionSimulation()
    
    # Mass input
    sim.mass = st.sidebar.slider('Object Mass (kg)', 1.0, 50.0, 10.0, 0.5)
    
    # Angle input
    sim.angle = st.sidebar.slider('Incline Angle (degrees)', 0, 90, 30, 1)
    
    # Friction coefficients
    sim.coefficient_static = st.sidebar.slider('Static Friction Coefficient', 0.0, 1.0, 0.5, 0.01)
    sim.coefficient_kinetic = st.sidebar.slider('Kinetic Friction Coefficient', 0.0, 1.0, 0.3, 0.01)
    
    # Calculate forces
    forces = sim.calculate_forces()
    
    # Display force calculations
    st.header('Force Calculations')
    force_df = pd.DataFrame.from_dict(forces, orient='index', columns=['Force (N)'])
    st.dataframe(force_df)
    
    # Visualization of forces
    st.header('Force Diagram')
    fig = sim.plot_force_diagram(forces)
    st.pyplot(fig)
    
    # Explanation section
    st.header('Friction Explanation')
    st.markdown("""
    ### Understanding Friction on an Inclined Plane
    
    - **Normal Force**: The force perpendicular to the surface, supporting the object's weight
    - **Weight Parallel**: Component of weight pushing the object down the slope
    - **Max Static Friction**: Maximum friction force that prevents object from sliding
    - **Kinetic Friction**: Friction force when the object is moving
    
    #### When will the object start sliding?
    - If the parallel component of weight exceeds maximum static friction
    - The critical angle can be calculated using the static friction coefficient
    """)

    # Critical angle calculation
    critical_angle = np.arctan(sim.coefficient_static) * 180 / np.pi
    st.info(f"Critical Angle: {critical_angle:.2f} degrees")

if __name__ == '__main__':
    main()