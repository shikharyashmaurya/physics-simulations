import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import matplotlib.gridspec as gridspec
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="Electromagnetic Induction Simulator",
    layout="wide"
)

# Title and description
st.title("Electromagnetic Induction Simulator")
st.markdown("""
This simulation demonstrates the principle of electromagnetic induction, where a changing magnetic field 
induces an electric current in a conductor. You can adjust various parameters to see how they affect the induced voltage.
""")

# Create two columns for controls and visualization
col1, col2 = st.columns([1, 3])

# Control parameters
with col1:
    st.subheader("Controls")
    
    # Magnet properties
    st.markdown("### Magnet Properties")
    magnet_strength = st.slider("Magnetic Field Strength (T)", 0.1, 2.0, 1.0, 0.1)
    magnet_speed = st.slider("Magnet Speed", 0.5, 3.0, 1.5, 0.1)
    magnet_direction = st.radio("Magnet Motion", ["Moving In", "Moving Out", "Oscillating"])
    
    # Coil properties
    st.markdown("### Coil Properties")
    coil_turns = st.slider("Number of Coil Turns", 5, 50, 20, 5)
    coil_radius = st.slider("Coil Radius (cm)", 2.0, 8.0, 5.0, 0.5)
    coil_resistance = st.slider("Coil Resistance (Ω)", 1.0, 20.0, 10.0, 1.0)

