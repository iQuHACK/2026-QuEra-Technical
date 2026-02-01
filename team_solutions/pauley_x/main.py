from bloqade import squin, stim
from kirin.dialects.ilist import IList
from team_solutions.pauley_x.noise_analysis.noise_injection import analyze_noise_channels
import numpy as np
import matplotlib.pyplot as plt


def MSD_encoding_Z(theta, phi, basis="z"):

    @squin.kernel
    def parameterized_MSD_encoding():
        q = squin.qalloc(7)  # allocate qubits
        squin.u3(theta, phi, 0, q[6])
        for i in range(6):
            squin.sqrt_y_adj(q[i])
        # [squin.broadcast.sqrt_y_adj(q[i]) for i in range(5)]
        squin.cz(q[1], q[2])
        squin.cz(q[3], q[4])
        squin.cz(q[5], q[6])
        squin.sqrt_y(q[6])
        squin.cz(q[0], q[3])
        squin.cz(q[2], q[5])
        squin.cz(q[4], q[6])
        for i in range(5):
            squin.sqrt_y(q[i + 2])
        # [squin.broadcast.sqrt_y(q[i+2]) for i in range(5)]
        squin.cz(q[0], q[1])
        squin.cz(q[2], q[3])
        squin.cz(q[4], q[5])
        squin.sqrt_y(q[1])
        squin.sqrt_y(q[2])
        squin.sqrt_y(q[4])
        squin.broadcast.measure(q)

    return parameterized_MSD_encoding


def MSD_encoding_X(theta, phi, basis="z"):

    @squin.kernel
    def parameterized_MSD_encoding():
        q = squin.qalloc(7)  # allocate qubits
        squin.u3(theta, phi, 0, q[6])
        for i in range(6):
            squin.sqrt_y_adj(q[i])
        # [squin.broadcast.sqrt_y_adj(q[i]) for i in range(5)]
        squin.cz(q[1], q[2])
        squin.cz(q[3], q[4])
        squin.cz(q[5], q[6])
        squin.sqrt_y(q[6])
        squin.cz(q[0], q[3])
        squin.cz(q[2], q[5])
        squin.cz(q[4], q[6])
        for i in range(5):
            squin.sqrt_y(q[i + 2])
        # [squin.broadcast.sqrt_y(q[i+2]) for i in range(5)]
        squin.cz(q[0], q[1])
        squin.cz(q[2], q[3])
        squin.cz(q[4], q[5])
        squin.sqrt_y(q[1])
        squin.sqrt_y(q[2])
        squin.sqrt_y(q[4])
        squin.broadcast.h(q)
        squin.broadcast.measure(q)

    return parameterized_MSD_encoding


ker = MSD_encoding_Z(0, 0)

def bitstring(i):
    return f"{bin(i)[2:]:0>{7}}"

SHOTS = 100

clean_histogram, noisy_histogram = analyze_noise_channels(ker, "cirq_heuristic_model")

# Convert histogram to lists for plotting

states = []
counts = []
colors = []
invalid_results = 0

for state, count in sorted(noisy_histogram.items()):
    # Convert tuple of measurement results to binary string
    state_str = bitstring(state)
    states.append(state_str)
    counts.append(100*count / SHOTS)
    if state in clean_histogram.keys():
        color = 'green'
    else:
        color = 'red'
        invalid_results += count
    colors.append(color)

# [x for x in counts.keys()]
# import numpy as np
# print(f"ExpVal:{np.mean(np.array([i[0]*i[1]*i[5] for i in result]))}")

# Create bar plot
plt.figure(figsize=(12, 6))
plt.bar(range(len(states)), counts, color=colors)
plt.xlabel("Measurement State")
plt.ylabel("Measurement Percent")
plt.title("Noisy Circuit")
plt.xticks(range(len(states)), states, rotation=90, fontsize=8)
plt.text(0.02, 0.98, f"Errors: {100*invalid_results / SHOTS}%", 
         transform=plt.gca().transAxes, 
         fontsize=12, 
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig("measurement_histogram.png", dpi=150, bbox_inches="tight")
y_range = np.arange(0, int(max(counts)) + 2, 1)
plt.yticks(y_range)
plt.grid(axis='y', linestyle='-', alpha=0.5)
plt.show()


print(f"Total measurements: {sum(counts)}")
print(f"Number of unique states: {len(states)}")
