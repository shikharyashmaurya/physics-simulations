import streamlit as st
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.title("Coulomb's Law Visualization")
st.write("Adjust the charges Q1, Q2, and the distance r to see the force between them.")

# Input sliders for Q1, Q2, and r
Q1 = st.slider("Charge Q1", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
Q2 = st.slider("Charge Q2", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
r = st.slider("Distance r", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Calculate the force (k=1 for simplicity)
F = (Q1 * Q2) / r**2

# Function to determine color based on charge sign
def get_color(Q):
    if Q > 0:
        return 'blue'  # Positive charge
    elif Q < 0:
        return 'red'   # Negative charge
    else:
        return 'gray'  # Zero charge

# Assign colors to charges
colors = [get_color(Q1), get_color(Q2)]

# Create the plot
fig, ax = plt.subplots()
ax.set_xlim(-1, r + 1)  # Adjust x-axis based on distance r
ax.set_ylim(-1, 1)      # Fixed y-axis for a 1D representation

# Plot the charges as points
ax.scatter([0, r], [0, 0], c=colors, s=100)
ax.text(-0.5, 0.5, f'Q1 = {Q1:.1f}')  # Label for Q1
ax.text(r + 0.5, 0.5, f'Q2 = {Q2:.1f}')  # Label for Q2

# Draw an arrow to represent the force direction on Q1
if F != 0:
    # If Q1*Q2 > 0 (like charges), force is repulsive (to the left)
    # If Q1*Q2 < 0 (unlike charges), force is attractive (to the right)
    dx = -0.5 if Q1 * Q2 > 0 else 0.5
    ax.quiver(0, 0, dx, 0, scale=1, scale_units='xy', angles='xy', color='green')

# Customize the plot
ax.set_xlabel('Distance')
ax.set_title("Coulomb's Law")

# Display the plot in Streamlit
st.pyplot(fig)

# Display force magnitude and direction
st.write(f"**Force magnitude:** {abs(F):.2f} units")
if Q1 * Q2 > 0:
    direction = "to the left (repulsive)"
elif Q1 * Q2 < 0:
    direction = "to the right (attractive)"
else:
    direction = "zero"
st.write(f"**Force direction on Q1:** {direction}")
st.write("**Note:** Coulomb's constant k is set to 1 for simplicity.")