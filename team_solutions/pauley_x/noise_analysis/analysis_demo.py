from main import MSD_encoding_Z
from team_solutions.pauley_x.noise_analysis.noise_injection import test_individual_noise_type
import sys

def demo():
    print("\n" + "="*70)
    print("="*70)
    
    circuit = MSD_encoding_Z(0, 0)
    
    # Test the most likely culprits
    key_noises = [
        'cz_paired_pz',        # CZ gates are just usually noisy
        'local_pz',            # Single-qubit rotations
        'cz_paired_px',        # X-type errors on CZ
        'local_px',            # X-type errors on singles
        'cz_unpaired_pz',      # Spectator qubits during CZ
    ]
    
    print(f"\nCircuit: MSD_encoding_Z(0, 0)")
    print(f"Testing {len(key_noises)} key noise sources (500 shots each)...\n")
    
    results = []
    max_error = 0
    
    for noise_type in key_noises:
        try:
            result = test_individual_noise_type(circuit, noise_type, shots=500)
            error_pct = result['error_rate'] * 100
            results.append((noise_type, error_pct))
            max_error = max(max_error, error_pct)
            print(f"✓ {noise_type:20s} -> {error_pct:6.2f}% error rate")
        except Exception as e:
            print(f"✗ {noise_type:20s} -> Failed: {e}")
    
    # Sort by impact
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "-"*70)
    print("RANKING (Most impactful first):")
    print("-"*70)
    for i, (noise_type, error_pct) in enumerate(results, 1):
        bar_length = int(error_pct / max_error * 40) if max_error > 0 else 0
        bar = "█" * bar_length
        print(f"{i}. {noise_type:20s} {error_pct:6.2f}% │{bar:40s}│")
    
    print("\n" + "="*70)
    print("RECOMMENDATION:")
    print("="*70)
    if results[0][1] > 20:
        print(f"(╯°o°)ᕗ  CRITICAL: '{results[0][0]}' causes {results[0][1]:.1f}% errors!")
        print(f"   This is your top priority for error correction/mitigation.")
    elif results[0][1] > 5:
        print(f"(ಠ╭╮ಠ)  SIGNIFICANT: '{results[0][0]}' causes {results[0][1]:.1f}% errors.")
        print(f"   Consider focusing error correction efforts here.")
    else:
        print(f"✓ All tested noise sources have <5% impact. Circuit is relatively robust!")
    
    print("\nFor full analysis of ALL noise types, run: python noise_analysis.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
