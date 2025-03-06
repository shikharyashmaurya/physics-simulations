import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set up the Streamlit app
st.title("Statics Beam Simulation")
st.write("Visualize a simply supported beam with point loads. Enter the beam length and add loads below.")

# User input for beam length
L = st.number_input("Beam Length (m)", min_value=0.1, value=10.0, step=0.1, help="Length of the beam in meters")

# Initialize an example data frame for loads
example_loads = pd.DataFrame({
    'Position (m)': [2.0, 5.0],
    'Magnitude (N)': [100.0, 200.0]
})

# User input for loads using data editor
st.write("Add or edit point loads (downward forces are positive):")
loads = st.data_editor(
    example_loads,
    column_config={
        'Position (m)': st.column_config.NumberColumn(
            min_value=0.0, max_value=L, step=0.1, help="Position along the beam (0 to L)"
        ),
        'Magnitude (N)': st.column_config.NumberColumn(
            min_value=0.0, step=1.0, help="Force magnitude in Newtons (downward)"
        )
    },
    num_rows="dynamic",
    use_container_width=True
)

# Process the loads: group by position to sum magnitudes at the same position
loads_grouped = loads.groupby('Position (m)')['Magnitude (N)'].sum().reset_index()

# Calculate reaction forces
sum_loads = loads_grouped['Magnitude (N)'].sum()
sum_moment = (loads_grouped['Magnitude (N)'] * loads_grouped['Position (m)']).sum()
R_B = sum_moment / L  # Reaction at B (right support)
R_A = sum_loads - R_B  # Reaction at A (left support)

# Display reaction forces
st.subheader("Reaction Forces")
st.write(f"Reaction at A (x=0): **{R_A:.2f} N** (upward)")
st.write(f"Reaction at B (x={L}): **{R_B:.2f} N** (upward)")

# --- Beam Diagram ---
st.subheader("Beam Diagram")
fig_beam = go.Figure()

# Draw the beam as a horizontal line
fig_beam.add_shape(type="line", x0=0, y0=0, x1=L, y1=0, line=dict(color="black", width=3))

# Determine scale for arrows based on maximum force
max_force = max([abs(R_A), abs(R_B)] + [abs(load) for load in loads_grouped['Magnitude (N)']] if not loads_grouped.empty else [1])
scale = max_force / 5  # Scale so largest arrow is 5 units

# Add reaction arrows (upward)
fig_beam.add_annotation(
    x=0, y=0, ax=0, ay=R_A / scale,
    xref="x", yref="y", axref="x", ayref="y",
    text=f"{R_A:.2f} N", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="blue",
    standoff=5
)
fig_beam.add_annotation(
    x=L, y=0, ax=L, ay=R_B / scale,
    xref="x", yref="y", axref="x", ayref="y",
    text=f"{R_B:.2f} N", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="blue",
    standoff=5
)

# Add load arrows (downward)
for index, load in loads_grouped.iterrows():
    x_load = load['Position (m)']
    magnitude = load['Magnitude (N)']
    fig_beam.add_annotation(
        x=x_load, y=0, ax=x_load, ay=-magnitude / scale,
        xref="x", yref="y", axref="x", ayref="y",
        text=f"{magnitude:.2f} N", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="red",
        standoff=5
    )

# Update layout for beam diagram
fig_beam.update_layout(
    xaxis_title="Position (m)",
    yaxis_title="Force (arbitrary units)",
    showlegend=False,
    height=400,
    yaxis_range=[-max_force/scale * 1.5, max_force/scale * 1.5],
    xaxis_range=[-0.1*L, L*1.1]
)
st.plotly_chart(fig_beam, use_container_width=True)

# --- Shear Force and Bending Moment Calculations ---
load_positions = sorted(loads_grouped['Position (m)'].unique())
critical_points = [0] + load_positions + [L]

# Compute shear force (V) at each critical point
V_list = []
cumulative_load = 0
for k in range(len(critical_points)):
    if k > 0:
        x_prev = critical_points[k-1]
        load_at_x_prev = loads_grouped[loads_grouped['Position (m)'] == x_prev]['Magnitude (N)'].sum()
        cumulative_load += load_at_x_prev
    V_k = R_A - cumulative_load
    V_list.append(V_k)

# Compute bending moment (M) at each critical point
M_list = [0]  # M(0) = 0
for k in range(1, len(critical_points)):
    x_prev = critical_points[k-1]
    x_curr = critical_points[k]
    V_k = V_list[k-1]  # Shear force in the segment
    M_curr = M_list[-1] + V_k * (x_curr - x_prev)
    M_list.append(M_curr)

# --- Shear Force Diagram ---
st.subheader("Shear Force Diagram")
fig_V = go.Figure()
fig_V.add_trace(go.Scatter(
    x=critical_points,
    y=V_list,
    mode='lines',
    line_shape='hv',  # Horizontal-vertical steps for shear force
    name='Shear Force',
    line=dict(color='green')
))
fig_V.update_layout(
    xaxis_title="Position (m)",
    yaxis_title="Shear Force (N)",
    height=400,
    xaxis_range=[-0.1*L, L*1.1]
)
st.plotly_chart(fig_V, use_container_width=True)

# --- Bending Moment Diagram ---
st.subheader("Bending Moment Diagram")
fig_M = go.Figure()
fig_M.add_trace(go.Scatter(
    x=critical_points,
    y=M_list,
    mode='lines',
    name='Bending Moment',
    line=dict(color='purple')
))
fig_M.update_layout(
    xaxis_title="Position (m)",
    yaxis_title="Bending Moment (N·m)",
    height=400,
    xaxis_range=[-0.1*L, L*1.1]
)
st.plotly_chart(fig_M, use_container_width=True)

# Footer
st.write("Note: This simulation assumes a simply supported beam with supports at x=0 and x=L. Loads are point forces applied vertically downward.")