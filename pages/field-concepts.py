import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Introduction and instructions
st.markdown("""
# Electric Field Visualization

This app helps you visualize the electric field created by point charges in a 2D space.

### How to Use
- In the sidebar, enter the charges in the format `x,y,Q` (one per line), where:
  - `x` and `y` are the coordinates of the charge.
  - `Q` is the charge value (positive or negative).
- Example: `0,0,1` places a positive charge of 1 at the origin, and `3,0,-1` places a negative charge at (3,0).
- Select the visualization type:
  - **Quiver Plot**: Shows arrows representing the direction and strength of the electric field.
  - **Field Lines**: Displays lines that follow the electric field's direction.

Try starting with `0,0,1` and `3,0,-1` to see a dipole field!
""")

# Sidebar inputs
charges_input = st.sidebar.text_area(
    "Enter charges (x,y,Q) one per line", 
    "0,0,1\n3,0,-1"
)
vis_type = st.sidebar.radio("Visualization Type", ["Quiver Plot", "Field Lines"])

# Parse the input charges
charges = []
for line in charges_input.split('\n'):
    if line.strip():
        try:
            x, y, Q = map(float, line.split(','))
            charges.append((x, y, Q))
        except ValueError:
            st.sidebar.error(f"Invalid input: {line}. Use format x,y,Q.")
            st.stop()

# Check if there are any charges
if not charges:
    st.warning("No charges entered. Please add charges in the sidebar.")
    st.stop()

# Function to compute the electric field at a point (x, y)
def electric_field(x, y, charges):
    Ex, Ey = 0, 0
    for cx, cy, Q in charges:
        dx = x - cx
        dy = y - cy
        r2 = dx**2 + dy**2
        # Avoid division by zero (when point is exactly at a charge)
        if r2 < 1e-10:
            continue
        r3 = r2**1.5
        Ex += Q * dx / r3
        Ey += Q * dy / r3
    return Ex, Ey

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 8))

# Define the grid for quiver plot
x = np.arange(-10, 11, 1)
y = np.arange(-10, 11, 1)
X, Y = np.meshgrid(x, y)

if vis_type == "Quiver Plot":
    # Compute electric field across the grid
    Ex = np.zeros_like(X, dtype=float)
    Ey = np.zeros_like(Y, dtype=float)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Ex[i, j], Ey[i, j] = electric_field(X[i, j], Y[i, j], charges)
    
    # Calculate field magnitude for coloring
    M = np.sqrt(Ex**2 + Ey**2)
    
    # Plot quiver with magnitude-based coloring
    quiv = ax.quiver(X, Y, Ex, Ey, M, cmap='viridis', scale=50)
    fig.colorbar(quiv, ax=ax, label='Field Magnitude')

else:  # Field Lines
    # Generate starting points around each charge
    starting_points = []
    for cx, cy, Q in charges:
        # 8 points around each charge at a small radius
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            x0 = cx + 0.1 * np.cos(angle)
            y0 = cy + 0.1 * np.sin(angle)
            starting_points.append((x0, y0))
    
    # Trace field lines from each starting point
    for x0, y0 in starting_points:
        path = [(x0, y0)]
        for _ in range(100):  # Maximum steps
            Ex, Ey = electric_field(x0, y0, charges)
            mag = np.sqrt(Ex**2 + Ey**2)
            if mag < 1e-5:  # Stop if field is too weak
                break
            # Normalize step size
            step_x = 0.1 * Ex / mag
            step_y = 0.1 * Ey / mag
            x0 += step_x
            y0 += step_y
            # Stop if outside the plot boundaries
            if x0 < -10 or x0 > 10 or y0 < -10 or y0 > 10:
                break
            path.append((x0, y0))
        
        # Plot the field line
        px, py = zip(*path)
        ax.plot(px, py, 'k-', linewidth=1)

# Plot the charges
for cx, cy, Q in charges:
    color = 'red' if Q > 0 else 'blue'
    ax.plot(cx, cy, 'o', color=color, markersize=10, label=f'Q={Q}')

# Customize the plot
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(f'Electric Field - {vis_type}')
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)