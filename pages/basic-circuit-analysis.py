import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

st.set_page_config(page_title="Circuit Analysis Simulator", layout="wide")

st.title("Interactive Circuit Analysis Simulator")
st.write("Explore basic circuit concepts including Ohm's Law, series and parallel circuits.")

# Sidebar for navigation
page = st.sidebar.radio("Choose a Simulation", 
                        ["Ohm's Law", "Series Circuit", "Parallel Circuit"])

if page == "Ohm's Law":
    st.header("Ohm's Law: V = I × R")
    st.write("""
    Ohm's Law describes the relationship between voltage (V), current (I), and resistance (R).
    Adjust the sliders to see how changing one parameter affects the others.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Let user control two of the variables and calculate the third
        calculation_mode = st.radio(
            "What do you want to calculate?",
            ["Voltage", "Current", "Resistance"]
        )
        
        if calculation_mode == "Voltage":
            current = st.slider("Current (A)", 0.1, 10.0, 1.0, 0.1)
            resistance = st.slider("Resistance (Ω)", 1.0, 100.0, 10.0, 1.0)
            voltage = current * resistance
            st.success(f"Calculated Voltage: {voltage:.2f} V")
        
        elif calculation_mode == "Current":
            voltage = st.slider("Voltage (V)", 1.0, 220.0, 12.0, 1.0)
            resistance = st.slider("Resistance (Ω)", 1.0, 100.0, 10.0, 1.0)
            current = voltage / resistance if resistance != 0 else float('inf')
            st.success(f"Calculated Current: {current:.2f} A")
        
        else:  # Resistance
            voltage = st.slider("Voltage (V)", 1.0, 220.0, 12.0, 1.0)
            current = st.slider("Current (A)", 0.1, 10.0, 1.0, 0.1)
            resistance = voltage / current if current != 0 else float('inf')
            st.success(f"Calculated Resistance: {resistance:.2f} Ω")
    
    with col2:
        # Create visualization
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Draw battery
        battery_height = 1.5
        battery_x = 1
        battery_y = 3
        
        # Long line
        ax.plot([battery_x, battery_x + 6], [battery_y + battery_height, battery_y + battery_height], 'k-', lw=2)
        # Bottom line
        ax.plot([battery_x, battery_x + 6], [battery_y, battery_y], 'k-', lw=2)
        
        # Battery
        ax.plot([battery_x, battery_x], [battery_y, battery_y + battery_height], 'k-', lw=2)
        ax.plot([battery_x + 0.2, battery_x + 0.2], [battery_y + 0.25, battery_y + battery_height - 0.25], 'k-', lw=4)
        ax.plot([battery_x + 0.5, battery_x + 0.5], [battery_y + 0.5, battery_y + battery_height - 0.5], 'k-', lw=2)
        
        # Resistor (zigzag)
        res_x = battery_x + 3
        res_y = battery_y + battery_height
        zigzag_width = 1.5
        zigzag_height = 0.5
        zigzag_pts = 7
        x_pts = np.linspace(res_x, res_x + zigzag_width, zigzag_pts)
        y_pts = np.array([0, 1, 0, 1, 0, 1, 0]) * zigzag_height + res_y
        ax.plot(x_pts, y_pts, 'k-', lw=2)
        
        # Add current direction arrow
        if calculation_mode == "Current" or calculation_mode == "Resistance":
            current_value = current
        else:
            current_value = current
        
        # Scale arrow size based on current
        arrow_scale = min(1, current_value / 5)
        arrow_width = 0.15 * (0.5 + arrow_scale)
        arrow = FancyArrowPatch((battery_x + 4.5, battery_y + 0.5), 
                              (battery_x + 3, battery_y + 0.5), 
                              arrowstyle='->', 
                              color='blue', 
                              lw=2,
                              mutation_scale=20)
        ax.add_patch(arrow)
        ax.text(battery_x + 3.8, battery_y + 0.3, f"{current:.1f} A", color='blue')
        
        # Add voltage label
        if calculation_mode == "Voltage" or calculation_mode == "Resistance":
            voltage_value = voltage
        else:
            voltage_value = voltage
            
        ax.text(battery_x + 0.7, battery_y + 0.75, f"{voltage:.1f} V", color='red')
        
        # Add resistance label
        if calculation_mode == "Resistance" or calculation_mode == "Voltage":
            resistance_value = resistance
        else:
            resistance_value = resistance
            
        ax.text(res_x + 0.2, res_y + 0.75, f"{resistance:.1f} Ω", color='green')
        
        ax.set_xlim(0, 8)
        ax.set_ylim(1, 6)
        ax.axis('equal')
        ax.axis('off')
        
        st.pyplot(fig)
        
        # Show the formula and calculation
        st.write("### Ohm's Law Formula")
        if calculation_mode == "Voltage":
            st.latex(r"V = I \times R")
            st.latex(f"V = {current:.2f} \, A \times {resistance:.2f} \, \Omega = {voltage:.2f} \, V")
        elif calculation_mode == "Current":
            st.latex(r"I = \frac{V}{R}")
            st.latex(f"I = \\frac{{{voltage:.2f} \, V}}{{{resistance:.2f} \, \Omega}} = {current:.2f} \, A")
        else:  # Resistance
            st.latex(r"R = \frac{V}{I}")
            st.latex(f"R = \\frac{{{voltage:.2f} \, V}}{{{current:.2f} \, A}} = {resistance:.2f} \, \Omega")

elif page == "Series Circuit":
    st.header("Series Circuit Analysis")
    st.write("""
    In a series circuit, the same current flows through each component, and the total voltage is the sum of the voltages across each component.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # User inputs
        voltage_source = st.slider("Voltage Source (V)", 1.0, 24.0, 12.0, 0.1)
        
        st.subheader("Resistors in Series")
        num_resistors = st.slider("Number of Resistors", 1, 5, 3)
        
        resistances = []
        for i in range(num_resistors):
            r = st.slider(f"R{i+1} (Ω)", 1.0, 100.0, 10.0 * (i+1), 1.0, key=f"series_r{i}")
            resistances.append(r)
        
        # Calculations
        total_resistance = sum(resistances)
        current = voltage_source / total_resistance if total_resistance > 0 else 0
        voltage_drops = [current * r for r in resistances]
        power_dissipations = [current**2 * r for r in resistances]
        
        st.subheader("Circuit Analysis Results")
        st.write(f"Total Resistance: {total_resistance:.2f} Ω")
        st.write(f"Current: {current:.2f} A")
        
        # Display voltage drops and power for each resistor
        for i in range(num_resistors):
            st.write(f"R{i+1}: Voltage Drop = {voltage_drops[i]:.2f} V, Power = {power_dissipations[i]:.2f} W")
    
    with col2:
        # Create visualization of series circuit
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Draw circuit
        start_x, start_y = 1, 5
        
        # Draw battery
        battery_height = 1.5
        battery_x = start_x
        battery_y = start_y - battery_height/2
        
        # Battery
        ax.plot([battery_x, battery_x], [battery_y, battery_y + battery_height], 'k-', lw=2)
        ax.plot([battery_x + 0.2, battery_x + 0.2], [battery_y + 0.25, battery_y + battery_height - 0.25], 'k-', lw=4)
        ax.plot([battery_x + 0.5, battery_x + 0.5], [battery_y + 0.5, battery_y + battery_height - 0.5], 'k-', lw=2)
        
        # Label voltage source
        ax.text(battery_x + 0.7, battery_y + 0.75, f"{voltage_source:.1f} V", color='red')
        
        # Draw wires and resistors in series
        line_length = 10 / (num_resistors + 1)
        
        # Top line from battery to first resistor
        ax.plot([battery_x + 0.5, battery_x + line_length], [battery_y + battery_height - 0.5, battery_y + battery_height - 0.5], 'k-', lw=2)
        
        # Draw resistors in series
        for i in range(num_resistors):
            res_x = battery_x + line_length * (i + 1)
            res_y = battery_y + battery_height - 0.5
            
            # Draw resistor (zigzag)
            zigzag_width = 1.0
            zigzag_height = 0.5
            zigzag_pts = 7
            x_pts = np.linspace(res_x, res_x + zigzag_width, zigzag_pts)
            y_pts = np.array([0, 1, 0, 1, 0, 1, 0]) * zigzag_height + res_y
            ax.plot(x_pts, y_pts, 'k-', lw=2)
            
            # Label resistor
            ax.text(res_x + 0.2, res_y + 0.8, f"R{i+1}\n{resistances[i]:.1f}Ω\n{voltage_drops[i]:.1f}V", fontsize=8)
            
            # Connect to next resistor if not the last one
            if i < num_resistors - 1:
                ax.plot([res_x + zigzag_width, res_x + line_length], [res_y, res_y], 'k-', lw=2)
        
        # Bottom line back to battery
        ax.plot([battery_x + line_length * (num_resistors + 1) - line_length + zigzag_width, battery_x + 0.5], 
                [res_y, battery_y + 0.5], 'k-', lw=2)
        
        # Add current direction arrow
        arrow = FancyArrowPatch((battery_x + 0.5, battery_y + 0.5), 
                              (battery_x + line_length/2, battery_y + 0.5), 
                              arrowstyle='->', 
                              color='blue', 
                              lw=2,
                              mutation_scale=15)
        ax.add_patch(arrow)
        ax.text(battery_x + line_length/4, battery_y + 0.2, f"{current:.1f}A", color='blue', fontsize=9)
        
        ax.set_xlim(0, 12)
        ax.set_ylim(2, 8)
        ax.axis('equal')
        ax.axis('off')
        
        st.pyplot(fig)
        
        # Show formulas
        st.write("### Series Circuit Formulas")
        st.latex(r"R_{total} = R_1 + R_2 + ... + R_n")
        st.latex(f"R_{{total}} = {' + '.join([f'{r:.1f}' for r in resistances])} = {total_resistance:.2f} \, \Omega")
        st.latex(r"I = \frac{V_{source}}{R_{total}}")
        st.latex(f"I = \\frac{{{voltage_source:.2f}}}{{{total_resistance:.2f}}} = {current:.2f} \, A")
        st.latex(r"V_n = I \times R_n")

elif page == "Parallel Circuit":
    st.header("Parallel Circuit Analysis")
    st.write("""
    In a parallel circuit, each component has the same voltage across it, and the total current is the sum of the currents through each path.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # User inputs
        voltage_source = st.slider("Voltage Source (V)", 1.0, 24.0, 12.0, 0.1)
        
        st.subheader("Resistors in Parallel")
        num_resistors = st.slider("Number of Resistors", 1, 5, 3)
        
        resistances = []
        for i in range(num_resistors):
            r = st.slider(f"R{i+1} (Ω)", 1.0, 100.0, float(10.0 * (i+1)), 1.0, key=f"parallel_r{i}")
            resistances.append(r)
        
        # Calculations
        inverse_resistance_sum = sum(1/r for r in resistances) if resistances else 0
        total_resistance = 1/inverse_resistance_sum if inverse_resistance_sum > 0 else float('inf')
        
        branch_currents = [voltage_source / r for r in resistances]
        total_current = sum(branch_currents)
        power_dissipations = [(voltage_source ** 2) / r for r in resistances]
        total_power = voltage_source * total_current
        
        st.subheader("Circuit Analysis Results")
        st.write(f"Total Resistance: {total_resistance:.2f} Ω")
        st.write(f"Total Current: {total_current:.2f} A")
        
        # Display current and power for each resistor
        for i in range(num_resistors):
            st.write(f"R{i+1}: Current = {branch_currents[i]:.2f} A, Power = {power_dissipations[i]:.2f} W")
    
    with col2:
        # Create visualization of parallel circuit
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Draw circuit
        start_x, start_y = 1, 5
        end_x = 9
        
        # Draw battery
        battery_height = 1.5
        battery_x = start_x
        battery_y = start_y - battery_height/2
        
        # Battery
        ax.plot([battery_x, battery_x], [battery_y, battery_y + battery_height], 'k-', lw=2)
        ax.plot([battery_x + 0.2, battery_x + 0.2], [battery_y + 0.25, battery_y + battery_height - 0.25], 'k-', lw=4)
        ax.plot([battery_x + 0.5, battery_x + 0.5], [battery_y + 0.5, battery_y + battery_height - 0.5], 'k-', lw=2)
        
        # Label voltage source
        ax.text(battery_x + 0.7, battery_y + 0.75, f"{voltage_source:.1f} V", color='red')
        
        # Top horizontal line
        ax.plot([battery_x + 0.5, end_x], [battery_y + battery_height - 0.5, battery_y + battery_height - 0.5], 'k-', lw=2)
        
        # Bottom horizontal line
        ax.plot([battery_x + 0.5, end_x], [battery_y + 0.5, battery_y + 0.5], 'k-', lw=2)
        
        # Add main current arrow
        arrow = FancyArrowPatch((battery_x + 1.5, battery_y + battery_height - 0.5), 
                              (battery_x + 2.5, battery_y + battery_height - 0.5), 
                              arrowstyle='->', 
                              color='blue', 
                              lw=2,
                              mutation_scale=15)
        ax.add_patch(arrow)
        ax.text(battery_x + 1.5, battery_y + battery_height - 0.8, f"{total_current:.1f}A", color='blue')
        
        # Draw resistors in parallel
        spacing = 5.0 / (num_resistors + 1)
        for i in range(num_resistors):
            res_x = battery_x + 2.5 + i * spacing
            res_y_top = battery_y + battery_height - 0.5
            res_y_bottom = battery_y + 0.5
            
            # Vertical lines to resistor
            ax.plot([res_x, res_x], [res_y_top, res_y_top - 1], 'k-', lw=2)
            ax.plot([res_x, res_x], [res_y_bottom, res_y_bottom + 1], 'k-', lw=2)
            
            # Draw resistor (zigzag horizontal)
            zigzag_height = 1.0
            zigzag_width = 0.5
            zigzag_pts = 7
            y_pts = np.linspace(res_y_top - 1, res_y_bottom + 1, zigzag_pts)
            x_pts = np.array([0, 1, 0, 1, 0, 1, 0]) * zigzag_width + res_x
            ax.plot(x_pts, y_pts, 'k-', lw=2)
            
            # Branch current arrow
            branch_arrow = FancyArrowPatch((res_x - 0.3, res_y_top - 0.5), 
                                        (res_x - 0.3, res_y_top - 1.5), 
                                        arrowstyle='->', 
                                        color='blue', 
                                        lw=2,
                                        mutation_scale=15)
            ax.add_patch(branch_arrow)
            
            # Label resistor and current
            ax.text(res_x + 0.6, res_y_top - 1.5, f"R{i+1}\n{resistances[i]:.1f}Ω\n{branch_currents[i]:.2f}A", fontsize=8)
        
        ax.set_xlim(0, 12)
        ax.set_ylim(2, 8)
        ax.axis('equal')
        ax.axis('off')
        
        st.pyplot(fig)
        
        # Show formulas
        st.write("### Parallel Circuit Formulas")
        st.latex(r"\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2} + ... + \frac{1}{R_n}")
        
        # Create the fractions part without f-strings
        fractions_parts = []
        for r in resistances:
            fractions_parts.append(r"\frac{1}{" + f"{r:.1f}" + "}")
        fractions_text = " + ".join(fractions_parts)
        
        st.latex(r"\frac{1}{R_{total}} = " + fractions_text + f" = {inverse_resistance_sum:.4f}")
        st.latex(r"R_{total} = \frac{1}{" + f"{inverse_resistance_sum:.4f}" + r"} = " + f"{total_resistance:.2f} \, \Omega")
        st.latex(r"I_{total} = I_1 + I_2 + ... + I_n")
        st.latex(f"I_{{total}} = {' + '.join([f'{i:.2f}' for i in branch_currents])} = {total_current:.2f} \, A")
        st.latex(r"I_n = \frac{V}{R_n}")

st.sidebar.markdown('''File "D:\projects\physics-simulations\pages\basic-circuit-analysis.py", line 359
              fractions_parts.append(r""\frac{1}{""" + f"{r:.1f}" + r""}""")
                                                                           ^
SyntaxError: unexpected character after line continuation character
### Basic Circuit Concepts

**Ohm's Law:** V = IR  
- V: Voltage (Volts)
- I: Current (Amperes)
- R: Resistance (Ohms)

**Series Circuit Properties:**
- Same current through all components
- Rtotal = R1 + R2 + ... + Rn
- Vtotal = V1 + V2 + ... + Vn

**Parallel Circuit Properties:**
- Same voltage across all components
- 1/Rtotal = 1/R1 + 1/R2 + ... + 1/Rn
- Itotal = I1 + I2 + ... + In
''')