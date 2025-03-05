import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

class GravitySimulation:
    def __init__(self, num_bodies=3, width=10, height=10):
        """
        Initialize the gravity simulation
        
        Parameters:
        -----------
        num_bodies : int, optional
            Number of bodies in the simulation (default is 3)
        width : float, optional
            Width of the simulation space (default is 10)
        height : float, optional
            Height of the simulation space (default is 10)
        """
        self.num_bodies = num_bodies
        self.width = width
        self.height = height
        
        # Gravitational constant (scaled for visualization)
        self.G = 1.0
        
        # Initialize positions, velocities, and masses
        self.positions = np.random.rand(num_bodies, 2) * np.array([width, height])
        self.velocities = np.random.randn(num_bodies, 2) * 0.1
        self.masses = np.random.uniform(0.5, 2, num_bodies)
    
    def compute_accelerations(self):
        """
        Compute gravitational accelerations between bodies
        
        Returns:
        --------
        numpy.ndarray
            Accelerations for each body
        """
        accelerations = np.zeros_like(self.positions)
        
        for i in range(self.num_bodies):
            for j in range(self.num_bodies):
                if i != j:
                    # Vector from body i to body j
                    r_vector = self.positions[j] - self.positions[i]
                    
                    # Distance between bodies
                    r_magnitude = np.linalg.norm(r_vector)
                    
                    # Avoid division by zero
                    if r_magnitude > 0:
                        # Gravitational acceleration
                        acceleration_magnitude = self.G * self.masses[j] / (r_magnitude ** 2)
                        
                        # Direction of acceleration
                        acceleration = acceleration_magnitude * (r_vector / r_magnitude)
                        
                        accelerations[i] += acceleration
        
        return accelerations
    
    def update(self, dt=0.01):
        """
        Update positions and velocities using Euler integration
        
        Parameters:
        -----------
        dt : float, optional
            Time step for simulation (default is 0.01)
        """
        # Compute accelerations
        accelerations = self.compute_accelerations()
        
        # Update velocities
        self.velocities += accelerations * dt
        
        # Update positions
        self.positions += self.velocities * dt
        
        # Simple boundary conditions (bouncing off walls)
        for i in range(self.num_bodies):
            for dim in range(2):
                if (self.positions[i, dim] < 0) or (self.positions[i, dim] > [self.width, self.height][dim]):
                    self.velocities[i, dim] *= -0.9  # Damped bounce
                    self.positions[i, dim] = np.clip(self.positions[i, dim], 0, [self.width, self.height][dim])

def main():
    st.title("Gravitational N-Body Simulation")
    
    # Sidebar for simulation parameters
    st.sidebar.header("Simulation Parameters")
    
    # Number of bodies slider
    num_bodies = st.sidebar.slider("Number of Bodies", min_value=2, max_value=10, value=3)
    
    # Simulation space dimensions
    width = st.sidebar.number_input("Simulation Width", min_value=5.0, max_value=20.0, value=10.0)
    height = st.sidebar.number_input("Simulation Height", min_value=5.0, max_value=20.0, value=10.0)
    
    # Time step slider
    dt = st.sidebar.slider("Time Step", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
    
    # Create simulation
    sim = GravitySimulation(num_bodies=num_bodies, width=width, height=height)
    
    # Matplotlib figure for animation
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title("Gravitational Interaction")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    
    # Scatter plot for bodies
    scatter = ax.scatter(sim.positions[:, 0], sim.positions[:, 1], 
                         c=sim.masses, cmap='viridis', 
                         s=sim.masses*100, alpha=0.7)
    
    # Animation update function
    def update_plot(frame):
        sim.update(dt)
        scatter.set_offsets(sim.positions)
        return scatter,
    
    # Create animation
    anim = FuncAnimation(fig, update_plot, frames=200, interval=50, blit=True)
    
    # Convert animation to HTML for Streamlit
    plt.close(fig)
    
    # Display animation
    st.pyplot(fig)
    
    # Optional: Provide download of animation
    st.sidebar.header("Animation Options")
    if st.sidebar.button("Save Animation"):
        # Save animation as gif
        anim.save('gravity_simulation.gif', writer='pillow')
        with open('gravity_simulation.gif', 'rb') as f:
            st.sidebar.download_button(
                label="Download Animation",
                data=f.read(),
                file_name="gravity_simulation.gif",
                mime="image/gif"
            )
    
    # Information section
    st.markdown("## About the Simulation")
    st.markdown("""
    This simulation demonstrates gravitational interactions between multiple bodies:
    - Bodies attract each other based on their masses
    - Gravitational force is inversely proportional to the square of the distance
    - Bodies bounce off the simulation boundaries
    - Larger/darker points represent bodies with more mass
    """)

if __name__ == "__main__":
    main()