import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
from PIL import Image

# Set page config
st.set_page_config(page_title="AC vs DC Electricity Visualization", layout="wide")

# Title and description
st.title("AC vs DC Electricity Visualization")
st.write("""
This simulation demonstrates the key differences between Alternating Current (AC) and Direct Current (DC).
- **AC**: Current periodically changes direction, voltage oscillates between positive and negative values
- **DC**: Current flows in a single direction, voltage remains constant
""")

# Sidebar controls
st.sidebar.header("Simulation Controls")

# AC parameters
st.sidebar.subheader("AC Parameters")
ac_amplitude = st.sidebar.slider("AC Amplitude (Volts)", 1.0, 10.0, 5.0, 0.1)
ac_frequency = st.sidebar.slider("AC Frequency (Hz)", 0.1, 2.0, 1.0, 0.1)

# DC parameters
st.sidebar.subheader("DC Parameters")
dc_voltage = st.sidebar.slider("DC Voltage (Volts)", 0.0, 10.0, 5.0, 0.1)

# Animation speed
animation_speed = st.sidebar.slider("Animation Speed", 0.1, 2.0, 1.0, 0.1)

# Time parameters
duration = 5  # seconds to simulate
fps = 30      # frames per second

# Function to create the simulation animation
def create_animation(ac_amplitude, ac_frequency, dc_voltage, duration, fps, animation_speed):
    # Create figure and axes
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    plt.tight_layout(pad=4.0)
    
    # Time array
    t = np.linspace(0, duration, int(duration * fps))
    dt = t[1] - t[0]
    
    # Calculate the AC and DC signals
    ac_signal = ac_amplitude * np.sin(2 * np.pi * ac_frequency * t)
    dc_signal = np.ones_like(t) * dc_voltage
    
    # Set up plots
    # Voltage plots
    ax1.set_xlim(0, duration)
    ax1.set_ylim(-max(ac_amplitude, dc_voltage) * 1.2, max(ac_amplitude, dc_voltage) * 1.2)
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Voltage vs Time')
    ax1.grid(True)
    
    ac_line, = ax1.plot([], [], 'r-', label='AC')
    dc_line, = ax1.plot([], [], 'b-', label='DC')
    ax1.legend(loc='upper right')
    
    # AC electron flow
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)
    ax2.set_aspect('equal')
    ax2.set_title('AC Electron Flow')
    ax2.grid(True)
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    # Draw a wire for AC
    wire_length = 1.8
    wire_thickness = 0.1
    wire_rect = plt.Rectangle((-wire_length/2, -wire_thickness/2), wire_length, wire_thickness, 
                             fc='gray', ec='black')
    ax2.add_patch(wire_rect)
    
    # Electrons for AC
    num_electrons = 20
    ac_electrons = []
    for i in range(num_electrons):
        electron = plt.Circle((0, 0), 0.03, fc='blue', ec='black')
        ax2.add_patch(electron)
        ac_electrons.append(electron)
    
    # DC electron flow
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect('equal')
    ax3.set_title('DC Electron Flow')
    ax3.grid(True)
    ax3.set_xticks([])
    ax3.set_yticks([])
    
    # Draw a wire for DC
    wire_rect = plt.Rectangle((-wire_length/2, -wire_thickness/2), wire_length, wire_thickness, 
                             fc='gray', ec='black')
    ax3.add_patch(wire_rect)
    
    # Electrons for DC
    dc_electrons = []
    for i in range(num_electrons):
        electron = plt.Circle((0, 0), 0.03, fc='blue', ec='black')
        ax3.add_patch(electron)
        dc_electrons.append(electron)
    
    # Initialization function for animation
    def init():
        ac_line.set_data([], [])
        dc_line.set_data([], [])
        
        # Initialize AC electrons positions
        for i, electron in enumerate(ac_electrons):
            pos = -wire_length/2 + i * wire_length / (num_electrons - 1)
            electron.center = (pos, 0)
            
        # Initialize DC electrons positions
        for i, electron in enumerate(dc_electrons):
            pos = -wire_length/2 + i * wire_length / (num_electrons - 1)
            electron.center = (pos, 0)
            
        return ac_line, dc_line, *ac_electrons, *dc_electrons
    
    # Animation function
    def animate(frame):
        frame = int(frame * animation_speed) % len(t)
        current_time = t[:frame+1]
        
        # Update voltage plots
        ac_line.set_data(current_time, ac_signal[:frame+1])
        dc_line.set_data(current_time, dc_signal[:frame+1])
        
        # Update AC electron positions
        ac_current_value = ac_signal[frame]
        ac_speed = ac_current_value / ac_amplitude  # Normalized speed factor
        
        for i, electron in enumerate(ac_electrons):
            # Base position
            base_pos = -wire_length/2 + i * wire_length / (num_electrons - 1)
            # Add oscillation based on AC signal
            oscillation = 0.05 * np.sin(2 * np.pi * ac_frequency * t[frame] - i * np.pi / 10)
            electron.center = (base_pos + oscillation, 0)
            
            # Change electron color based on direction
            if ac_current_value > 0:
                electron.set_facecolor('blue')
            else:
                electron.set_facecolor('red')
        
        # Update DC electron positions
        for i, electron in enumerate(dc_electrons):
            # Base position plus movement based on time
            pos = (-wire_length/2 + (i + frame/20 * animation_speed) % num_electrons * wire_length / num_electrons) 
            if pos > wire_length/2:
                pos = -wire_length/2
            electron.center = (pos, 0)
        
        return ac_line, dc_line, *ac_electrons, *dc_electrons
    
    # Create animation
    anim = FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True)
    
    plt.tight_layout()
    return anim, fig

