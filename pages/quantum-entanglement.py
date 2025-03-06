import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

st.title("Quantum Entanglement Simulation")
st.write(
    """
    This simulation visualizes quantum entanglement for a pair of spin‑½ particles in a singlet state.
    Adjust the measurement angles for Particle A and Particle B to see how the correlation between outcomes changes.
    
    In a singlet state:
    - When both particles are measured along the same axis (θ = 0°), the outcomes are perfectly anti‑correlated.
    - When the measurement axes differ, the probability for Particle B to be the opposite of Particle A is given by:
    
    P(B = –A) = cos²(θ/2)
    
    and the probability for getting the same result is:
    
    P(B = A) = sin²(θ/2)
    """
)

# Input: measurement angles and number of trials
angle_A = st.slider("Measurement angle for Particle A (degrees)", 0, 360, 0)
angle_B = st.slider("Measurement angle for Particle B (degrees)", 0, 360, 0)
num_trials = st.number_input("Number of measurement trials", min_value=100, max_value=10000, value=1000, step=100)

def simulate_entanglement(angle_A, angle_B, num_trials):
    # Compute the effective angle difference (in radians) as the smallest difference
    diff_deg = abs(angle_A - angle_B)
    if diff_deg > 180:
        diff_deg = 360 - diff_deg
    theta = math.radians(diff_deg)
    
    # For a singlet state:
    # P(B = -A) = cos²(theta/2) (anti-correlated outcomes)
    # P(B = A)  = sin²(theta/2) (correlated outcomes)
    p_anti = math.cos(theta/2)**2
    p_same = math.sin(theta/2)**2

    outcomes = []
    for _ in range(num_trials):
        # Randomly assign outcome for Particle A
        A = np.random.choice([1, -1])
        # Decide outcome for Particle B based on the probabilities
        if np.random.rand() < p_anti:
            B = -A
        else:
            B = A
        outcomes.append((A, B))
    outcomes = np.array(outcomes)
    # The correlation is the average of the product A * B
    correlation = np.mean(outcomes[:, 0] * outcomes[:, 1])
    return outcomes, correlation, theta, p_anti, p_same

outcomes, sim_corr, theta, p_anti, p_same = simulate_entanglement(angle_A, angle_B, int(num_trials))

# Theoretical correlation for a singlet state is -cos(theta)
theo_corr = -math.cos(theta)

st.write("### Simulation Results")
st.write(f"Effective angle difference: {math.degrees(theta):.2f}°")
st.write(f"Probability of anti-correlated outcomes (B = -A): {p_anti:.3f}")
st.write(f"Probability of correlated outcomes (B = A): {p_same:.3f}")
st.write(f"Simulated correlation (average of A×B): {sim_corr:.3f}")
st.write(f"Theoretical correlation (-cos(theta)): {theo_corr:.3f}")

# Count outcome occurrences for visualization
unique, counts = np.unique(outcomes, axis=0, return_counts=True)
outcome_counts = {}
for outcome, count in zip(unique, counts):
    outcome_counts[tuple(outcome)] = count

st.write("#### Outcome Counts")
st.write(outcome_counts)

# Bar chart to display the distribution of outcomes
labels = ['(1, 1)', '(1, -1)', '(-1, 1)', '(-1, -1)']
values = [outcome_counts.get((1, 1), 0),
          outcome_counts.get((1, -1), 0),
          outcome_counts.get((-1, 1), 0),
          outcome_counts.get((-1, -1), 0)]
fig, ax = plt.subplots()
ax.bar(labels, values, color='skyblue')
ax.set_xlabel("Measurement outcomes (A, B)")
ax.set_ylabel("Counts")
ax.set_title("Outcome Distribution")
st.pyplot(fig)
