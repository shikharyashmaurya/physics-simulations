import streamlit as st
import matplotlib.pyplot as plt

st.title("Mechanical Advantage Simulation: Lever")

st.write(
    """
    This simulation visualizes the concept of mechanical advantage for a simple lever.
    Adjust the parameters below to see how the input force is amplified.
    """
)

# Slider inputs for the simulation parameters
effort_arm = st.slider(
    "Effort Arm Length (distance from fulcrum to applied force, in meters)",
    min_value=0.1, max_value=10.0, value=5.0, step=0.1
)
load_arm = st.slider(
    "Load Arm Length (distance from fulcrum to load, in meters)",
    min_value=0.1, max_value=10.0, value=2.0, step=0.1
)
input_force = st.slider(
    "Input Force (in Newtons)",
    min_value=0.0, max_value=100.0, value=10.0, step=0.5
)

# Calculate mechanical advantage and output force
mechanical_advantage = effort_arm / load_arm
output_force = input_force * mechanical_advantage

st.markdown(f"### Mechanical Advantage: {mechanical_advantage:.2f}")
st.markdown(f"### Output Force: {output_force:.2f} N")

# Plotting a simple lever diagram
fig, ax = plt.subplots(figsize=(8, 3))
ax.set_xlim(-1, effort_arm + load_arm + 1)
ax.set_ylim(-3, 3)
ax.axhline(0, color="black", linewidth=2)

# Define positions for the fulcrum, effort, and load
fulcrum_pos = effort_arm
load_pos = fulcrum_pos + load_arm

# Plot the fulcrum
ax.plot(fulcrum_pos, 0, marker="v", markersize=15, color="red")
ax.annotate("Fulcrum", xy=(fulcrum_pos, 0), xytext=(fulcrum_pos, -0.5),
            ha="center", color="red")

# Draw the lever as a horizontal line
ax.plot([0, load_pos], [0, 0], color="gray", linewidth=3)

# Plot effort force arrow
ax.arrow(0, 0, fulcrum_pos * 0.8, 1.0, head_width=0.3, head_length=0.3, fc="green", ec="green")
ax.text(0, 1.2, "Effort", color="green", ha="center")

# Plot load force arrow (direction reversed to indicate opposition)
ax.arrow(load_pos, 0, -load_arm * 0.8, -1.0, head_width=0.3, head_length=0.3, fc="blue", ec="blue")
ax.text(load_pos, -1.2, "Load", color="blue", ha="center")

# Remove axes for clarity
ax.axis("off")

st.pyplot(fig)
