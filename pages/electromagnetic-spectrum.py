import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Constants
SPEED_OF_LIGHT = 3e8  # m/s

# Configure app
st.set_page_config(page_title="EM Spectrum Visualizer", layout="wide")
st.title("Electromagnetic Spectrum Visualization")
st.markdown("Explore different regions of the electromagnetic spectrum")

# Sidebar controls
with st.sidebar:
    st.header("Configuration")
    wavelength = st.slider("Wavelength (meters)", 
                         1e-12, 100.0, 
                         value=5e-7, 
                         format="%.1e")
    
    region = st.selectbox("Predefined Regions", [
        "Radio Waves", "Microwaves", "Infrared",
        "Visible Light", "Ultraviolet", "X-Rays", "Gamma Rays"
    ])

# Calculate frequency
frequency = SPEED_OF_LIGHT / wavelength

# Main display
tab1, tab2 = st.tabs(["Wave Visualization", "Spectrum Diagram"])

with tab1:
    # Create wave visualization
    x = np.linspace(0, 4*np.pi, 1000)
    y_electric = np.sin(x * wavelength * 100)  # Scaled for visualization
    y_magnetic = np.cos(x * wavelength * 100)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y_electric, label='Electric Field (E)')
    ax.plot(x, y_magnetic, label='Magnetic Field (B)')
    ax.set_title(f"EM Wave Visualization\nλ = {wavelength:.2e} m | ν = {frequency:.2e} Hz")
    ax.set_xlabel("Propagation Direction")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    # Create spectrum diagram
    spectrum_data = {
        "Region": ["Gamma", "X-Ray", "UV", "Visible", "IR", "Microwave", "Radio"],
        "Start (m)": [1e-12, 1e-10, 4e-7, 4e-7, 7e-7, 1e-3, 1e-1],
        "End (m)": [1e-10, 1e-8, 4e-7, 7e-7, 1e-3, 1e-1, 1e4],
        "Color": ["purple", "blue", "violet", "#FF00FF", "red", "orange", "yellow"]
    }
    
    fig = px.bar(spectrum_data, 
                 x=["Gamma", "X-Ray", "UV", "Visible", "IR", "Microwave", "Radio"],
                 y=[1,1,1,1,1,1,1],
                 color="Region",
                 color_discrete_map={r: c for r,c in zip(spectrum_data["Region"], 
                                                         spectrum_data["Color"])},
                 orientation="h",
                 log_x=True,
                 height=400)
    
    fig.update_layout(title="Electromagnetic Spectrum Regions",
                     xaxis_title="Wavelength (meters)",
                     yaxis_visible=False,
                     showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Region information
region_info = {
    "Radio Waves": {"range": "1 mm - 100 km", "uses": "Communications, broadcasting"},
    "Microwaves": {"range": "1 mm - 1 m", "uses": "Radar, cooking"},
    "Infrared": {"range": "700 nm - 1 mm", "uses": "Thermal imaging"},
    "Visible Light": {"range": "400-700 nm", "uses": "Human vision, photography"},
    "Ultraviolet": {"range": "10-400 nm", "uses": "Sterilization, astronomy"},
    "X-Rays": {"range": "0.01-10 nm", "uses": "Medical imaging"},
    "Gamma Rays": {"range": "<0.01 nm", "uses": "Cancer treatment"}
}

st.subheader(f"Region Information: {region}")
col1, col2 = st.columns(2)
with col1:
    st.metric("Wavelength Range", region_info[region]["range"])
with col2:
    st.metric("Common Applications", region_info[region]["uses"])