# Create separate plots for static visualization instead of animation
def create_static_plots():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Time array
    t = np.linspace(0, duration, 1000)
    
    # Calculate the AC and DC signals
    ac_signal = ac_amplitude * np.sin(2 * np.pi * ac_frequency * t)
    dc_signal = np.ones_like(t) * dc_voltage
    
    # AC plot
    ax1.plot(t, ac_signal, 'r-', label=f'AC ({ac_frequency} Hz, {ac_amplitude}V)')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Alternating Current (AC)')
    ax1.grid(True)
    ax1.legend()
    
    # DC plot
    ax2.plot(t, dc_signal, 'b-', label=f'DC ({dc_voltage}V)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Voltage (V)')
    ax2.set_title('Direct Current (DC)')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    return fig

# Display static plots
st.header("Voltage Over Time")
static_fig = create_static_plots()
st.pyplot(static_fig)

# Visualize electron flow differences
st.header("Electron Flow Visualization")
st.write("""
The visualization below shows how electrons move in AC and DC circuits:
- In the AC circuit (top), electrons oscillate back and forth, changing direction periodically
- In the DC circuit (bottom), electrons flow continuously in one direction
""")

# Instead of animation, create a visual representation with multiple frames
st.write("**Animation visualization replaced with static representation**")

# Create frames to show electron movement
def create_electron_flow_images():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    # Set up axes
    for ax, title in zip([ax1, ax2], ['AC Electron Flow', 'DC Electron Flow']):
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_title(title)
        ax.grid(True)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Draw wires
        wire_length = 1.8
        wire_thickness = 0.1
        wire_rect = plt.Rectangle((-wire_length/2, -wire_thickness/2), wire_length, wire_thickness, 
                                 fc='gray', ec='black')
        ax.add_patch(wire_rect)
    
    plt.tight_layout()
    return fig

# Show different phases of electron movement
phases = ['Phase 1: Initial', 'Phase 2: Movement', 'Phase 3: Direction Change (AC only)']

