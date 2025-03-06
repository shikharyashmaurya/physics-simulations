import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Lenz's Law Visual Simulation")

# --- Simulation Controls ---
st.header("Simulation Controls")
magnet_position = st.slider("Magnet Position", -5.0, 5.0, 0.0, step=0.1,
                           help="Control the horizontal position of the magnet.")
magnet_velocity = st.slider("Magnet Velocity (for change visualization)", -1.0, 1.0, 0.0, step=0.1,
                            help="Simulate magnet velocity to show change in flux (for visualization purposes only). A positive velocity means magnet is moving right, negative velocity means left.")
show_field_lines = st.checkbox("Show Magnetic Field Lines", value=True)
show_induced_current = st.checkbox("Show Induced Current", value=True)
show_forces = st.checkbox("Show Forces", value=True)

# --- Plotting Area ---
plot_placeholder = st.empty()  # Placeholder for the plot

def draw_magnet(ax, x_magnet, magnet_width=1.0, magnet_height=0.5):
    """Draws the magnet on the plot."""
    y_center = 0
    ax.add_patch(plt.Rectangle((x_magnet - magnet_width / 2, y_center - magnet_height / 2), magnet_width, magnet_height,
                                facecolor='red', edgecolor='black'))
    ax.text(x_magnet - magnet_width / 4, y_center, 'N', color='white', ha='center', va='center', fontweight='bold')
    ax.text(x_magnet + magnet_width / 4, y_center, 'S', color='white', ha='center', va='center', fontweight='bold')

def draw_coil(ax, coil_x_center=0, coil_width=1.5, coil_height=1.0):
    """Draws the coil on the plot."""
    y_center = 0
    ax.add_patch(plt.Rectangle((coil_x_center - coil_width / 2, y_center - coil_height / 2), coil_width, coil_height,
                                facecolor='lightgray', edgecolor='black'))
    ax.text(coil_x_center, y_center, 'Coil', color='black', ha='center', va='center')

def draw_magnetic_field_magnet(ax, x_magnet, field_strength=0.5, num_lines=15):
    """Draws simplified magnetic field lines from the magnet."""
    y_center = 0
    start_x = x_magnet - 0.5  # Approximate North pole position for field lines
    end_x = x_magnet + 0.5    # Approximate South pole position

    for i in range(num_lines):
        y_offset = (i - num_lines // 2) * 0.2 * field_strength
        if y_offset != 0: # Avoid drawing lines exactly on top of each other which can cause issues
            ax.plot([start_x, end_x], [y_center + 0.2 + y_offset, y_center + 0.2 - y_offset], color='blue', linewidth=0.5, alpha=0.7) # Lines above
            ax.plot([start_x, end_x], [y_center - 0.2 + y_offset, y_center - 0.2 - y_offset], color='blue', linewidth=0.5, alpha=0.7) # Lines below

def draw_induced_current(ax, coil_x_center, magnet_velocity):
    """Draws arrows indicating induced current direction based on magnet velocity."""
    y_center = 0
    current_direction = 0  # 0: No current, 1: Clockwise, -1: Counter-clockwise

    if magnet_velocity > 0.1: # Magnet moving right (towards coil)
        current_direction = 1 # Clockwise to oppose increasing flux into the page (assuming field is into the page when N pole approaches)
    elif magnet_velocity < -0.1: # Magnet moving left (away from coil)
        current_direction = -1 # Counter-clockwise to oppose decreasing flux into the page

    if current_direction == 1: # Clockwise
        ax.arrow(coil_x_center + 0.3, y_center + 0.4, 0, -0.3, head_width=0.1, head_length=0.1, fc='green', ec='green')
        ax.arrow(coil_x_center - 0.3, y_center - 0.4, 0, 0.3, head_width=0.1, head_length=0.1, fc='green', ec='green')
        ax.text(coil_x_center, y_center + 0.6, "Induced Current (Clockwise)", color='green', ha='center', va='center')
    elif current_direction == -1: # Counter-clockwise
        ax.arrow(coil_x_center + 0.3, y_center - 0.4, 0, 0.3, head_width=0.1, head_length=0.1, fc='green', ec='green')
        ax.arrow(coil_x_center - 0.3, y_center + 0.4, 0, -0.3, head_width=0.1, head_length=0.1, fc='green', ec='green')
        ax.text(coil_x_center, y_center + 0.6, "Induced Current (Counter-Clockwise)", color='green', ha='center', va='center')
    else:
        ax.text(coil_x_center, y_center + 0.6, "No Induced Current", color='gray', ha='center', va='center')


def draw_force_arrow(ax, x_magnet, magnet_velocity):
    """Draws force arrows indicating repulsion or attraction based on Lenz's Law."""
    force_direction = 0 # 0: No force, 1: Repulsion (away from coil), -1: Attraction (towards coil)

    if magnet_velocity > 0.1: # Moving towards coil - Repulsion
        force_direction = 1
    elif magnet_velocity < -0.1: # Moving away from coil - Attraction
        force_direction = -1

    if force_direction == 1: # Repulsion - Force on Magnet to the Left
        ax.arrow(x_magnet, 1.0, -0.5, 0, head_width=0.1, head_length=0.2, fc='purple', ec='purple')
        ax.text(x_magnet - 0.25, 1.2, "Repulsive Force", color='purple', ha='center', va='center')
    elif force_direction == -1: # Attraction - Force on Magnet to the Right
        ax.arrow(x_magnet, 1.0, 0.5, 0, head_width=0.1, head_length=0.2, fc='purple', ec='purple')
        ax.text(x_magnet + 0.25, 1.2, "Attractive Force", color='purple', ha='center', va='center')
    else:
        ax.text(x_magnet, 1.2, "No Force", color='gray', ha='center', va='center')


# --- Main Plot Update Function ---
def update_plot(magnet_position, magnet_velocity, show_field_lines, show_induced_current, show_forces):
    """Updates the plot based on slider values and checkboxes."""
    fig, ax = plt.subplots()
    ax.set_xlim([-6, 6])
    ax.set_ylim([-2, 2])
    ax.set_aspect('equal') # Ensure circle is drawn as circle
    ax.axis('off') # Hide axes

    draw_coil(ax)
    draw_magnet(ax, magnet_position)

    if show_field_lines:
        draw_magnetic_field_magnet(ax, magnet_position)

    if show_induced_current:
        draw_induced_current(ax, 0, magnet_velocity) # Coil is at x=0

    if show_forces:
        draw_force_arrow(ax, magnet_position, magnet_velocity)

    plot_placeholder.pyplot(fig) # Update the plot in Streamlit

# --- Run the simulation and update plot on slider change ---
update_plot(magnet_position, magnet_velocity, show_field_lines, show_induced_current, show_forces)