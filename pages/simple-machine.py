import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def lever_simulation():
    st.header("Lever Simulation")
    st.write("Adjust the parameters below to explore a lever system.")

    # Parameters for the lever with unique keys
    lever_length = st.slider("Lever Length (m)", min_value=1.0, max_value=5.0, value=3.0, step=0.1, key="lever_length_slider")
    pivot_position = st.slider("Pivot Position (m from left end)", min_value=0.0, max_value=lever_length, value=lever_length/2, step=0.1, key="pivot_slider")
    
    st.subheader("Left Side")
    mass_left = st.number_input("Mass on Left Side (kg)", value=1.0, min_value=0.0, key="mass_left_input")
    distance_left = st.slider("Distance from Pivot (m)", min_value=0.0, max_value=pivot_position, value=pivot_position/2, step=0.1, key="distance_left_slider")
    
    st.subheader("Right Side")
    mass_right = st.number_input("Mass on Right Side (kg)", value=1.0, min_value=0.0, key="mass_right_input")
    distance_right = st.slider("Distance from Pivot (m)", min_value=0.0, max_value=lever_length - pivot_position, value=(lever_length - pivot_position)/2, step=0.1, key="distance_right_slider")
    
    g = 9.81  # gravitational acceleration (m/s²)
    torque_left = mass_left * g * distance_left
    torque_right = mass_right * g * distance_right
    
    st.write("**Torque on Left Side:**", torque_left, "Nm")
    st.write("**Torque on Right Side:**", torque_right, "Nm")
    
    # Create a plot for the lever
    fig, ax = plt.subplots()
    # Draw lever as a horizontal line
    ax.plot([0, lever_length], [0, 0], color="black", linewidth=4)
    # Mark the pivot point
    ax.plot([pivot_position], [0], marker="o", markersize=10, color="red", label="Pivot")
    
    # Mark left mass position (to the left of pivot)
    left_mass_position = pivot_position - distance_left
    ax.plot([left_mass_position], [0], marker="o", markersize=10, color="blue", label="Left Mass")
    ax.arrow(left_mass_position, 0, 0, -0.5, head_width=0.05, head_length=0.1, fc='blue', ec='blue')
    
    # Mark right mass position (to the right of pivot)
    right_mass_position = pivot_position + distance_right
    ax.plot([right_mass_position], [0], marker="o", markersize=10, color="green", label="Right Mass")
    ax.arrow(right_mass_position, 0, 0, -0.5, head_width=0.05, head_length=0.1, fc='green', ec='green')
    
    ax.set_xlim(-0.5, lever_length + 0.5)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.set_title("Lever Diagram")
    ax.legend()
    st.pyplot(fig)

def inclined_plane_simulation():
    st.header("Inclined Plane Simulation")
    st.write("Adjust the parameters below to explore an inclined plane.")
    
    angle_deg = st.slider("Angle of Incline (degrees)", min_value=0, max_value=60, value=30, step=1, key="angle_slider")
    length = st.slider("Length of the Inclined Plane (m)", min_value=1.0, max_value=10.0, value=5.0, step=0.1, key="length_slider")
    friction_coeff = st.slider("Coefficient of Friction", min_value=0.0, max_value=1.0, value=0.2, step=0.05, key="friction_slider")
    mass_block = st.number_input("Mass of the Block (kg)", value=1.0, min_value=0.0, key="mass_block_input")
    
    angle_rad = np.deg2rad(angle_deg)
    height = length * np.sin(angle_rad)
    base = length * np.cos(angle_rad)
    
    g = 9.81
    weight = mass_block * g
    force_down = weight * np.sin(angle_rad)
    friction_force = friction_coeff * weight * np.cos(angle_rad)
    net_force = force_down - friction_force
    
    st.write("**Block Weight:**", weight, "N")
    st.write("**Component of Weight Down the Plane:**", force_down, "N")
    st.write("**Friction Force:**", friction_force, "N")
    st.write("**Net Force on Block:**", net_force, "N")
    
    # Plotting the inclined plane
    fig, ax = plt.subplots()
    x_vals = [0, base]
    y_vals = [0, height]
    ax.plot(x_vals, y_vals, color="black", linewidth=4)
    
    # Draw the block as a rotated rectangle placed halfway along the plane
    block_pos = 0.5 * length
    block_x = block_pos * np.cos(angle_rad)
    block_y = block_pos * np.sin(angle_rad)
    block_width = 0.5
    block_height = 0.3
    transform = plt.matplotlib.transforms.Affine2D().rotate_deg_around(block_x, block_y, angle_deg) + ax.transData
    block = patches.Rectangle((block_x - block_width/2, block_y - block_height/2), block_width, block_height, transform=transform, color="blue")
    ax.add_patch(block)
    
    ax.set_xlim(-1, base + 1)
    ax.set_ylim(-1, height + 1)
    ax.set_aspect("equal")
    ax.set_title("Inclined Plane Diagram")
    st.pyplot(fig)

