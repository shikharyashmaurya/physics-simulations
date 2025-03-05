import numpy as np

def simulate_projectile(initial_velocity, launch_angle, air_resistance):
    """
    Simulate projectile motion.
    
    Parameters:
    - initial_velocity: Initial speed (m/s)
    - launch_angle: Launch angle in degrees
    - air_resistance: Boolean to include air resistance (simplified here)
    
    Returns:
    - t: Time array
    - x: Horizontal position array
    - y: Vertical position array
    """
    g = 9.8  # Gravity (m/s²)
    theta = np.radians(launch_angle)
    vx = initial_velocity * np.cos(theta)
    vy = initial_velocity * np.sin(theta)
    
    # Time to reach peak (when vertical velocity becomes zero)
    t_peak = vy / g
    t_total = 2 * t_peak  # Total flight time (no air resistance)
    t = np.linspace(0, t_total, 1000)
    
    x = vx * t
    y = vy * t - 0.5 * g * t**2
    
    # If air resistance were included, you'd modify x and y with drag equations
    if air_resistance:
        st.warning("Air resistance not implemented in this simple example.")
    
    return t, x, y