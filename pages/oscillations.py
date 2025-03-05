import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
    st.title("Oscillations Simulation")
    st.write("Visualize a simple harmonic oscillator using interactive parameters.")

    # Define interactive controls for oscillator parameters.
    amplitude = st.slider("Amplitude", 0.1, 10.0, 1.0, step=0.1)
    frequency = st.slider("Frequency (Hz)", 0.1, 5.0, 1.0, step=0.1)
    phase = st.slider("Phase (radians)", 0.0, 2*np.pi, 0.0, step=0.1)
    duration = st.slider("Simulation Duration (seconds)", 1, 20, 10)
    dt = 0.1  # Time step for the animation

    start = st.button("Start Simulation")
    if start:
        # Use an empty placeholder that will be updated for the animation.
        placeholder = st.empty()
        t_vals_full = np.linspace(0, duration, 500)  # Time points for the full curve
        
        # Animation loop: update the plot for each time step.
        for t in np.arange(0, duration, dt):
            # Calculate current displacement using simple harmonic motion equation.
            x_current = amplitude * np.cos(2 * np.pi * frequency * t + phase)
            
            # Compute full oscillation for plotting
            x_vals_full = amplitude * np.cos(2 * np.pi * frequency * t_vals_full + phase)
            
            # Create the plot
            fig, ax = plt.subplots()
            ax.plot(t_vals_full, x_vals_full, label="Oscillation")
            # Mark the current position with a red dot
            ax.scatter([t], [x_current], color="red", s=100, zorder=5, label="Current Position")
            
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Displacement")
            ax.set_title("Simple Harmonic Motion")
            ax.legend()
            ax.set_xlim(0, duration)
            # Adjust y-axis limits based on amplitude
            ax.set_ylim(-amplitude - 1, amplitude + 1)
            
            # Update the placeholder with the new plot
            placeholder.pyplot(fig)
            time.sleep(dt)

if __name__ == "__main__":
    main()