def pulley_simulation():
    st.header("Pulley Simulation")
    st.write("This simulation visualizes a simple pulley system with two masses.")
    
    mass_left = st.number_input("Mass on Left Side (kg)", value=2.0, min_value=0.0, key="pulley_mass_left")
    mass_right = st.number_input("Mass on Right Side (kg)", value=1.0, min_value=0.0, key="pulley_mass_right")
    g = 9.81
    weight_left = mass_left * g
    weight_right = mass_right * g
    net_force = abs(weight_left - weight_right)
    total_mass = mass_left + mass_right if (mass_left + mass_right) > 0 else 1
    acceleration = net_force / total_mass
    
    st.write("**Acceleration of the System:**", acceleration, "m/s²")
    
    # Plotting the pulley system
    fig, ax = plt.subplots()
    pulley_center = (0, 0)
    pulley_radius = 0.5
    # Draw the pulley
    pulley_circle = plt.Circle(pulley_center, pulley_radius, color='black', fill=False, linewidth=3)
    ax.add_patch(pulley_circle)
    
    # Draw the ropes for both sides
    ax.plot([pulley_center[0] - pulley_radius, pulley_center[0] - pulley_radius],
            [pulley_center[1] - pulley_radius, pulley_center[1] - pulley_radius - 2],
            color="black", linewidth=2)
    ax.plot([pulley_center[0] + pulley_radius, pulley_center[0] + pulley_radius],
            [pulley_center[1] - pulley_radius, pulley_center[1] - pulley_radius - 2],
            color="black", linewidth=2)
    
    # Draw masses as rectangles
    left_rect = patches.Rectangle((pulley_center[0] - pulley_radius - 0.3, pulley_center[1] - pulley_radius - 2 - 0.3),
                                  0.6, 0.6, color="blue")
    right_rect = patches.Rectangle((pulley_center[0] + pulley_radius - 0.3, pulley_center[1] - pulley_radius - 2 - 0.3),
                                   0.6, 0.6, color="green")
    ax.add_patch(left_rect)
    ax.add_patch(right_rect)
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-5, 2)
    ax.set_aspect("equal")
    ax.set_title("Pulley Diagram")
    st.pyplot(fig)

def wheel_axle_simulation():
    st.header("Wheel and Axle Simulation")
    st.write("Adjust the parameters below to explore the wheel and axle mechanism.")
    
    wheel_radius = st.slider("Wheel Radius (m)", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key="wheel_radius_slider")
    axle_radius = st.slider("Axle Radius (m)", min_value=0.1, max_value=wheel_radius, value=0.3, step=0.05, key="axle_radius_slider")
    
    mech_adv = wheel_radius / axle_radius
    st.write("**Mechanical Advantage (Wheel Radius / Axle Radius):**", mech_adv)
    
    fig, ax = plt.subplots()
    # Draw the wheel
    wheel = plt.Circle((0, 0), wheel_radius, color='black', fill=False, linewidth=3)
    ax.add_patch(wheel)
    # Draw the axle
    axle = plt.Circle((0, 0), axle_radius, color='gray', fill=True)
    ax.add_patch(axle)
    
    ax.set_xlim(-wheel_radius-0.5, wheel_radius+0.5)
    ax.set_ylim(-wheel_radius-0.5, wheel_radius+0.5)
    ax.set_aspect("equal")
    ax.set_title("Wheel and Axle Diagram")
    st.pyplot(fig)

