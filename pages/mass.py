import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

def introduction_to_mass():
    """
    Provides an introductory explanation of mass
    """
    st.header("Understanding Mass 🧊")
    st.markdown("""
    Mass is a fundamental property of matter that represents the amount of material in an object. 
    It is a measure of an object's resistance to acceleration when a force is applied.

    Key Characteristics of Mass:
    - Measured in kilograms (kg)
    - Remains constant regardless of location (unlike weight)
    - Determines an object's inertia
    """)

def mass_vs_weight_simulation():
    """
    Interactive simulation showing difference between mass and weight
    """
    st.header("Mass vs Weight Comparison 🌍")
    
    # Gravity values for different celestial bodies
    gravity_dict = {
        "Earth": 9.8,
        "Moon": 1.62,
        "Mars": 3.72,
        "Jupiter": 24.79
    }
    
    # User input for mass
    mass = st.slider("Select Object Mass (kg)", min_value=1, max_value=100, value=50)
    
    # Create DataFrame for visualization
    data = []
    for planet, gravity in gravity_dict.items():
        weight = mass * gravity
        data.append({"Celestial Body": planet, "Weight (N)": weight})
    
    df = pd.DataFrame(data)
    
    # Plotly bar chart
    fig = px.bar(df, x="Celestial Body", y="Weight (N)", 
                 title=f"Weight of a {mass} kg Object on Different Planets",
                 labels={"Weight (N)": "Weight (Newtons)"})
    st.plotly_chart(fig)
    
    # Explanation
    st.markdown(f"""
    🔍 For a {mass} kg object:
    - Mass remains constant at {mass} kg everywhere
    - Weight changes based on local gravitational acceleration
    """)

def density_visualization():
    """
    Visualization of mass density
    """
    st.header("Mass Density Exploration 📊")
    
    # Predefined materials and their densities
    materials = {
        "Air": 0.001225,
        "Water": 1000,
        "Wood": 700,
        "Aluminum": 2700,
        "Iron": 7874,
        "Lead": 11340
    }
    
    # User selects volume
    volume = st.slider("Select Volume (m³)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    
    # Calculate masses
    masses = {material: density * volume for material, density in materials.items()}
    
    # Create DataFrame
    df = pd.DataFrame.from_dict(masses, orient='index', columns=['Mass (kg)'])
    df.index.name = 'Material'
    df = df.reset_index()
    
    # Plotly bar chart
    fig = px.bar(df, x='Material', y='Mass (kg)', 
                 title=f"Mass of Different Materials (Volume: {volume} m³)",
                 labels={'Mass (kg)': 'Mass (kg)'})
    st.plotly_chart(fig)
    
    st.markdown("""
    💡 Density determines how much mass is contained in a given volume:
    - Low density: Less mass per volume (e.g., Air)
    - High density: More mass per volume (e.g., Lead)
    """)

def main():
    """
    Main Streamlit app
    """
    st.title("Mass Visualization Simulator 🔬")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a Visualization", [
        "Introduction to Mass", 
        "Mass vs Weight", 
        "Density Exploration"
    ])
    
    # Page routing
    if page == "Introduction to Mass":
        introduction_to_mass()
    elif page == "Mass vs Weight":
        mass_vs_weight_simulation()
    elif page == "Density Exploration":
        density_visualization()

if __name__ == "__main__":
    main()