import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_power_work_time(work, time):
    """Calculate power given work and time."""
    return work / time if time != 0 else 0

def calculate_power_force_velocity(force, velocity):
    """Calculate power given force and velocity."""
    return force * velocity

def calculate_power_torque_angular_velocity(torque, angular_velocity):
    """Calculate power given torque and angular velocity."""
    return torque * angular_velocity

def visualize_power_work_time():
    """Visualization for Power = Work / Time"""
    st.subheader("Power: Work / Time")
    
    work = st.slider("Work (Joules)", min_value=0.0, max_value=1000.0, value=50.0, step=10.0)
    time = st.slider("Time (Seconds)", min_value=0.1, max_value=60.0, value=10.0, step=0.5)
    
    power = calculate_power_work_time(work, time)
    
    st.write(f"Power = {work} J / {time} s = {power:.2f} Watts")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Bar graph showing work and time
    ax.bar(['Work (J)', 'Time (s)'], [work, time], color=['blue', 'green'])
    ax.set_ylabel('Value')
    ax.set_title('Work and Time Relationship')
    
    # Annotate power
    ax.text(0.5, max(work, time), f'Power = {power:.2f} W', 
            horizontalalignment='center', verticalalignment='bottom')
    
    st.pyplot(fig)

def visualize_power_force_velocity():
    """Visualization for Power = Force * Velocity"""
    st.subheader("Power: Force * Velocity")
    
    force = st.slider("Force (Newtons)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
    velocity = st.slider("Velocity (m/s)", min_value=0.0, max_value=20.0, value=10.0, step=0.5)
    
    power = calculate_power_force_velocity(force, velocity)
    
    st.write(f"Power = {force} N * {velocity} m/s = {power:.2f} Watts")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Scatter plot to show force and velocity
    scatter = ax.scatter([force], [velocity], c=[power], cmap='viridis', 
                         s=500, alpha=0.7)
    ax.set_xlabel('Force (N)')
    ax.set_ylabel('Velocity (m/s)')
    ax.set_title('Force and Velocity Relationship')
    
    # Colorbar to show power
    plt.colorbar(scatter, ax=ax, label='Power (W)')
    
    st.pyplot(fig)

def visualize_power_torque_angular_velocity():
    """Visualization for Power = Torque * Angular Velocity"""
    st.subheader("Power: Torque * Angular Velocity")
    
    torque = st.slider("Torque (N·m)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
    angular_velocity = st.slider("Angular Velocity (rad/s)", 
                                 min_value=0.0, max_value=20.0, value=10.0, step=0.5)
    
    power = calculate_power_torque_angular_velocity(torque, angular_velocity)
    
    st.write(f"Power = {torque} N·m * {angular_velocity} rad/s = {power:.2f} Watts")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Line plot to show power relationship
    x = np.linspace(0, torque, 100)
    y = x * angular_velocity
    
    ax.plot(x, y, label='Power Curve', color='red')
    ax.scatter([torque], [power], color='blue', s=200, label='Current Point')
    
    ax.set_xlabel('Torque (N·m)')
    ax.set_ylabel('Power (W)')
    ax.set_title('Torque and Angular Velocity Power Relationship')
    ax.legend()
    
    st.pyplot(fig)

def main():
    st.title("Power Visualization in Physics")
    
    # Introduction to Power
    st.write("""
    ### Understanding Power
    Power is the rate of doing work or the amount of energy transferred per unit time. 
    It is measured in Watts (W), which is equivalent to Joules per second (J/s).
    
    There are multiple ways to calculate power:
    1. Power = Work / Time
    2. Power = Force * Velocity
    3. Power = Torque * Angular Velocity
    """)
    
    # Visualization options
    visualization_option = st.selectbox(
        "Select Power Visualization",
        [
            "Work and Time", 
            "Force and Velocity", 
            "Torque and Angular Velocity"
        ]
    )
    
    # Select appropriate visualization based on user choice
    if visualization_option == "Work and Time":
        visualize_power_work_time()
    elif visualization_option == "Force and Velocity":
        visualize_power_force_velocity()
    else:
        visualize_power_torque_angular_velocity()

if __name__ == "__main__":
    main()