def wedge_simulation():
    st.header("Wedge Simulation")
    st.write("Adjust the parameters below to visualize a wedge. A wedge converts a force applied at its blunt end into forces perpendicular to its inclined surfaces.")
    
    wedge_length = st.slider("Wedge Length (m)", min_value=0.5, max_value=3.0, value=2.0, step=0.1, key="wedge_length_slider")
    wedge_height = st.slider("Wedge Height (m)", min_value=0.1, max_value=2.0, value=0.5, step=0.1, key="wedge_height_slider")
    
    fig, ax = plt.subplots()
    # Draw the wedge as a filled triangle
    triangle = np.array([[0, 0], [wedge_length, 0], [0, wedge_height]])
    ax.fill(triangle[:, 0], triangle[:, 1], color="brown", alpha=0.5)
    
    ax.set_xlim(-0.5, wedge_length + 0.5)
    ax.set_ylim(-0.5, wedge_height + 0.5)
    ax.set_aspect("equal")
    ax.set_title("Wedge Diagram")
    st.pyplot(fig)

def screw_simulation():
    st.header("Screw Simulation")
    st.write("Adjust the parameters below to visualize a screw, which is essentially an inclined plane wrapped around a cylinder.")
    
    screw_length = st.slider("Screw Length (m)", min_value=0.1, max_value=1.0, value=0.5, step=0.05, key="screw_length_slider")
    screw_diameter = st.slider("Screw Diameter (m)", min_value=0.01, max_value=0.2, value=0.05, step=0.005, key="screw_diameter_slider")
    pitch = st.slider("Pitch (distance between threads, m)", min_value=0.005, max_value=0.1, value=0.02, step=0.005, key="pitch_slider")
    
    screw_radius = screw_diameter / 2
    mech_adv = (2 * np.pi * screw_radius) / pitch
    st.write("**Mechanical Advantage:**", mech_adv)
    
    fig, ax = plt.subplots()
    # Draw the screw as a rectangle with thread lines
    rect = patches.Rectangle((0, 0), screw_length, screw_diameter, color="gray", alpha=0.3)
    ax.add_patch(rect)
    num_threads = int(screw_length / pitch)
    for i in range(num_threads):
        x_start = i * pitch
        ax.plot([x_start, x_start + pitch/2], [0, screw_diameter], color="black")
    ax.set_xlim(0, screw_length + 0.1)
    ax.set_ylim(0, screw_diameter + 0.1)
    ax.set_aspect("equal")
    ax.set_title("Screw Diagram (Side View)")
    st.pyplot(fig)

def main():
    st.title("Simple Machines Simulation")
    st.write("Explore and visualize various simple machines along with some key physics concepts behind them.")
    
    machine = st.sidebar.selectbox(
        "Select a Simple Machine",
        ["Lever", "Inclined Plane", "Pulley", "Wheel and Axle", "Wedge", "Screw"],
        key="machine_select"
    )
    
    if machine == "Lever":
        lever_simulation()
    elif machine == "Inclined Plane":
        inclined_plane_simulation()
    elif machine == "Pulley":
        pulley_simulation()
    elif machine == "Wheel and Axle":
        wheel_axle_simulation()
    elif machine == "Wedge":
        wedge_simulation()
    elif machine == "Screw":
        screw_simulation()

if __name__ == '__main__':
    main()