for i, phase in enumerate(phases):
    st.subheader(phase)
    
    fig = create_electron_flow_images()
    num_electrons = 10
    
    # Get the axes from the figure
    ax1, ax2 = fig.axes
    
    # Draw electrons for AC
    for j in range(num_electrons):
        # Base position
        base_pos = -0.9 + j * 1.8 / (num_electrons - 1)
        
        # Different positions for different phases
        if i == 0:  # Initial phase
            pos = base_pos
            color = 'blue'
        elif i == 1:  # Movement phase
            pos = base_pos + 0.1  # Slightly moved to the right
            color = 'blue'
        else:  # Direction change (for AC)
            pos = base_pos - 0.1  # Now moved to the left
            color = 'red'  # Changed color to indicate reversed direction
            
        electron = plt.Circle((pos, 0), 0.03, fc=color, ec='black')
        ax1.add_patch(electron)
    
    # Draw electrons for DC (always moving in one direction)
    for j in range(num_electrons):
        base_pos = -0.9 + j * 1.8 / (num_electrons - 1)
        
        # Different positions for different phases, but always moving right
        if i == 0:  # Initial phase
            pos = base_pos
        elif i == 1:  # Movement phase
            pos = base_pos + 0.1  # Moved to the right
        else:  # Continued movement
            pos = base_pos + 0.2  # Moved further right
            
        # If electron moves beyond wire, wrap around
        if pos > 0.9:
            pos = -0.9 + (pos - 0.9)
            
        electron = plt.Circle((pos, 0), 0.03, fc='blue', ec='black')
        ax2.add_patch(electron)
    
    st.pyplot(fig)
    
    # Explain each phase
    if i == 0:
        st.write("Initial state: Electrons are evenly distributed along both wires.")
    elif i == 1:
        st.write("Both AC and DC electrons begin moving to the right as current flows.")
    else:
        st.write("In AC, the current reverses direction periodically (red electrons now moving left). In DC, electrons continue flowing in the same direction (wrapping around when reaching the end).")

# Explanations
st.header("Key Differences Between AC and DC")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Alternating Current (AC)")
    st.write("""
    - **Direction**: Periodically changes direction
    - **Waveform**: Typically sinusoidal
    - **Voltage**: Oscillates between positive and negative values
    - **Generation**: Produced by alternators and generators
    - **Transmission**: Can be efficiently transmitted over long distances
    - **Usage**: Power grid, household appliances, transformers
    """)

with col2:
    st.subheader("Direct Current (DC)")
    st.write("""
    - **Direction**: Flows in one direction only
    - **Waveform**: Constant (or with minimal variation)
    - **Voltage**: Maintains consistent polarity
    - **Generation**: Produced by batteries, solar cells, and power supplies
    - **Transmission**: Loses power over long distances
    - **Usage**: Electronics, batteries, LED lighting, computers
    """)

st.header("Real-World Applications")
st.write("""
- **AC** is used for power transmission and distribution systems because its voltage can be easily changed using transformers, allowing for efficient transmission over long distances.
- **DC** is used in electronic devices, mobile phones, computers, and electric vehicles because these devices require a stable, consistent current.
- Many devices convert AC to DC using adapters or power supplies. Look at your laptop charger - it converts the AC from the wall outlet to the DC your computer needs!
""")

# Advantages and disadvantages
st.header("Advantages and Disadvantages")

adv_col1, adv_col2 = st.columns(2)

with adv_col1:
    st.subheader("AC Advantages")
    st.write("""
    - Easy to transform voltage levels
    - Less energy loss in transmission
    - Easy to generate with rotating machines
    - Self-extinguishing arcs (helpful for circuit breakers)
    """)
    
    st.subheader("AC Disadvantages")
    st.write("""
    - More complex circuits needed
    - Skin effect in conductors
    - Inductive and capacitive losses
    - Not suitable for sensitive electronics without conversion
    """)

with adv_col2:
    st.subheader("DC Advantages")
    st.write("""
    - Simple to understand and use
    - Steady power delivery
    - No frequency considerations
    - Better for electronic components
    - Less dangerous at equal voltages
    """)
    
    st.subheader("DC Disadvantages")
    st.write("""
    - Difficult to change voltage levels
    - Higher transmission losses over distance
    - Cannot use transformers directly
    - Difficult to interrupt (arc issues)
    """)