import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# First Law: Inertia Visualization
def first_law_simulation():
    st.header("Newton's First Law: Law of Inertia")
    st.write("An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force.")
    
    # Simulation parameters
    friction_options = st.radio("Select Friction Condition:", 
                                ["No Friction", "With Friction"])
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 4))
    
    if friction_options == "No Friction":
        st.write("In this simulation, the object continues moving at constant velocity with no external forces.")
        # Scenario with no friction
        x = np.linspace(0, 10, 100)
        y = np.ones_like(x) * 5  # Horizontal line at constant height
        
        ax.plot(x, y, 'b-', linewidth=2)
        ax.plot(0, 5, 'ro', markersize=10)  # Object
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title("Object Moving at Constant Velocity")
        ax.set_xlabel("Distance")
        ax.set_ylabel("Position")
        
    else:
        st.write("In this simulation, friction gradually slows down the object.")
        # Scenario with friction
        x = np.linspace(0, 10, 100)
        y = np.linspace(5, 5, 100)
        
        # Declining velocity simulation
        velocities = np.linspace(1, 0, 100)
        
        ax.plot(x, y, 'b-', linewidth=2)
        point, = ax.plot(0, 5, 'ro', markersize=10)
        
        def update(frame):
            point.set_xdata(x[frame])
            return point,
        
        ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
        st.pyplot(fig)
        st.write("Note how the object slows down due to friction.")

# Second Law: Force = Mass * Acceleration
def second_law_simulation():
    st.header("Newton's Second Law: F = ma")
    st.write("The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.")
    
    # Sliders for mass and force
    mass = st.slider("Mass (kg)", 1, 10, 5)
    force = st.slider("Applied Force (N)", 1, 50, 25)
    
    # Calculate acceleration
    acceleration = force / mass
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar chart
    labels = ['Mass', 'Force', 'Acceleration']
    values = [mass, force, acceleration]
    colors = ['blue', 'green', 'red']
    
    ax.bar(labels, values, color=colors)
    ax.set_title("Relationship between Mass, Force, and Acceleration")
    ax.set_ylabel("Value")
    
    st.pyplot(fig)
    
    # Explanation
    st.write(f"With a mass of {mass} kg and a force of {force} N:")
    st.write(f"Acceleration = {force} N ÷ {mass} kg = {acceleration:.2f} m/s²")

# Third Law: Action-Reaction
def third_law_simulation():
    st.header("Newton's Third Law: Action-Reaction")
    st.write("For every action, there is an equal and opposite reaction.")
    
    # Interaction type selection
    interaction = st.selectbox("Select Interaction:", 
                               ["Rocket Propulsion", "Walking", "Collision"])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if interaction == "Rocket Propulsion":
        st.write("Rocket launches by expelling gas in the opposite direction.")
        ax.arrow(5, 5, 0, 2, head_width=0.3, head_length=0.3, fc='blue', ec='blue')
        ax.arrow(5, 5, 0, -2, head_width=0.3, head_length=0.3, fc='red', ec='red')
        ax.set_title("Rocket Propulsion: Action and Reaction Forces")
        
    elif interaction == "Walking":
        st.write("Person walks by pushing ground backward.")
        ax.arrow(4, 5, 1, 0, head_width=0.3, head_length=0.3, fc='blue', ec='blue')
        ax.arrow(6, 5, -1, 0, head_width=0.3, head_length=0.3, fc='red', ec='red')
        ax.set_title("Walking: Ground Pushes Back")
        
    else:  # Collision
        st.write("Collision between two objects with equal and opposite forces.")
        ax.arrow(3, 5, 1, 0, head_width=0.3, head_length=0.3, fc='blue', ec='blue')
        ax.arrow(7, 5, -1, 0, head_width=0.3, head_length=0.3, fc='red', ec='red')
        ax.set_title("Collision: Equal and Opposite Forces")
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    
    st.pyplot(fig)

# Main Streamlit App
def main():
    st.title("Newton's Laws of Motion Interactive Visualization")
    
    law_selection = st.sidebar.radio(
        "Select a Law to Visualize",
        ["First Law (Inertia)", 
         "Second Law (F = ma)", 
         "Third Law (Action-Reaction)"]
    )
    
    if law_selection == "First Law (Inertia)":
        first_law_simulation()
    elif law_selection == "Second Law (F = ma)":
        second_law_simulation()
    else:
        third_law_simulation()

if __name__ == "__main__":
    main()

# Instructions for running:
# 1. Save this script as newtons_laws_simulation.py
# 2. Install required libraries:
#    pip install streamlit numpy matplotlib
# 3. Run the app:
#    streamlit run newtons_laws_simulation.py