# Main visualization
with col2:
    st.markdown("### Simulation")
    
    # Create a placeholder for our animation
    plot_placeholder = st.empty()
    
    # Create a static visualization that updates with parameters
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    
    # Top plot: Physical setup
    ax1 = fig.add_subplot(gs[0])
    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Magnet and Coil Configuration')
    ax1.set_xlabel('Position (cm)')
    ax1.set_ylabel('Position (cm)')
    
    # Draw the coil (circle)
    coil = plt.Circle((0, 0), coil_radius, fill=False, color='black', linewidth=2)
    ax1.add_artist(coil)
    
    # Add coil turns visualization
    theta = np.linspace(0, 2*np.pi, coil_turns+1)[:-1]
    coil_points_x = coil_radius * np.cos(theta)
    coil_points_y = coil_radius * np.sin(theta)
    
    for i in range(coil_turns):
        ax1.plot(coil_points_x[i], coil_points_y[i], 'ko', markersize=3)
    
    # Initial magnet position depends on the selected motion
    if magnet_direction == "Moving In":
        magnet_pos = -9  # Start far left
    elif magnet_direction == "Moving Out":
        magnet_pos = 0  # Start at center
    else:  # Oscillating
        magnet_pos = -5  # Start slightly to the left
    
    # Draw the magnet (rectangle)
    magnet_width, magnet_height = 2, 4
    magnet = patches.Rectangle((magnet_pos-magnet_width/2, -magnet_height/2), 
                               magnet_width, magnet_height, 
                               linewidth=1, edgecolor='r', facecolor='r', alpha=0.7)
    ax1.add_patch(magnet)
    
    # Add N and S labels to the magnet
    ax1.text(magnet_pos, 1, "N", fontsize=12, ha='center', color='white', fontweight='bold')
    ax1.text(magnet_pos, -1, "S", fontsize=12, ha='center', color='white', fontweight='bold')
    
    # Add magnetic field lines
    def plot_magnetic_field(pos_x, strength):
        # Clear previous field lines
        for line in ax1.lines[:]:
            if line not in coil_points:
                ax1.lines.remove(line)
        
        # Field strength indicator by number and spread of field lines
        num_field_lines = int(strength * 5)
        
        # Field around the magnet
        for i in range(-num_field_lines, num_field_lines+1, 2):
            y_offset = i * 0.3
            
            # Field lines from N to S pole (outside the magnet)
            if abs(y_offset) > magnet_height/2:
                x = np.linspace(pos_x, pos_x, 20)
                y = np.linspace(magnet_height/2, -magnet_height/2, 20)
                ax1.plot(x, y + y_offset, 'b-', linewidth=0.7, alpha=0.6)
            
            # Field lines extending outward (further out based on strength)
            extent = 2 + strength * 3
            
            # Top field lines (from North pole)
            x_top = np.linspace(pos_x - extent, pos_x + extent, 20)
            y_top = np.zeros_like(x_top)
            y_curvature = 4 * strength * (1 - ((x_top - pos_x) / extent) ** 2)
            ax1.plot(x_top, magnet_height/2 + y_curvature, 'b-', linewidth=0.7, alpha=0.6)
            
            # Bottom field lines (from South pole)
            x_bottom = np.linspace(pos_x - extent, pos_x + extent, 20)
            y_bottom = np.zeros_like(x_bottom)
            y_curvature = 4 * strength * (1 - ((x_bottom - pos_x) / extent) ** 2)
            ax1.plot(x_bottom, -magnet_height/2 - y_curvature, 'b-', linewidth=0.7, alpha=0.6)
    
    # Store coil points reference
    coil_points = ax1.lines.copy()
    
    # Initialize magnetic field lines
    plot_magnetic_field(magnet_pos, magnet_strength)
    
    # Add a current indicator around the coil
    current_indicator = ax1.text(0, coil_radius + 1.5, "Current: 0 mA", 
                                 ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    
    # Bottom plot: Induced voltage over time
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-10, 10)
    ax2.set_title('Induced Voltage vs. Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Voltage (mV)')
    ax2.grid(True)
    
    # Initialize voltage data
    voltage_data = np.zeros(100)
    time_data = np.arange(100)
    voltage_line, = ax2.plot(time_data, voltage_data, 'g-')
    
    # Function to calculate induced voltage based on parameters
    def calculate_induced_voltage(pos, prev_pos, strength, turns, radius):
        # Flux change calculation based on position change
        area = np.pi * (radius ** 2)
        
        # Distance from coil center affects field strength (inverse square law approximation)
        distance_factor = max(0.1, 1 / (1 + abs(pos) ** 2))
        
        # Flux through coil
        current_flux = strength * area * distance_factor
        
        # Flux from previous position
        prev_distance_factor = max(0.1, 1 / (1 + abs(prev_pos) ** 2))
        previous_flux = strength * area * prev_distance_factor
        
        # Change in flux
        d_flux = current_flux - previous_flux
        
        # Induced voltage (Faraday's law: E = -N * dΦ/dt)
        # We approximate dt as 1 time unit
        induced_voltage = -turns * d_flux
        
        # Add sign based on approach/retreat
        if magnet_direction == "Moving In":
            if pos < 0:  # Approaching from left
                induced_voltage *= -1
        elif magnet_direction == "Moving Out":
            if pos > 0:  # Moving away to the right
                induced_voltage *= -1
        
        return induced_voltage
    
    # Function to simulate current direction
    def show_current_direction(voltage, ax, coil_r):
        current = voltage / coil_resistance  # I = V/R
        
        # Update current text
        current_indicator.set_text(f"Current: {current*1000:.2f} mA")
        
        # Remove any existing current direction indicators
        for artist in ax.artists:
            if hasattr(artist, 'current_indicator'):
                artist.remove()
        
        # If current is significant, show direction
        if abs(current) > 0.01:
            # Define arrow properties based on current direction
            if current > 0:
                color = 'g'
                rotation = 90  # Clockwise
            else:
                color = 'r'
                rotation = -90  # Counter-clockwise
            
            # Current magnitude affects arrow size
            arrow_size = min(1.5, max(0.5, abs(current) * 10))
            
            # Add arrow around the coil
            arrow = patches.FancyArrowPatch((-coil_r, 0), (coil_r, 0),
                                          connectionstyle=f"arc3,rad={rotation/180}",
                                          arrowstyle=f"fancy,head_width={arrow_size},head_length={arrow_size*1.5}",
                                          fc=color, ec=color, alpha=0.7)
            arrow.current_indicator = True
            arrow.set_transform(ax.transData)
            
            ax.add_patch(arrow)
    
    # Animation state variables
    animation_state = {
        'magnet_pos': magnet_pos,
        'previous_pos': magnet_pos,
        'frame_count': 0
    }
    
    def update():
        magnet_pos = animation_state['magnet_pos']
        previous_pos = animation_state['previous_pos']
        frame_count = animation_state['frame_count']
        
        # Update magnet position based on selected motion
        if magnet_direction == "Moving In":
            magnet_pos = min(0, magnet_pos + magnet_speed * 0.2)
        elif magnet_direction == "Moving Out":
            magnet_pos = min(9, magnet_pos + magnet_speed * 0.2)
        else:  # Oscillating
            magnet_pos = 5 * np.sin(frame_count * 0.1 * magnet_speed)
        
        # Update magnet position
        magnet.set_x(magnet_pos - magnet_width/2)
        
        # Update magnetic field
        plot_magnetic_field(magnet_pos, magnet_strength)
        
        # Calculate induced voltage
        induced_voltage = calculate_induced_voltage(
            magnet_pos, previous_pos, magnet_strength, coil_turns, coil_radius/10)  # Convert cm to dm
        
        # Scale for display
        display_voltage = induced_voltage * 5
        
        # Update voltage data
        voltage_data[:-1] = voltage_data[1:]
        voltage_data[-1] = display_voltage
        voltage_line.set_ydata(voltage_data)
        
        # Update current indicator
        show_current_direction(induced_voltage, ax1, coil_radius)
        
        # Update previous position for next frame
        # Update state for next frame
        animation_state['magnet_pos'] = magnet_pos
        animation_state['previous_pos'] = magnet_pos
        animation_state['frame_count'] = frame_count + 1
        # Convert plot to image
        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return f'data:image/png;base64,{img_str}'
    
    # Create a loop to update the plot repeatedly
    while True:
        img_data = update()
        plot_placeholder.image(img_data, use_column_width=True)
        # Sleep briefly to control animation speed
        import time
        time.sleep(0.1)

# Additional explanations
st.markdown("""
### How Electromagnetic Induction Works

1. **Faraday's Law**: When a magnetic field changes through a coil of wire, an electromotive force (EMF) is induced, leading to current flow if there is a complete circuit.

2. **Key Factors Affecting Induced Voltage**:
   - Magnetic field strength: Stronger fields create greater induced voltages
   - Number of coil turns: More turns create more induced voltage
   - Rate of change: Faster movement of the magnet creates higher voltage
   - Coil area: Larger coils intercept more magnetic flux

3. **Lenz's Law**: The induced current creates its own magnetic field that opposes the change that produced it.

Try moving the magnet at different speeds and directions to see how the induced voltage changes!
""")
