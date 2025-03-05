import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_euclidean_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def create_distance_plot(x1, y1, x2, y2):
    """Create a matplotlib plot showing distance between two points."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x1, y1, 'ro', label='Point 1')  # Red dot for first point
    ax.plot(x2, y2, 'bo', label='Point 2')  # Blue dot for second point
    ax.plot([x1, x2], [y1, y2], 'g--', label='Distance')  # Green dashed line
    ax.set_title('Distance Between Two Points')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)
    ax.legend()
    return fig

def create_manhattan_distance_plot(x1, y1, x2, y2):
    """Create a matplotlib plot showing Manhattan distance."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x1, y1, 'ro', label='Point 1')  # Red dot for first point
    ax.plot(x2, y2, 'bo', label='Point 2')  # Blue dot for second point
    
    # Draw Manhattan distance path
    ax.plot([x1, x2], [y1, y1], 'g--')  # Horizontal path
    ax.plot([x2, x2], [y1, y2], 'g--')  # Vertical path
    
    ax.set_title('Manhattan Distance Visualization')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)
    ax.legend()
    return fig

def create_distance_over_time_plot(velocity, time):
    """Create a matplotlib plot showing distance over time."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Distance vs Time plot
    t = np.linspace(0, time, 100)
    d = velocity * t
    
    ax.plot(t, d, 'b-', label='Distance')
    ax.set_title('Distance Traveled vs Time')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Distance (units)')
    ax.grid(True)
    ax.legend()
    
    # Annotate final distance
    distance = velocity * time
    ax.annotate(f'Final Distance: {distance} units', 
                xy=(time, distance), 
                xytext=(time/2, distance/2),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    return fig

def main():
    st.title('Distance Visualization')
    
    # Sidebar for navigation
    app_mode = st.sidebar.selectbox('Choose Visualization Mode', 
        ['Euclidean Distance', 'Manhattan Distance', 'Distance Over Time'])
    
    if app_mode == 'Euclidean Distance':
        st.header('Euclidean Distance Calculator')
        
        # Input for coordinates
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input('X1 Coordinate', value=0.0, key='x1_euc')
            y1 = st.number_input('Y1 Coordinate', value=0.0, key='y1_euc')
        
        with col2:
            x2 = st.number_input('X2 Coordinate', value=3.0, key='x2_euc')
            y2 = st.number_input('Y2 Coordinate', value=4.0, key='y2_euc')
        
        # Calculate distance
        distance = calculate_euclidean_distance(x1, y1, x2, y2)
        
        # Display results
        st.write(f'Euclidean Distance: {distance:.2f} units')
        
        # Create and display plot
        fig = create_distance_plot(x1, y1, x2, y2)
        st.pyplot(fig)
        plt.close(fig)
    
    elif app_mode == 'Manhattan Distance':
        st.header('Manhattan Distance Calculator')
        
        # Input for coordinates
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input('X1 Coordinate', value=0.0, key='x1_man')
            y1 = st.number_input('Y1 Coordinate', value=0.0, key='y1_man')
        
        with col2:
            x2 = st.number_input('X2 Coordinate', value=3.0, key='x2_man')
            y2 = st.number_input('Y2 Coordinate', value=4.0, key='y2_man')
        
        # Calculate Manhattan distance
        manhattan_distance = abs(x2 - x1) + abs(y2 - y1)
        
        # Display results
        st.write(f'Manhattan Distance: {manhattan_distance:.2f} units')
        
        # Create Manhattan distance visualization
        fig = create_manhattan_distance_plot(x1, y1, x2, y2)
        st.pyplot(fig)
        plt.close(fig)
    
    elif app_mode == 'Distance Over Time':
        st.header('Distance Traveled Over Time')
        
        # Velocity input
        velocity = st.slider('Velocity (units/second)', 1, 20, 5)
        
        # Time input
        time = st.slider('Time (seconds)', 1, 60, 10)
        
        # Calculate distance
        distance = velocity * time
        
        # Visualization
        fig = create_distance_over_time_plot(velocity, time)
        st.pyplot(fig)
        plt.close(fig)
        
        # Display numerical results
        st.write(f'Velocity: {velocity} units/second')
        st.write(f'Time: {time} seconds')
        st.write(f'Total Distance: {distance} units')

if __name__ == '__main__':
    main()