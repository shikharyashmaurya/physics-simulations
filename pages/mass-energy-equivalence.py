import streamlit as st
import numpy as np
import pandas as pd

# Define the speed of light constant (in m/s)
c = 3e8  # 300,000,000 m/s

# Set up the Streamlit app title and description.
st.title("Mass–Energy Equivalence Visualization")
st.write("""
Einstein's famous equation \(E = mc^2\) tells us that mass and energy are interchangeable. 
Use the slider below to adjust the mass and see the equivalent energy.
""")

# Create a slider for selecting the mass (in kg)
mass = st.slider("Select mass (kg)", min_value=0.001, max_value=100.0, value=1.0, step=0.001)

# Calculate energy using E = m * c^2
energy = mass * c**2

# Display the calculated energy
st.write(f"**For a mass of {mass:.3f} kg, the equivalent energy is {energy:.3e} Joules.**")

# Additional explanation for perspective
st.write("""
For context, 1 kg of mass is equivalent to about 9 × 10^16 Joules of energy – 
an amount that can power entire cities for days.
""")

# Plotting: Show a graph of Energy vs Mass for a range from 0 up to the selected mass.
st.subheader("Energy as a Function of Mass")
mass_values = np.linspace(0, mass, 100)
energy_values = mass_values * c**2

# Create a DataFrame for plotting
df = pd.DataFrame({
    "Mass (kg)": mass_values,
    "Energy (Joules)": energy_values
})

# Display the line chart
st.line_chart(df.set_index("Mass (kg)"))
