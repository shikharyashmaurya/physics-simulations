import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px

class EnergyVisualization:
    def __init__(self):
        # Energy types and their descriptions
        self.energy_types = {
            "Kinetic Energy": {
                "description": "Energy of motion. Depends on mass and velocity.",
                "formula": "KE = 1/2 * m * v²",
                "example": "A moving car, a rolling ball"
            },
            "Potential Energy": {
                "description": "Stored energy due to position or configuration.",
                "subtypes": {
                    "Gravitational": "Energy due to height in a gravitational field.",
                    "Elastic": "Energy stored in stretched or compressed springs.",
                    "Chemical": "Energy stored in chemical bonds"
                },
                "formula": "PE = m * g * h (for gravitational)",
                "example": "A book on a high shelf, a stretched rubber band"
            },
            "Thermal Energy": {
                "description": "Energy associated with the motion of particles.",
                "formula": "Q = m * c * ΔT",
                "example": "Heat from a fire, warmth of your body"
            },
            "Electrical Energy": {
                "description": "Energy from electric charges and their movement.",
                "formula": "E = V * Q",
                "example": "Lightning, electricity in your home"
            },
            "Chemical Energy": {
                "description": "Energy stored in chemical bonds between atoms and molecules.",
                "formula": "ΔH (Change in Enthalpy)",
                "example": "Batteries, food, fuel"
            }
        }

    def display_energy_overview(self):
        """Create an overview of energy types"""
        st.title("Energy Visualization and Exploration")
        
        # Sidebar for energy type selection
        selected_energy = st.sidebar.selectbox(
            "Select Energy Type", 
            list(self.energy_types.keys())
        )
        
        # Display details of selected energy type
        energy_info = self.energy_types[selected_energy]
        
        st.header(f"{selected_energy}")
        st.write(energy_info["description"])
        st.write(f"**Formula:** {energy_info['formula']}")
        st.write(f"**Example:** {energy_info['example']}")
        
        # Check for subtypes
        if "subtypes" in energy_info:
            st.subheader("Subtypes")
            for subtype, sub_desc in energy_info["subtypes"].items():
                st.write(f"- **{subtype}:** {sub_desc}")
        
        # Interactive visualization based on energy type
        self._visualize_energy_type(selected_energy)

    def _visualize_energy_type(self, energy_type):
        """Create interactive visualizations for different energy types"""
        if energy_type == "Kinetic Energy":
            self._kinetic_energy_visualization()
        elif energy_type == "Potential Energy":
            self._potential_energy_visualization()
        elif energy_type == "Thermal Energy":
            self._thermal_energy_visualization()
        elif energy_type == "Electrical Energy":
            self._electrical_energy_visualization()
        elif energy_type == "Chemical Energy":
            self._chemical_energy_visualization()

    def _kinetic_energy_visualization(self):
        """Visualization for Kinetic Energy"""
        st.subheader("Kinetic Energy Interactive Simulation")
        
        # Mass and velocity sliders
        mass = st.slider("Mass (kg)", 1.0, 100.0, 10.0, 0.1)
        velocity = st.slider("Velocity (m/s)", 0.0, 50.0, 10.0, 0.1)
        
        # Calculate Kinetic Energy
        ke = 0.5 * mass * (velocity ** 2)
        
        # Plotly visualization
        fig = go.Figure(data=[go.Bar(
            x=['Kinetic Energy'], 
            y=[ke], 
            text=[f'{ke:.2f} J'],
            textposition='auto'
        )])
        fig.update_layout(
            title='Kinetic Energy Calculation',
            yaxis_title='Energy (Joules)'
        )
        st.plotly_chart(fig)
        
        st.write(f"**Calculation:** KE = 1/2 * {mass} * {velocity}² = {ke:.2f} Joules")

    def _potential_energy_visualization(self):
        """Visualization for Potential Energy"""
        st.subheader("Gravitational Potential Energy Simulation")
        
        # Inputs for potential energy calculation
        mass = st.slider("Mass (kg)", 1.0, 100.0, 10.0, 0.1)
        height = st.slider("Height (m)", 0.0, 50.0, 10.0, 0.1)
        g = 9.8  # acceleration due to gravity
        
        # Calculate Potential Energy
        pe = mass * g * height
        
        # Create a simple visualization
        fig = plt.figure(figsize=(8, 6))
        plt.title("Gravitational Potential Energy")
        plt.bar(['Potential Energy'], [pe], color='green')
        plt.ylabel('Energy (Joules)')
        plt.text(0, pe, f'{pe:.2f} J', ha='center', va='bottom')
        st.pyplot(fig)
        
        st.write(f"**Calculation:** PE = {mass} * {g} * {height} = {pe:.2f} Joules")

    def _thermal_energy_visualization(self):
        """Visualization for Thermal Energy"""
        st.subheader("Thermal Energy Temperature Simulation")
        
        # Inputs for thermal energy
        mass = st.slider("Mass (kg)", 0.1, 10.0, 1.0, 0.1)
        specific_heat = st.slider("Specific Heat Capacity (J/kg·K)", 100, 5000, 1000, 10)
        delta_temp = st.slider("Temperature Change (°C)", -100, 100, 20, 1)
        
        # Calculate Thermal Energy
        thermal_energy = mass * specific_heat * delta_temp
        
        # Plotly heat map visualization
        temps = np.linspace(-100, 100, 100)
        heat_map = [mass * specific_heat * t for t in temps]
        
        fig = go.Figure(data=[go.Scatter(
            x=temps, 
            y=heat_map, 
            mode='lines', 
            name='Thermal Energy'
        )])
        fig.update_layout(
            title='Thermal Energy vs Temperature',
            xaxis_title='Temperature Change (°C)',
            yaxis_title='Thermal Energy (Joules)'
        )
        st.plotly_chart(fig)
        
        st.write(f"**Calculation:** Q = {mass} * {specific_heat} * {delta_temp} = {thermal_energy:.2f} Joules")

    def _electrical_energy_visualization(self):
        """Visualization for Electrical Energy"""
        st.subheader("Electrical Energy Simulation")
        
        # Inputs for electrical energy
        voltage = st.slider("Voltage (V)", 1, 240, 120, 1)
        charge = st.slider("Charge (Coulombs)", 0.1, 10.0, 1.0, 0.1)
        
        # Calculate Electrical Energy
        electrical_energy = voltage * charge
        
        # Plotly bar chart
        fig = go.Figure(data=[go.Bar(
            x=['Electrical Energy'], 
            y=[electrical_energy], 
            text=[f'{electrical_energy:.2f} J'],
            textposition='auto'
        )])
        fig.update_layout(
            title='Electrical Energy Calculation',
            yaxis_title='Energy (Joules)'
        )
        st.plotly_chart(fig)
        
        st.write(f"**Calculation:** E = {voltage} * {charge} = {electrical_energy:.2f} Joules")

    def _chemical_energy_visualization(self):
        """Visualization for Chemical Energy"""
        st.subheader("Chemical Energy Bond Simulation")
        
        # Chemical bond energy types
        bond_energies = {
            "Hydrogen Bond": 20,
            "Ionic Bond": 700,
            "Covalent Bond": 350,
            "Metallic Bond": 250
        }
        
        # Multiselect for bond types
        selected_bonds = st.multiselect(
            "Select Bond Types", 
            list(bond_energies.keys()), 
            default=["Covalent Bond"]
        )
        
        # Calculate total bond energy
        total_bond_energy = sum(bond_energies[bond] for bond in selected_bonds)
        
        # Pie chart visualization
        fig = go.Figure(data=[go.Pie(
            labels=selected_bonds, 
            values=[bond_energies[bond] for bond in selected_bonds],
            hole=.3
        )])
        fig.update_layout(title='Chemical Bond Energy Distribution')
        st.plotly_chart(fig)
        
        st.write("**Bond Energies:**")
        for bond in selected_bonds:
            st.write(f"- {bond}: {bond_energies[bond]} kJ/mol")
        st.write(f"**Total Bond Energy:** {total_bond_energy} kJ/mol")

def main():
    # Initialize and run the Energy Visualization
    energy_viz = EnergyVisualization()
    energy_viz.display_energy_overview()

if __name__ == "__main__":
    main()

# Requirements for this Streamlit app
# Run this in terminal: 
# pip install streamlit numpy matplotlib plotly
# streamlit run energy_visualization.py