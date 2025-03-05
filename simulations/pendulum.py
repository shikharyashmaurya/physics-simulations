import numpy as np

def simulate_pendulum(length, gravity, initial_angle, time_span):
    """
    Simulate a simple pendulum.
    
    Parameters:
    - length: Length of the pendulum (m)
    - gravity: Gravitational acceleration (m/s²)
    - initial_angle: Initial angle in radians
    - time_span: Duration of simulation (s)
    
    Returns:
    - t: Time array
    - angle: Angle array over time
    """
    t = np.linspace(0, time_span, 1000)
    omega = np.sqrt(gravity / length)  # Angular frequency
    angle = initial_angle * np.cos(omega * t)  # Simple harmonic motion
    return t, angle