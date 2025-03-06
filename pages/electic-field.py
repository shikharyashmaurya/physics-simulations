import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title of the Streamlit app
st.title("Electric Field Visualization")
st.write("Add charges to see how the electric field changes! Positive charges are red, negative charges are blue.")

# Initialize session state to store charges
if 'charges' not in st.session_state:
    st.session_state.charges = []

# Function to calculate the electric field on a grid
def calculate_electric_field(charges, X, Y, k=1, epsilon=1e-6):
    """
    Calculate the electric field components (E_x, E_y) at each point on the grid.
    
    Parameters:
    - charges: List of dictionaries with 'x', 'y', and 'q' for each charge
    - X, Y: 2D arrays from np.meshgrid representing grid coordinates
    - k: Coulomb's constant (set to 1 for simplicity)
    - epsilon: Small value to avoid division by zero at charge locations
    
    Returns:
    - E_x, E_y: Electric field components as 2D arrays
    """
    E_x_total = np.zeros_like(X)
    E_y_total = np.zeros_like(Y)
    for charge in charges:
        dx = X - charge['x']
        dy = Y - charge['y']
        r = np.sqrt(dx**2 + dy**2 + epsilon)  # Distance with epsilon to avoid singularity
        # E = k * q * r̂ / r^2, where r̂ is the unit vector (dx/r, dy/r)
        # So, E_x = k * q * dx / r^3, E_y = k * q * dy / r^3
        E_x_charge = k * charge['q'] * dx / r**3
        E_y_charge = k * charge['q'] * dy / r**3
        E_x_total += E_x_charge
        E_y_total += E_y_charge
    return E_x_total, E_y_total

# UI to add a charge
st.subheader("Add a Charge")
x = st.slider("X position", -5.0, 5.0, 0.0, key="x_add")
y = st.slider("Y position", -5.0, 5.0, 0.0, key="y_add")
q = st.selectbox("Charge", [1, -1], format_func=lambda val: "+1" if val > 0 else "-1", key="q_add")
if st.button("Add Charge", key="add_charge"):
    st.session_state.charges.append({'x': x, 'y': y, 'q': q})
    st.success(f"Added charge q={q} at ({x}, {y})")

# UI to display and remove charges
st.subheader("Current Charges")
if st.session_state.charges:
    for i, charge in enumerate(st.session_state.charges):
        st.write(f"Charge {i}: x={charge['x']}, y={charge['y']}, q={'+' if charge['q'] > 0 else '-'}1")
    
    # Select and remove a charge
    charge_to_remove = st.selectbox(
        "Select charge to remove",
        options=range(len(st.session_state.charges)),
        format_func=lambda i: f"Charge {i}: x={st.session_state.charges[i]['x']}, y={st.session_state.charges[i]['y']}, q={'+' if st.session_state.charges[i]['q'] > 0 else '-'}1",
        key="charge_to_remove"
    )
    if st.button("Remove Selected Charge", key="remove_charge"):
        del st.session_state.charges[charge_to_remove]
        st.success("Charge removed!")
else:
    st.write("No charges added yet. Add some to see the electric field.")

# Create the plot if there are charges
if st.session_state.charges:
    # Define the grid for calculation
    x_grid = np.linspace(-5, 5, 20)
    y_grid = np.linspace(-5, 5, 20)
    X, Y = np.meshgrid(x_grid, y_grid)

    # Calculate the electric field
    E_x, E_y = calculate_electric_field(st.session_state.charges, X, Y)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.streamplot(X, Y, E_x, E_y, color='black', linewidth=1, density=1.5)
    
    # Plot each charge
    for charge in st.session_state.charges:
        color = 'red' if charge['q'] > 0 else 'blue'
        ax.plot(charge['x'], charge['y'], 'o', color=color, markersize=10, label=f"q={charge['q']}")
    
    # Set plot limits and labels
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Electric Field Lines")
    ax.grid(True)

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.info("Add some charges above to visualize the electric field!")

# Footer
st.write("Note: The field lines point away from positive charges and toward negative charges, following the direction a positive test charge would move.")