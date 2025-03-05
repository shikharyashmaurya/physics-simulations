import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np

# App title and introduction
st.title("Center of Gravity Visualization")
st.markdown("""
The **center of gravity** is the point where the weight of an object is evenly distributed in all directions. 
This simulation lets you explore the center of gravity for different shapes by inputting their parameters.
""")

# Sidebar for shape selection
st.sidebar.title("Shape Selection")
shape = st.sidebar.selectbox("Select a shape", ["Rectangle", "Triangle", "Circle", "Custom Polygon"])

# Input fields and shape definition based on selection
if shape == "Rectangle":
    st.markdown("### Rectangle")
    width = st.number_input("Width", min_value=0.0, value=1.0, step=0.1)
    height = st.number_input("Height", min_value=0.0, value=1.0, step=0.1)
    # Define rectangle points starting at (0,0)
    points = [(0, 0), (width, 0), (width, height), (0, height)]

elif shape == "Triangle":
    st.markdown("### Triangle")
    st.markdown("Enter the coordinates of the three vertices:")
    x1 = st.number_input("X1", value=0.0, step=0.1)
    y1 = st.number_input("Y1", value=0.0, step=0.1)
    x2 = st.number_input("X2", value=1.0, step=0.1)
    y2 = st.number_input("Y2", value=0.0, step=0.1)
    x3 = st.number_input("X3", value=0.5, step=0.1)
    y3 = st.number_input("Y3", value=1.0, step=0.1)
    points = [(x1, y1), (x2, y2), (x3, y3)]

elif shape == "Circle":
    st.markdown("### Circle")
    radius = st.number_input("Radius", min_value=0.0, value=1.0, step=0.1)
    # Approximate circle as a polygon with 100 points
    num_points = 100
    points = [(radius * np.cos(theta), radius * np.sin(theta)) 
              for theta in np.linspace(0, 2 * np.pi, num_points)]

elif shape == "Custom Polygon":
    st.markdown("### Custom Polygon")
    st.markdown("Enter the coordinates of the vertices (one per line, e.g., 'x y') in order:")
    points_str = st.text_area("Points", value="0 0\n1 0\n1 1\n0 1")
    points = []
    for line in points_str.split('\n'):
        if line.strip():
            try:
                x, y = map(float, line.split())
                points.append((x, y))
            except ValueError:
                st.error("Invalid input: Please enter numbers separated by a space (e.g., '1 2').")
                st.stop()
    if len(points) < 3:
        st.error("Need at least 3 points to form a polygon.")
        st.stop()

# Create Polygon object and compute centroid
poly = Polygon(points)
centroid = poly.centroid

# Plotting
st.markdown(f"### {shape} and its Center of Gravity")
fig, ax = plt.subplots()
poly_patch = plt.Polygon(points, fill=False, edgecolor='blue')
ax.add_artist(poly_patch)
ax.plot(centroid.x, centroid.y, 'ro', label='Center of Gravity')
ax.set_aspect('equal')  # Ensure the shape isn't distorted
# Set plot limits with some padding
xs = [p[0] for p in points]
ys = [p[1] for p in points]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
ax.set_xlim(min_x - 1, max_x + 1)
ax.set_ylim(min_y - 1, max_y + 1)
ax.legend()
st.pyplot(fig)

# Display centroid coordinates
st.write(f"**Center of Gravity:** ({centroid.x:.2f}, {centroid.y:.2f})")