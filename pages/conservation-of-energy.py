import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class EnergyConservationSimulation:
    def __init__(self, mass=1.0, gravity=9.8, initial_height=10.0):
        """
        Initialize the simulation parameters
        
        :param mass: Mass of the object (kg)
        :param gravity: Acceleration due to gravity (m/s^2)
        :param initial_height: Starting height of the object (m)
        """
        self.mass = mass
        self.gravity = gravity
        self.initial_height = initial_height
        
    def calculate_energies(self):
        """
        Calculate potential and kinetic energies at different heights
        
        :return: Tuple of lists (heights, potential_energies, kinetic_energies, total_energies)
        """
        # Create array of heights from initial height to 0
        heights = np.linspace(0, self.initial_height, 100)
        
        # Calculate potential energy at each height
        potential_energies = self.mass * self.gravity * heights
        
        # Calculate kinetic energy at each height (using conservation of energy principle)
        kinetic_energies = self.mass * self.gravity * self.initial_height - potential_energies
        
        # Total energy remains constant
        total_energies = np.full_like(heights, self.mass * self.gravity * self.initial_height)
        
        return heights, potential_energies, kinetic_energies, total_energies
    
    def create_energy_plot(self):
        """
        Create a matplotlib figure showing energy transformations
        
        :return: matplotlib figure
        """
        # Calculate energies
        heights, pe, ke, te = self.calculate_energies()
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot the energy curves
        ax.plot(heights, pe, label='Potential Energy', color='blue')
        ax.plot(heights, ke, label='Kinetic Energy', color='red')
        ax.plot(heights, te, label='Total Energy', color='green', linestyle='--')
        
        # Customize the plot
        ax.set_title('Conservation of Energy: Energy vs Height', fontsize=15)
        ax.set_xlabel('Height (m)', fontsize=12)
        ax.set_ylabel('Energy (J)', fontsize=12)
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.7)
        
        return fig

def main():
    # Streamlit app title and description
    st.title('Conservation of Energy Simulation')
    st.write("""
    ## Exploring Energy Transformations
    
    This interactive simulation demonstrates the principle of Conservation of Energy 
    for a falling object. As the object falls:
    - Potential Energy decreases
    - Kinetic Energy increases
    - Total Energy remains constant
    """)
    
    # Sidebar for simulation parameters
    st.sidebar.header('Simulation Parameters')
    
    # Mass input
    mass = st.sidebar.slider('Mass of Object (kg)', 
                             min_value=0.1, 
                             max_value=10.0, 
                             value=1.0, 
                             step=0.1)
    
    # Initial height input
    initial_height = st.sidebar.slider('Initial Height (m)', 
                                       min_value=1.0, 
                                       max_value=20.0, 
                                       value=10.0, 
                                       step=0.5)
    
    # Gravity (with option to modify)
    gravity = st.sidebar.number_input('Gravity (m/s²)', 
                                      min_value=0.1, 
                                      max_value=20.0, 
                                      value=9.8, 
                                      step=0.1)
    
    # Create simulation instance
    sim = EnergyConservationSimulation(
        mass=mass, 
        gravity=gravity, 
        initial_height=initial_height
    )
    
    # Generate and display the plot
    fig = sim.create_energy_plot()
    st.pyplot(fig)
    
    # Additional information section
    st.markdown("### Key Insights")
    st.markdown("""
    - 🔵 Blue Line: Potential Energy - Decreases as height decreases
    - 🔴 Red Line: Kinetic Energy - Increases as height decreases
    - 🟢 Green Dashed Line: Total Energy - Remains constant
    
    The simulation shows how energy is transformed from potential to kinetic 
    energy while maintaining a constant total energy.
    """)
    
    # Calculate and display some specific values
    heights, pe, ke, te = sim.calculate_energies()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Potential Energy", f"{pe[0]:.2f} J")
    with col2:
        st.metric("Final Kinetic Energy", f"{ke[-1]:.2f} J")
    with col3:
        st.metric("Total Energy", f"{te[0]:.2f} J")

if __name__ == "__main__":
    main()