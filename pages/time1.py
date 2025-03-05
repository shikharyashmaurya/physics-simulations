import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

def time_dilation_visualization():
    """
    Visualize time dilation effect using relativistic time calculation
    """
    st.header("Time Dilation Visualization")
    st.markdown("""
    Time dilation demonstrates how time passes differently 
    depending on relative motion and gravitational fields.
    """)
    
    # Slider for velocity as a fraction of speed of light
    velocity = st.slider(
        "Velocity (as a fraction of speed of light)", 
        min_value=0.0, 
        max_value=0.99, 
        value=0.0, 
        step=0.01
    )
    
    # Speed of light
    c = 299792458  # meters per second
    
    # Calculate time dilation factor
    if velocity > 0:
        time_dilation_factor = 1 / np.sqrt(1 - (velocity ** 2))
        
        # Visualize time passage
        st.write(f"Velocity: {velocity * c:,.0f} m/s")
        st.write(f"Time Dilation Factor: {time_dilation_factor:.4f}")
        
        # Create a comparative visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Normal time (stationary reference frame)
        normal_time = np.linspace(0, 10, 100)
        dilated_time = normal_time * time_dilation_factor
        
        ax.plot(normal_time, normal_time, label='Stationary Time', color='blue')
        ax.plot(normal_time, dilated_time, label='Dilated Time', color='red', linestyle='--')
        
        ax.set_xlabel('Proper Time')
        ax.set_ylabel('Observed Time')
        ax.set_title('Time Dilation Comparison')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
        st.markdown("""
        **Interpretation:**
        - Blue line represents time in a stationary reference frame
        - Red dashed line shows time for an object moving at high velocity
        - As velocity increases, time appears to slow down for the moving object
        """)
    else:
        st.write("Adjust velocity to see time dilation effect")

def entropy_and_time():
    """
    Visualize entropy as a representation of time's arrow
    """
    st.header("Entropy: The Arrow of Time")
    
    # Simulation of entropy increase
    st.markdown("""
    Entropy demonstrates why time seems to flow in one direction.
    The second law of thermodynamics suggests that entropy (disorder) 
    always increases in a closed system.
    """)
    
    # Create an entropy visualization
    states = st.slider(
        "Number of System States", 
        min_value=10, 
        max_value=500, 
        value=100
    )
    
    # Generate entropy data
    np.random.seed(42)
    entropy_data = np.cumsum(np.random.random(states))
    
    # Plotly visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(states)), 
        y=entropy_data, 
        mode='lines', 
        name='Entropy Progression'
    ))
    
    fig.update_layout(
        title='Entropy Progression Over Time',
        xaxis_title='Time Steps',
        yaxis_title='Cumulative Entropy'
    )
    
    st.plotly_chart(fig)
    
    st.markdown("""
    **Key Observations:**
    - Entropy consistently increases over time
    - This irreversible increase creates a 'time arrow'
    - Demonstrates why we can remember the past but not the future
    """)

def main():
    st.title("Time in Physics: A Multidimensional Exploration")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose a Visualization",
        [
            "Time Dilation", 
            "Entropy and Time's Arrow"
        ]
    )
    
    # Page routing
    if page == "Time Dilation":
        time_dilation_visualization()
    elif page == "Entropy and Time's Arrow":
        entropy_and_time()

if __name__ == "__main__":
    main()

# Note: To run this, you'll need to install:
# streamlit, numpy, matplotlib, plotly
# Use command: streamlit run time_visualization.py