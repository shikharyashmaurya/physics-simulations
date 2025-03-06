import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# Streamlit app title and description
st.title("Kinetic Theory of Gases Simulation")
st.write("This simulation visualizes gas molecules as particles moving in a 2D container. Watch how their motion relates to temperature and pressure!")

# Simulation parameters
L = 1.0          # Container side length
N = 50           # Number of particles
sigma = 0.05     # Standard deviation of velocities (related to temperature)
dt = 0.01        # Time step for simulation

# Initialize particle positions and velocities
x = np.random.uniform(0, L, N)
y = np.random.uniform(0, L, N)
vx = np.random.normal(0, sigma, N)
vy = np.random.normal(0, sigma, N)

# Initialize momentum transfer for pressure calculation
total_momentum_transfer = 0

# Create placeholders for plot and metrics
plot_placeholder = st.empty()
metrics_placeholder = st.empty()

# Simulation loop
step = 0
while True:
    # Update particle positions
    x_new = x + vx * dt
    y_new = y + vy * dt
    
    # Handle collisions with walls and accumulate momentum transfer
    for i in range(N):
        if x_new[i] < 0:
            x_new[i] = -x_new[i]              # Reflect position
            vx[i] = -vx[i]                    # Reverse velocity
            total_momentum_transfer += 2 * abs(vx[i])
        elif x_new[i] > L:
            x_new[i] = 2 * L - x_new[i]       # Reflect position
            vx[i] = -vx[i]                    # Reverse velocity
            total_momentum_transfer += 2 * abs(vx[i])
        if y_new[i] < 0:
            y_new[i] = -y_new[i]              # Reflect position
            vy[i] = -vy[i]                    # Reverse velocity
            total_momentum_transfer += 2 * abs(vy[i])
        elif y_new[i] > L:
            y_new[i] = 2 * L - y_new[i]       # Reflect position
            vy[i] = -vy[i]                    # Reverse velocity
            total_momentum_transfer += 2 * abs(vy[i])
    
    # Update positions
    x = x_new
    y = y_new
    
    # Increment step counter
    step += 1
    
    # Calculate and display temperature and pressure every 100 steps
    if step % 100 == 0:
        # Temperature: T = (1/2) * <v^2> in 2D (with k=1, m=1)
        v_squared = vx**2 + vy**2
        T = (1 / (2 * N)) * np.sum(v_squared)
        
        # Pressure: P = momentum_transfer / (perimeter * time)
        time_elapsed = 100 * dt
        P = total_momentum_transfer / (4 * L * time_elapsed)
        
        # Update metrics display
        metrics_placeholder.write(f"Temperature: {T:.4f} | Pressure: {P:.4f}")
        
        # Reset momentum transfer
        total_momentum_transfer = 0
    
    # Create and update the Plotly scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=5)))
    fig.update_layout(
        xaxis_range=[0, L],
        yaxis_range=[0, L],
        width=500,
        height=500,
        title="Gas Molecules in Motion"
    )
    plot_placeholder.plotly_chart(fig)
    
    # Control animation speed
    time.sleep(0.05)