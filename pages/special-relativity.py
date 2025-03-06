import streamlit as st
import math
import matplotlib.pyplot as plt

st.title("Special Relativity Visualization: Length Contraction")

st.markdown(
    """
    In special relativity, an object moving with velocity \( v \) will have its length contracted as observed in the lab frame.
    The contracted length \( L \) is given by:
    
    \[
    L = L_0 \sqrt{1 - \beta^2} \quad \text{with} \quad \beta = \frac{v}{c}
    \]
    
    (Here, we set \( c = 1 \) for simplicity.)
    """
)

# Slider to select the velocity (as a fraction of c)
v = st.slider("Select velocity (v) as a fraction of the speed of light", 0.0, 0.99, 0.0, 0.01)

# Define the rest length (in arbitrary units)
L0 = 10  # rest length
beta = v  # since c = 1
gamma = 1 / math.sqrt(1 - beta**2)  # Lorentz factor
L_contracted = L0 * math.sqrt(1 - beta**2)

st.write(f"At \( v = {v:.2f}c \):")
st.write(f"- Lorentz factor \( \\gamma \\) = {gamma:.2f}")
st.write(f"- Rest Length: {L0} units")
st.write(f"- Contracted Length: {L_contracted:.2f} units")

# Create a plot to visualize the contraction
fig, ax = plt.subplots(figsize=(8, 2))

# Draw the rest length bar (in the rest frame) in blue
ax.broken_barh([(0, L0)], (10, 9), facecolors='blue', label="Rest Frame (Proper Length)")

# Draw the moving rod (length contracted) in red
ax.broken_barh([(0, L_contracted)], (0, 9), facecolors='red', label="Moving Frame (Contracted)")

# Formatting the plot
ax.set_ylim(0, 20)
ax.set_xlim(0, L0 + 1)
ax.set_xlabel("Length (arbitrary units)")
ax.set_yticks([5, 15])
ax.set_yticklabels(["Moving Frame", "Rest Frame"])
ax.set_title("Length Contraction Visualization")
ax.legend(loc='upper right')

st.pyplot(fig)
