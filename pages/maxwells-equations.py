import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Visualizing Maxwell's Equations")
st.write("An illustrative visualization of fundamental concepts related to Maxwell's Equations.")

equation_choice = st.selectbox("Choose a Maxwell's Equation Concept to Visualize:",
                                 ["Electric Field of a Point Charge (Gauss's Law for Electricity)",
                                  "Magnetic Field of a Current-Carrying Wire (Ampere's Law)",
                                  "Electromagnetic Plane Wave (Faraday's & Ampere-Maxwell - Simplified)"])

# --- Visualization Functions ---

def electric_field_point_charge(charge_pos_x, charge_pos_y, charge_magnitude, grid_size):
    """Visualizes the electric field of a point charge."""
    x = np.linspace(-grid_size, grid_size, 30)
    y = np.linspace(-grid_size, grid_size, 30)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r_vec = np.array([X[i, j] - charge_pos_x, Y[i, j] - charge_pos_y])
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0.1:  # Avoid singularity at charge location
                E_direction = r_vec / r_mag
                E_magnitude = charge_magnitude / (r_mag**2) #Simplified formula, ignoring constants for visualization
                Ex[i, j] = E_magnitude * E_direction[0]
                Ey[i, j] = E_magnitude * E_direction[1]

    return X, Y, Ex, Ey

def magnetic_field_wire(wire_pos_x, wire_pos_y, current_magnitude, grid_size):
    """Visualizes the magnetic field around a long straight wire."""
    x = np.linspace(-grid_size, grid_size, 30)
    y = np.linspace(-grid_size, grid_size, 30)
    X, Y = np.meshgrid(x, y)

    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(X) # Magnetic field in the Z direction (out of plane)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r_vec = np.array([X[i, j] - wire_pos_x, Y[i, j] - wire_pos_y])
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0.1: # Avoid singularity at wire location
                B_direction = np.array([-r_vec[1], r_vec[0]]) / r_mag # Tangential direction (right-hand rule)
                B_magnitude = current_magnitude / r_mag # Simplified, ignoring constants
                Bx[i, j] = B_magnitude * B_direction[0]
                By[i, j] = B_magnitude * B_direction[1]
                Bz[i,j] = 0 # for 2D visualization, assume B is in xy plane

    return X, Y, Bx, By, Bz

def electromagnetic_plane_wave(time_step, grid_size, wave_direction):
    """Illustrative plane EM wave propagation (simplified)."""
    x = np.linspace(-grid_size, grid_size, 30)
    y = np.linspace(-grid_size, grid_size, 30)
    X, Y = np.meshgrid(x, y)
    t = time_step

    # Simplified Plane Wave along x-axis for illustration
    if wave_direction == "x":
        Ex = np.sin(X - t)
        Ey = np.zeros_like(X)
        Ez = np.zeros_like(X)
        Bx = np.zeros_like(X)
        By = np.zeros_like(X)
        Bz = np.sin(X - t) # B field perpendicular to E and propagation direction (along z)
    elif wave_direction == "y":
        Ex = np.zeros_like(X)
        Ey = np.sin(Y - t)
        Ez = np.zeros_like(X)
        Bx = np.sin(Y - t) # B perpendicular to E and prop. direction (along x)
        By = np.zeros_like(X)
        Bz = np.zeros_like(X)


    return X, Y, Ex, Ey, Ez, Bx, By, Bz


# --- Streamlit UI based on equation choice ---

st.subheader("Visualization Parameters")

if equation_choice == "Electric Field of a Point Charge (Gauss's Law for Electricity)":
    charge_pos_x = st.slider("Charge Position X", -5.0, 5.0, 0.0)
    charge_pos_y = st.slider("Charge Position Y", -5.0, 5.0, 0.0)
    charge_magnitude = st.slider("Charge Magnitude", -5.0, 5.0, 1.0)
    grid_size = st.slider("Grid Size", 5, 15, 10)

    X, Y, Ex, Ey = electric_field_point_charge(charge_pos_x, charge_pos_y, charge_magnitude, grid_size)

    fig, ax = plt.subplots()
    q = ax.quiver(X, Y, Ex, Ey, color='r', label='Electric Field (E)')
    ax.plot(charge_pos_x, charge_pos_y, 'ro', markersize=10, label='Point Charge')
    ax.set_title("Electric Field of a Point Charge")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis('equal')
    ax.legend()
    st.pyplot(fig)

elif equation_choice == "Magnetic Field of a Current-Carrying Wire (Ampere's Law)":
    wire_pos_x = st.slider("Wire Position X", -5.0, 5.0, 0.0)
    wire_pos_y = st.slider("Wire Position Y", -5.0, 5.0, 0.0)
    current_magnitude = st.slider("Current Magnitude (out of plane)", -5.0, 5.0, 1.0)
    grid_size = st.slider("Grid Size", 5, 15, 10)

    X, Y, Bx, By, Bz = magnetic_field_wire(wire_pos_x, wire_pos_y, current_magnitude, grid_size)

    fig, ax = plt.subplots()
    q = ax.quiver(X, Y, Bx, By, color='b', label='Magnetic Field (B)')
    ax.plot(wire_pos_x, wire_pos_y, 'ko', markersize=10, label='Wire (Current out of plane)')
    ax.set_title("Magnetic Field of a Current-Carrying Wire")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis('equal')
    ax.legend()
    st.pyplot(fig)

elif equation_choice == "Electromagnetic Plane Wave (Faraday's & Ampere-Maxwell - Simplified)":
    wave_direction = st.selectbox("Wave Propagation Direction", ["x", "y"])
    grid_size = st.slider("Grid Size", 5, 15, 10)

    placeholder = st.empty() # For animation

    for t in range(0, 100): # Animation loop
        X, Y, Ex, Ey, Ez, Bx, By, Bz = electromagnetic_plane_wave(t * 0.1, grid_size, wave_direction) # Time step
        fig, ax = plt.subplots()
        q_e = ax.quiver(X[::2, ::2], Y[::2, ::2], Ex[::2, ::2], Ey[::2, ::2], color='r', label='Electric Field (E)', scale=50) # Subsample for clarity
        q_b = ax.quiver(X[::2, ::2], Y[::2, ::2], Bx[::2, ::2], By[::2, ::2], color='b', label='Magnetic Field (B)', scale=50) # Subsample
        ax.set_title("Electromagnetic Plane Wave Propagation")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.axis('equal')
        ax.legend()
        placeholder.pyplot(fig) # Update plot in placeholder
        time.sleep(0.1) # Control animation speed
        plt.close(fig) # Clear figure for next frame