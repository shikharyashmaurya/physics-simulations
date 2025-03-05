import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Sidebar for user input
st.sidebar.title("Input Particles")
instructions = """
Enter particles in the format: mass,x,y
One particle per line.
For example:
1,0,0
2,3,4
1.5,2,1
"""
st.sidebar.markdown(instructions)

# Prefill with an example for immediate visualization
example_input = "1,0,0\n2,3,4\n1.5,2,1"
input_text = st.sidebar.text_area("Particles", value=example_input, height=200)

# Parse the input
particles = []
lines = input_text.strip().split('\n')
for line in lines:
    if line.strip() == '':  # Skip empty lines
        continue
    try:
        m, x, y = map(float, line.split(','))
        particles.append((m, x, y))
    except ValueError:
        st.error(f"Invalid input: {line}")
        particles = []  # Reset on error
        break

# Process and visualize if there are valid particles
if particles:
    # Extract masses and coordinates
    masses = np.array([p[0] for p in particles])
    x_coords = np.array([p[1] for p in particles])
    y_coords = np.array([p[2] for p in particles])
    total_mass = np.sum(masses)

    if total_mass == 0:
        st.write("Total mass is zero. Cannot compute Center of Mass.")
    else:
        # Calculate Center of Mass
        x_com = np.sum(masses * x_coords) / total_mass
        y_com = np.sum(masses * y_coords) / total_mass

        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(x_coords, y_coords, 'bo', label='Particles')  # Blue dots for particles
        ax.plot(x_com, y_com, 'r*', markersize=15, label='Center of Mass')  # Red star for COM
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title("Center of Mass Visualization")
        ax.legend()
        ax.grid(True)  # Add grid for readability
        ax.set_aspect('equal')  # Equal aspect ratio for accurate distances

        # Set plot limits dynamically
        if len(particles) > 1:
            x_min, x_max = np.min(x_coords), np.max(x_coords)
            y_min, y_max = np.min(y_coords), np.max(y_coords)
            ax.set_xlim(x_min - 1, x_max + 1)
            ax.set_ylim(y_min - 1, y_max + 1)
        else:
            ax.set_xlim(-5, 5)
            ax.set_ylim(-5, 5)

        # Display the plot in Streamlit
        st.pyplot(fig)
        st.write(f"Center of Mass: ({x_com:.2f}, {y_com:.2f})")
else:
    st.write("Please enter at least one particle.")