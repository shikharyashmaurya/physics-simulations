import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def generate_ising_lattice(N, seed=None):
    """Generate an N x N lattice with random spins ±1."""
    if seed is not None:
        np.random.seed(seed)
    lattice = np.random.choice([1, -1], size=(N, N))
    return lattice

def block_spin_transform(lattice, block_size):
    """
    Perform a block spin transformation:
    Divide the lattice into blocks of size block_size x block_size.
    Each block's spin is set to +1 if the sum of spins is non-negative, and -1 otherwise.
    """
    N = lattice.shape[0]
    new_size = N // block_size
    new_lattice = np.zeros((new_size, new_size), dtype=int)
    for i in range(new_size):
        for j in range(new_size):
            block = lattice[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
            if np.sum(block) >= 0:
                new_lattice[i, j] = 1
            else:
                new_lattice[i, j] = -1
    return new_lattice

# Streamlit app layout
st.title("Renormalization Group Visualization via Block Spin Transformation")
st.write("""
This simulation demonstrates a renormalization group (RG) transformation applied to an Ising model.
The RG step is implemented as a block spin transformation where blocks of spins are replaced by their majority.
Adjust the parameters in the sidebar to see how coarse-graining affects the lattice configuration.
""")

# Sidebar controls for interactive simulation
N = st.sidebar.slider("Lattice Size", 64, 256, 128, step=16)
block_size = st.sidebar.slider("Block Size", 2, 16, 2, step=1)
iterations = st.sidebar.slider("Iterations", 1, 5, 1, step=1)
seed = st.sidebar.number_input("Random Seed (optional)", value=42)

# Generate the initial lattice and perform iterative block transformations
lattice = generate_ising_lattice(N, seed)
lattice_current = lattice.copy()

# Create subplots to display the original and renormalized lattices
fig, axs = plt.subplots(1, iterations+1, figsize=(4*(iterations+1), 4))
axs[0].imshow(lattice, cmap="bwr", interpolation="nearest")
axs[0].set_title("Original Lattice")
axs[0].axis("off")

for it in range(iterations):
    lattice_current = block_spin_transform(lattice_current, block_size)
    axs[it+1].imshow(lattice_current, cmap="bwr", interpolation="nearest")
    axs[it+1].set_title(f"Iteration {it+1}")
    axs[it+1].axis("off")

st.pyplot(fig)
