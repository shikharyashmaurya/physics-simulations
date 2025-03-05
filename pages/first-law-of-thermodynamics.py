import streamlit as st
import matplotlib.pyplot as plt

def main():
    st.title("First Law of Thermodynamics Simulation")
    st.write("""
    The First Law of Thermodynamics is essentially an expression of energy conservation. 
    It states that the change in internal energy (ΔU) of a system equals the heat (Q) added 
    to the system minus the work (W) done by the system:
    
    **ΔU = Q - W**
    
    Use the sliders below to adjust the heat added and the work done.
    """)

    # User input for heat (Q) and work (W)
    Q = st.slider("Heat added (Q) [Joules]", min_value=-200, max_value=200, value=50, step=1)
    W = st.slider("Work done (W) [Joules]", min_value=-200, max_value=200, value=30, step=1)

    # Calculate the change in internal energy
    delta_U = Q - W
    st.write(f"**Calculated change in internal energy (ΔU):** {delta_U} Joules")

    # Create a bar chart to visualize the energy contributions
    labels = ['Heat (Q)', 'Work (W)', 'ΔU']
    values = [Q, W, delta_U]
    colors = ['#69b3a2', '#404080', '#e377c2']

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=colors)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_ylabel("Energy (Joules)")
    ax.set_title("Energy Balance: Q, W, and ΔU")
    for bar in bars:
        yval = bar.get_height()
        # Position the text slightly above the bar if positive, or below if negative.
        offset = 3 if yval >= 0 else -15
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + offset, f'{yval}', 
                ha='center', color='black', fontsize=10)
    st.pyplot(fig)

    st.write("""
    **Explanation:**  
    - **Q (Heat added):** The energy put into the system via heating.  
    - **W (Work done):** The energy used by the system to perform work (like expanding against a piston).  
    - **ΔU:** The resulting change in the system's internal energy.  
    
    Notice that increasing Q or decreasing W (or both) will result in a higher ΔU, showing that more energy remains stored within the system.
    """)

if __name__ == '__main__':
    main()
