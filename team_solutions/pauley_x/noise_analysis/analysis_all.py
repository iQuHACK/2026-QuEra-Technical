from main import MSD_encoding_Z, MSD_encoding_X
from team_solutions.pauley_x.noise_analysis.noise_injection import test_individual_noise_type, compare_all_noise_types
import matplotlib.pyplot as plt
import numpy as np

# Config
SHOTS = 500
CIRCUIT = MSD_encoding_Z(0, 0)  # Change to MSD_encoding_X(0, 0) if needed

# Test 1 comparing all noise types
print("=" * 60)
print("Testing impact of all noise types...")
print("=" * 60)
results = compare_all_noise_types(CIRCUIT, shots=SHOTS)

print("\n" + "=" * 60)
print("RANKING BY ERROR RATE (Most impactful first):")
print("=" * 60)
for i, (noise_type, error_rate) in enumerate(results.items(), 1):
    print(f"{i:2d}. {noise_type:30s} -> {error_rate*100:6.2f}% error rate")

# Test 2 most likely issues
print("\n" + "=" * 60)
print("Detailed analysis of top 5 noise sources...")
print("=" * 60)

top_5_noises = list(results.keys())[:5]
detailed_results = []

for noise_type in top_5_noises:
    result = test_individual_noise_type(CIRCUIT, noise_type, shots=SHOTS)
    detailed_results.append(result)
    
    print(f"\n{noise_type}:")
    print(f"  Error rate: {result['error_rate']*100:.2f}%")
    
    # Count unique erroneous states
    clean_histogram = result['clean_histogram']
    noisy_histogram = result['noisy_histogram']
    
    error_states = {state: count for state, count in noisy_histogram.items() 
                   if state not in clean_histogram}
    print(f"  Number of erroneous states: {len(error_states)}")
    if error_states:
        print(f"  Most common erroneous state: {max(error_states.items(), key=lambda x: x[1])}")

# visualizing the top three noise sources
print("\n" + "=" * 60)
print("Creating visualization...")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
top_3_noises = list(results.keys())[:3]

for idx, (ax, result) in enumerate(zip(axes, detailed_results[:3])):
    clean_histogram = result['clean_histogram']
    noisy_histogram = result['noisy_histogram']
    
    # Prepare data for plotting
    states = sorted(set(list(clean_histogram.keys()) + list(noisy_histogram.keys())))
    clean_counts = [clean_histogram.get(state, 0) for state in states]
    noisy_counts = [noisy_histogram.get(state, 0) for state in states]
    
    x = np.arange(len(states))
    width = 0.35
    
    ax.bar(x - width/2, clean_counts, width, label='Clean', alpha=0.8)
    ax.bar(x + width/2, noisy_counts, width, label='Noisy', alpha=0.8)
    
    ax.set_title(f"{result['noise_type']}\n({result['error_rate']*100:.2f}% error)")
    ax.set_xlabel("Measurement State")
    ax.set_ylabel("Count")
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # will rotate the x-axis labels if too many states
    if len(states) > 10:
        ax.set_xticklabels([f"{s:07b}" for s in states], rotation=45, fontsize=8)
    else:
        ax.set_xticklabels([f"{s:07b}" for s in states], fontsize=9)

# quera if you read this you are awesome sauce

plt.tight_layout()
plt.savefig("noise_type_comparison.png", dpi=150, bbox_inches="tight")
print("visuals saved at noise_type_comparison.png")
plt.show()