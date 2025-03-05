import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class MomentumSimulation:
    def __init__(self, mass1, velocity1, mass2, velocity2):
        """
        Initialize the momentum simulation with two objects
        """
        self.mass1 = mass1
        self.velocity1 = velocity1
        self.mass2 = mass2
        self.velocity2 = velocity2
        
    def calculate_momentum(self):
        """
        Calculate initial and final momentum
        """
        initial_momentum = self.mass1 * self.velocity1 + self.mass2 * self.velocity2
        
        # Simplified elastic collision calculation
        v1_final = ((self.mass1 - self.mass2) * self.velocity1 + 
                    2 * self.mass2 * self.velocity2) / (self.mass1 + self.mass2)
        
        v2_final = ((self.mass2 - self.mass1) * self.velocity2 + 
                    2 * self.mass1 * self.velocity1) / (self.mass1 + self.mass2)
        
        final_momentum = self.mass1 * v1_final + self.mass2 * v2_final
        
        return initial_momentum, final_momentum, v1_final, v2_final
    
    def visualize_collision(self):
        """
        Create an animation of the collision
        """
        # Create figure and axis
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle('Momentum Collision Simulation')
        
        # Initial momentum plot
        initial_momentum, final_momentum, v1_final, v2_final = self.calculate_momentum()
        
        # Before collision plot
        ax1.set_title('Before Collision')
        ax1.set_xlim(-10, 10)
        ax1.set_ylim(0, max(self.mass1, self.mass2) + 1)
        rect1 = plt.Rectangle((-5, 1), 1, self.mass1, 
                              fc='blue', label=f'Mass 1: {self.mass1} kg')
        rect2 = plt.Rectangle((5 - 1, 1), 1, self.mass2, 
                              fc='red', label=f'Mass 2: {self.mass2} kg')
        
        ax1.add_patch(rect1)
        ax1.add_patch(rect2)
        
        # Velocity annotations
        ax1.annotate(f'v1: {self.velocity1} m/s', xy=(-4.5, 0.5), 
                     xytext=(-4.5, 0.5), color='blue')
        ax1.annotate(f'v2: {self.velocity2} m/s', xy=(5.5, 0.5), 
                     xytext=(5.5, 0.5), color='red')
        
        ax1.legend()
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Mass')
        
        # After collision plot
        ax2.set_title('After Collision')
        ax2.set_xlim(-10, 10)
        ax2.set_ylim(0, max(self.mass1, self.mass2) + 1)
        rect1_final = plt.Rectangle((-5, 1), 1, self.mass1, 
                                    fc='blue', label=f'Mass 1: {self.mass1} kg')
        rect2_final = plt.Rectangle((5 - 1, 1), 1, self.mass2, 
                                    fc='red', label=f'Mass 2: {self.mass2} kg')
        
        ax2.add_patch(rect1_final)
        ax2.add_patch(rect2_final)
        
        # Final velocity annotations
        ax2.annotate(f'v1 final: {v1_final:.2f} m/s', xy=(-4.5, 0.5), 
                     xytext=(-4.5, 0.5), color='blue')
        ax2.annotate(f'v2 final: {v2_final:.2f} m/s', xy=(5.5, 0.5), 
                     xytext=(5.5, 0.5), color='red')
        
        ax2.legend()
        ax2.set_xlabel('Position (m)')
        ax2.set_ylabel('Mass')
        
        return fig

def main():
    st.title('Momentum Collision Simulator')
    
    # Sidebar for input
    st.sidebar.header('Collision Parameters')
    
    # Mass inputs
    mass1 = st.sidebar.number_input('Mass of Object 1 (kg)', 
                                    min_value=0.1, 
                                    max_value=100.0, 
                                    value=10.0)
    mass2 = st.sidebar.number_input('Mass of Object 2 (kg)', 
                                    min_value=0.1, 
                                    max_value=100.0, 
                                    value=5.0)
    
    # Velocity inputs
    velocity1 = st.sidebar.number_input('Initial Velocity of Object 1 (m/s)', 
                                        min_value=-50.0, 
                                        max_value=50.0, 
                                        value=2.0)
    velocity2 = st.sidebar.number_input('Initial Velocity of Object 2 (m/s)', 
                                        min_value=-50.0, 
                                        max_value=50.0, 
                                        value=-1.0)
    
    # Create simulation
    simulation = MomentumSimulation(mass1, velocity1, mass2, velocity2)
    
    # Calculate momentum
    initial_momentum, final_momentum, v1_final, v2_final = simulation.calculate_momentum()
    
    # Display momentum calculations
    st.subheader('Momentum Analysis')
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('Initial Momentum', f'{initial_momentum:.2f} kg·m/s')
    
    with col2:
        st.metric('Final Momentum', f'{final_momentum:.2f} kg·m/s')
    
    # Visualization
    st.subheader('Collision Visualization')
    fig = simulation.visualize_collision()
    st.pyplot(fig)
    
    # Additional explanation
    st.markdown("""
    ### Understanding Momentum
    
    **Momentum** is the product of an object's mass and velocity (p = mv). 
    In this simulation:
    - The total momentum before and after the collision remains constant (Conservation of Momentum)
    - The objects exchange velocities based on their masses
    - Positive velocity indicates movement to the right
    - Negative velocity indicates movement to the left
    """)

if __name__ == '__main__':
    main()