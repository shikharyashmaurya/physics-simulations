import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import time as pytime

def time_dilation_visualization():
    st.header("Time Dilation Visualization")
    st.markdown("""
    Explore how time changes at different velocities according to Einstein's Special Relativity.
    
    Time dilation is the phenomenon where time passes differently for objects moving at different speeds.
    """)
    
    # Velocity slider
    velocity = st.slider(
        "Velocity as a fraction of speed of light (c)", 
        min_value=0.0, 
        max_value=0.99, 
        value=0.5, 
        step=0.01
    )
    
    # Speed of light (m/s)
    c = 299792458
    
    # Calculate time dilation factor
    time_dilation_factor = 1 / np.sqrt(1 - (velocity**2))
    
    # Visualize time dilation
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Stationary Observer")
        st.write(f"Time passes normally")
        st.write(f"Time scale: 1.0")
    
    with col2:
        st.write("### Moving Object")
        st.write(f"Velocity: {velocity * 100:.2f}% of c")
        st.write(f"Time Dilation Factor: {time_dilation_factor:.4f}")
        st.write(f"Time passes slower by a factor of {time_dilation_factor:.4f}")
    
    # Visualization graph
    plt.figure(figsize=(10, 6))
    velocities = np.linspace(0, 0.99, 100)
    dilation_factors = 1 / np.sqrt(1 - (velocities**2))
    
    plt.plot(velocities * 100, dilation_factors, 'b-')
    plt.title('Time Dilation vs Velocity')
    plt.xlabel('Velocity (% of speed of light)')
    plt.ylabel('Time Dilation Factor')
    plt.grid(True)
    st.pyplot(plt)

def entropy_and_time_visualization():
    st.header("Entropy and Time's Arrow")
    st.markdown("""
    Explore how entropy relates to the perception of time's direction.
    
    The Second Law of Thermodynamics suggests that entropy (disorder) always increases, 
    giving time a distinct direction or "arrow".
    """)
    
    # Entropy simulation
    st.subheader("Entropy Simulation")
    
    # Random walk to simulate entropy increase
    steps = st.slider("Number of Steps", min_value=10, max_value=500, value=100)
    
    # Run simulation
    def entropy_walk(steps):
        position = np.zeros(steps)
        for i in range(1, steps):
            # Random step left or right
            position[i] = position[i-1] + np.random.choice([-1, 1])
        return position
    
    # Multiple walks
    plt.figure(figsize=(12, 6))
    for _ in range(5):
        walk = entropy_walk(steps)
        plt.plot(range(steps), walk)
    
    plt.title('Random Walks Demonstrating Entropy Increase')
    plt.xlabel('Time Steps')
    plt.ylabel('Position')
    st.pyplot(plt)
    
    # Entropy explanation
    st.write("""
    ### Understanding the Visualization
    - Each line represents a random walk
    - The spread of lines shows increasing disorder over time
    - This mirrors how entropy increases in physical systems
    """)

def quantum_time_visualization():
    st.header("Quantum Time Uncertainty")
    st.markdown("""
    Explore time uncertainty in quantum mechanics.
    
    In quantum mechanics, time is not as precisely defined as in classical physics.
    """)
    
    # Heisenberg Uncertainty Principle visualization
    st.subheader("Energy-Time Uncertainty")
    
    # Energy range slider
    energy_uncertainty = st.slider(
        "Energy Uncertainty (ℏ units)", 
        min_value=0.1, 
        max_value=10.0, 
        value=1.0, 
        step=0.1
    )
    
    # Calculate time uncertainty
    # Using ℏ (reduced Planck constant) = 1 for simplification
    time_uncertainty = 1 / (2 * energy_uncertainty)
    
    st.write(f"Time Uncertainty: {time_uncertainty:.4f}")
    
    # Visualization of uncertainty
    plt.figure(figsize=(10, 6))
    energies = np.linspace(0.1, 10, 100)
    times = 1 / (2 * energies)
    
    plt.plot(energies, times, 'r-')
    plt.title('Energy-Time Uncertainty Relationship')
    plt.xlabel('Energy Uncertainty (ℏ units)')
    plt.ylabel('Time Uncertainty')
    plt.grid(True)
    st.pyplot(plt)
    
    st.write("""
    ### Quantum Time Insights
    - Smaller energy uncertainties lead to larger time uncertainties
    - This demonstrates the fundamental limit of precision in quantum systems
    """)

def main():
    st.title("Physics of Time")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a Time Visualization",
        [
            "Time Dilation", 
            "Entropy and Time's Arrow", 
            "Quantum Time Uncertainty"
        ]
    )
    
    # Page routing
    if page == "Time Dilation":
        time_dilation_visualization()
    elif page == "Entropy and Time's Arrow":
        entropy_and_time_visualization()
    elif page == "Quantum Time Uncertainty":
        quantum_time_visualization()

if __name__ == "__main__":
    main()