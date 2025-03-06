import streamlit as st
import pint
import math

# Initialize the unit registry from Pint
ureg = pint.UnitRegistry()

st.title("Dimensional Analysis Visualizer")
st.markdown("""
This interactive simulation demonstrates how dimensional analysis works for different physics equations.
Select an example from the sidebar, adjust the parameters, and see how the units come together to verify that the equation is dimensionally consistent.
""")

# Sidebar to select the example
option = st.sidebar.selectbox("Select a physics concept", 
                              ["Gravitational Force", "Pendulum Period", "Kinetic Energy"])

if option == "Gravitational Force":
    st.header("Gravitational Force: F = G * m₁ * m₂ / r²")
    st.markdown("""
    **Concept:** The gravitational force between two masses is given by Newton’s law of gravitation.
    
    **Units Check:**  
    - **G (Gravitational constant):** m³/(kg·s²)  
    - **m₁ and m₂ (Masses):** kg  
    - **r (Distance):** m  
    When you combine these, the result should have the units of force (Newton): kg·m/s².
    """)
    # User inputs for masses and distance
    m1_val = st.number_input("Mass 1 (kg)", value=5.0, min_value=0.0)
    m2_val = st.number_input("Mass 2 (kg)", value=5.0, min_value=0.0)
    r_val = st.number_input("Distance (m)", value=1.0, min_value=0.1)

    # Define constants and variables with units
    G_val = 6.67430e-11  # Gravitational constant (SI units)
    G = G_val * ureg("meter**3/(kilogram*second**2)")
    m1 = m1_val * ureg.kilogram
    m2 = m2_val * ureg.kilogram
    r = r_val * ureg.meter

    # Compute gravitational force using dimensional quantities
    F = G * m1 * m2 / (r**2)

    st.write("**Computed Gravitational Force:**", F)
    st.write("**Dimensionality of F:**", F.dimensionality)
    # Expected dimension for force (Newton)
    expected = ureg.newton
    st.write("**Expected Dimensionality (Newton):**", expected.dimensionality)
    if F.dimensionality == expected.dimensionality:
        st.success("Dimensional analysis checks out!")
    else:
        st.error("There is an inconsistency in the dimensions.")

elif option == "Pendulum Period":
    st.header("Pendulum Period: T = 2π √(L/g)")
    st.markdown("""
    **Concept:** The period of a simple pendulum (for small oscillations) depends on its length L and the gravitational acceleration g.
    
    **Units Check:**  
    - **L (Length):** m  
    - **g (Gravitational acceleration):** m/s²  
    When you take the square root of (L/g), the result has units of time (s), and multiplying by 2π (a dimensionless constant) keeps the dimension unchanged.
    """)
    # User inputs for pendulum length and gravitational acceleration
    L_val = st.number_input("Length L (m)", value=1.0, min_value=0.0)
    g_val = st.number_input("Gravitational acceleration g (m/s²)", value=9.8, min_value=0.1)

    L = L_val * ureg.meter
    g = g_val * ureg("meter/second**2")
    
    # Calculate the period numerically (2π is dimensionless)
    T_numeric = 2 * math.pi * math.sqrt(L_val / g_val)
    st.write("**Computed Pendulum Period T:**", f"{T_numeric:.3f} seconds")
    
    # Dimensional analysis using Pint: sqrt(L/g) must have the dimension of time
    time_dim = (L / g)**0.5
    st.write("**Dimensionality of √(L/g):**", time_dim.dimensionality)
    expected = ureg.second
    st.write("**Expected Dimensionality (second):**", expected.dimensionality)
    if time_dim.dimensionality == expected.dimensionality:
        st.success("Dimensional analysis checks out!")
    else:
        st.error("There is an inconsistency in the dimensions.")

elif option == "Kinetic Energy":
    st.header("Kinetic Energy: E = ½ m v²")
    st.markdown("""
    **Concept:** The kinetic energy of a moving object is given by one-half the product of its mass and the square of its velocity.
    
    **Units Check:**  
    - **m (Mass):** kg  
    - **v (Velocity):** m/s  
    Therefore, m·v² has units kg·(m²/s²), which are the units of energy (Joule).
    """)
    # User inputs for mass and velocity
    m_val = st.number_input("Mass m (kg)", value=1.0, min_value=0.0)
    v_val = st.number_input("Velocity v (m/s)", value=1.0, min_value=0.0)

    m = m_val * ureg.kilogram
    v = v_val * ureg("meter/second")
    E = 0.5 * m * (v**2)

    st.write("**Computed Kinetic Energy E:**", E)
    st.write("**Dimensionality of E:**", E.dimensionality)
    expected = ureg.joule
    st.write("**Expected Dimensionality (Joule):**", expected.dimensionality)
    if E.dimensionality == expected.dimensionality:
        st.success("Dimensional analysis checks out!")
    else:
        st.error("There is an inconsistency in the dimensions.")
