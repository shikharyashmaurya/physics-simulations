import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

# Set page configuration
st.set_page_config(page_title="Electric Current & Ohm's Law Simulation", 
                   page_icon="⚡", 
                   layout="wide")

# Title and introduction
st.title("⚡ Electric Current & Ohm's Law Visualization")
st.markdown("""
This interactive simulation demonstrates the fundamental principles of electric current and Ohm's Law.
Adjust the voltage and resistance values to see how they affect current flow in a circuit.

**Ohm's Law**: $V = I \\times R$, where:
- $V$ is voltage (in volts, V)
- $I$ is current (in amperes, A)
- $R$ is resistance (in ohms, Ω)
""")

# Create sidebar for controls
st.sidebar.header("Circuit Controls")

# Input widgets for voltage and resistance
voltage = st.sidebar.slider("Voltage (V)", min_value=0.0, max_value=24.0, value=12.0, step=0.1)
resistance = st.sidebar.slider("Resistance (Ω)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)

# Calculate current using Ohm's Law
if resistance > 0:
    current = voltage / resistance
else:
    current = 0  # Prevent division by zero

# Display the calculated values
st.sidebar.markdown("### Calculated Values")
st.sidebar.info(f"Current (I): {current:.2f} A")
st.sidebar.info(f"Power (P = V × I): {voltage * current:.2f} W")

# Main display area with two columns
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Circuit Visualization")
    
    # Create figure for the circuit visualization
    fig_circuit, ax_circuit = plt.subplots(figsize=(10, 6))
    
    # Draw circuit components
    # Battery
    battery_rect = patches.Rectangle((0.1, 0.4), 0.1, 0.2, fill=True, color='red')
    battery_line1 = plt.Line2D([0.1, 0.1], [0.4, 0.6], lw=2, color='black')
    battery_line2 = plt.Line2D([0.2, 0.2], [0.35, 0.65], lw=2, color='black')
    ax_circuit.add_patch(battery_rect)
    ax_circuit.add_line(battery_line1)
    ax_circuit.add_line(battery_line2)
    ax_circuit.text(0.15, 0.3, f"{voltage}V", ha='center')
    
    # Resistor
    resistor_x = 0.6
    resistor_y = 0.5
    resistor_width = 0.2
    resistor_height = 0.1
    
    resistor = patches.Rectangle((resistor_x, resistor_y - resistor_height/2), 
                                resistor_width, resistor_height, 
                                fill=True, color='#FFA500')
    ax_circuit.add_patch(resistor)
    ax_circuit.text(resistor_x + resistor_width/2, resistor_y - 0.1, 
                  f"{resistance}Ω", ha='center')
    
    # Wires
    wire1 = plt.Line2D([0.2, resistor_x], [0.5, 0.5], lw=2, color='black')
    wire2 = plt.Line2D([resistor_x + resistor_width, 0.9], [0.5, 0.5], lw=2, color='black')
    wire3 = plt.Line2D([0.9, 0.9], [0.5, 0.2], lw=2, color='black')
    wire4 = plt.Line2D([0.9, 0.1], [0.2, 0.2], lw=2, color='black')
    wire5 = plt.Line2D([0.1, 0.1], [0.2, 0.4], lw=2, color='black')
    
    ax_circuit.add_line(wire1)
    ax_circuit.add_line(wire2)
    ax_circuit.add_line(wire3)
    ax_circuit.add_line(wire4)
    ax_circuit.add_line(wire5)
    
    # Electron animation setup
    num_electrons = min(int(current * 15), 50)  # Scale number of electrons with current
    electrons_x = []
    electrons_y = []
    electron_positions = []
    
    # Initialize electron positions along the circuit path
    circuit_path = [
        # Top horizontal wire (right to left)
        [(resistor_x + resistor_width + 0.01, 0.9), (0.5, 0.5)],
        # Right vertical wire (top to bottom)
        [(0.9, 0.9), (0.9, 0.2)],
        # Bottom horizontal wire (right to left)
        [(0.9, 0.1), (0.1, 0.2)],
        # Left vertical wire (bottom to top)
        [(0.1, 0.1), (0.1, 0.4)]
    ]
    
    # Distribute electrons evenly across the circuit
    for i in range(num_electrons):
        segment = i % 4
        position = i / num_electrons
        
        start, end = circuit_path[segment]
        x = start[0] + position * (end[0] - start[0])
        y = start[1] + position * (end[1] - start[1])
        
        electrons_x.append(x)
        electrons_y.append(y)
        electron_positions.append((segment, position))
    
    electrons = ax_circuit.scatter(electrons_x, electrons_y, s=50, 
                                 color='blue', alpha=0.7, zorder=3)
    
    # Set plot limits and remove axes
    ax_circuit.set_xlim(0, 1)
    ax_circuit.set_ylim(0, 1)
    ax_circuit.axis('off')
    
    # Display the static circuit
    st.pyplot(fig_circuit)
    
    # Animated version (using streamlit animation)
    st.subheader("Animated Current Flow")
    
    # Create a placeholder for the animation
    animation_placeholder = st.empty()
    
    # Animation function
    def update_animation(frame):
        electron_speed = current / 10  # Speed proportional to current
        
        new_x = []
        new_y = []
        
        for i in range(num_electrons):
            segment, pos = electron_positions[i]
            
            # Update position
            pos += electron_speed * 0.01
            
            # If position exceeds 1, move to next segment
            if pos >= 1:
                segment = (segment + 1) % 4
                pos = pos - 1
            
            electron_positions[i] = (segment, pos)
            
            # Calculate x, y coordinates
            start, end = circuit_path[segment]
            x = start[0] + pos * (end[0] - start[0])
            y = start[1] + pos * (end[1] - start[1])
            
            new_x.append(x)
            new_y.append(y)
        
        electrons.set_offsets(np.column_stack([new_x, new_y]))
        return electrons,
    
    # Set up the animation
    ani = FuncAnimation(fig_circuit, update_animation, frames=50, 
                        interval=50, blit=True)
    
    # Display the animation (as static frames for Streamlit)
    for frame in range(30):
        update_animation(frame)
        animation_placeholder.pyplot(fig_circuit)
        
with col2:
    st.subheader("Ohm's Law Graph")
    
    # Create figure for Ohm's Law graph
    fig_graph, ax_graph = plt.subplots(figsize=(8, 6))
    
    # Plot I-V curve for current resistance
    v_values = np.linspace(0, 24, 100)
    i_values = v_values / resistance
    
    ax_graph.plot(v_values, i_values, 'b-', linewidth=2, label=f'R = {resistance}Ω')
    
    # Add current point
    ax_graph.plot(voltage, current, 'ro', markersize=10)
    ax_graph.text(voltage+0.5, current+0.1, f'({voltage}V, {current:.2f}A)', 
                fontsize=10, color='red')
    
    # Plot additional I-V curves for comparison
    comparison_resistances = [5, 20, 50]
    colors = ['g', 'm', 'c']
    
    for i, r in enumerate(comparison_resistances):
        if r != resistance:  # Skip if it's the same as current resistance
            i_values_comp = v_values / r
            ax_graph.plot(v_values, i_values_comp, f'{colors[i]}--', 
                         linewidth=1, label=f'R = {r}Ω')
    
    # Set labels and title
    ax_graph.set_xlabel('Voltage (V)', fontsize=12)
    ax_graph.set_ylabel('Current (A)', fontsize=12)
    ax_graph.set_title('I-V Curve (Ohm\'s Law)', fontsize=14)
    ax_graph.grid(True, linestyle='--', alpha=0.7)
    ax_graph.legend(loc='upper left')
    
    # Set axis limits
    ax_graph.set_xlim(0, 25)
    y_max = max(24/5, current*1.5)  # Adjust based on current value
    ax_graph.set_ylim(0, y_max)
    
    # Display the graph
    st.pyplot(fig_graph)

# Add explanatory text at the bottom
st.markdown("""
## How Ohm's Law Works

1. **Voltage (V)** is the electrical pressure that pushes electrons through a circuit, measured in volts (V).
2. **Current (I)** is the flow rate of electrons, measured in amperes (A).
3. **Resistance (R)** is the opposition to current flow, measured in ohms (Ω).

As you adjust the sliders:
- Increasing voltage while keeping resistance constant increases the current (more pressure = more flow).
- Increasing resistance while keeping voltage constant decreases the current (more resistance = less flow).
- The power (P = V × I) tells you how much energy is converted in the circuit per second.

In the animation, the blue dots represent electrons flowing through the circuit. Their speed corresponds to the current intensity.
""")

# Add a section about applications
st.markdown("""
## Real-World Applications

- **Home Electrical Systems**: Circuit breakers prevent excessive current that could cause fires.
- **Electronic Devices**: Resistors control current flow to sensitive components.
- **Power Transmission**: Engineers use Ohm's Law to design efficient power grids.
- **LED Lighting**: Current-limiting resistors protect LEDs from burning out.
- **Battery-Powered Devices**: Battery life depends on current draw, which follows Ohm's Law.
""")

# Add footer
st.markdown("---")
st.markdown("Interactive Physics Simulation | Created with Streamlit and Matplotlib")