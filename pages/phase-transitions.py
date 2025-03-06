import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define grid size and interaction energy
grid_size = 50
ε = 1.0  # Energy scale for interactions

# Initialize the grid with half the sites occupied (stored in session state)
if 'grid' not in st.session_state:
    total_sites = grid_size * grid_size
    num_occupied = total_sites // 2
    grid = np.zeros((grid_size, grid_size), dtype=int)
    indices = np.random.choice(total_sites, num_occupied, replace=False)
    grid.flat[indices] = 1
    st.session_state.grid = grid

# Function to count occupied neighbors with periodic boundaries
def get_occupied_neighbors(grid, i, j):
    return (grid[(i-1) % grid_size, j] + grid[(i+1) % grid_size, j] +
            grid[i, (j-1) % grid_size] + grid[i, (j+1) % grid_size])

# Add a temperature slider
T = st.slider("Temperature", min_value=0.0, max_value=5.0, value=2.0, step=0.1)

# Run Monte Carlo simulation with Kawasaki dynamics
num_steps = 1000
for _ in range(num_steps):
    # Find occupied and empty sites
    occupied_indices = np.argwhere(st.session_state.grid == 1)
    empty_indices = np.argwhere(st.session_state.grid == 0)
    if len(occupied_indices) == 0 or len(empty_indices) == 0:
        break
    # Randomly select one occupied (A) and one empty (B) site
    A = tuple(occupied_indices[np.random.randint(len(occupied_indices))])
    B = tuple(empty_indices[np.random.randint(len(empty_indices))])
    # Calculate energy change for swapping A and B
    num_neighbors_A = get_occupied_neighbors(st.session_state.grid, *A)
    num_neighbors_B = get_occupied_neighbors(st.session_state.grid, *B)
    ΔE = ε * (num_neighbors_A - num_neighbors_B)
    # Accept swap based on Metropolis criterion
    if ΔE < 0 or np.random.rand() < np.exp(-ΔE / T):
        st.session_state.grid[A] = 0
        st.session_state.grid[B] = 1

# Visualize the grid
fig, ax = plt.subplots()
ax.imshow(st.session_state.grid, cmap='Blues')
ax.set_title(f"Temperature = {T}")
ax.set_xticks([])
ax.set_yticks([])  # Remove axis ticks for clarity
st.pyplot(fig)

# Add explanatory text
st.write("""
### What’s Happening?
This simulation uses the lattice gas model to show a liquid-gas phase transition:
- **Blue cells** represent the liquid phase (occupied sites).
- **White cells** represent the gas phase (empty sites).
- Below the critical temperature (\(T_c \approx 2.27\)), the system separates into high-density (liquid) and low-density (gas) regions.
- Above \(T_c\), it remains in a uniform mixed phase.
Adjust the temperature slider to see how the system evolves!
""")