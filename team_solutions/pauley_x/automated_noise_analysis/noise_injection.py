import cirq
from bloqade import cirq_utils
from bloqade.cirq_utils.noise import GeminiOneZoneNoiseModel, GeminiTwoZoneNoiseModel
from bloqade.cirq_utils.noise.transform import transform_circuit
import numpy as np
from typing import Dict, Tuple, Callable


def _cirq_gemini_one_zone_noise(circuit: cirq.Circuit, scaling_factor: float = 1.0):
    "Exports Squin code to Cirq and returns a noisy circuit using GeminiOneZoneNoiseModel"
    noise_model = GeminiOneZoneNoiseModel(scaling_factor=scaling_factor)
    noisy_circuit = circuit.with_noise(noise_model)
    return noisy_circuit


def _cirq_gemini_two_zone_noise(circuit: cirq.Circuit, scaling_factor: float = 1.0):
    "Exports Squin code to Cirq and returns a noisy circuit using GeminiTwoZoneNoiseModel"
    noise_model = GeminiTwoZoneNoiseModel(scaling_factor=scaling_factor)
    noisy_circuit = circuit.with_noise(noise_model)
    return noisy_circuit


def _isolated_noise_model(
    noise_type: str, scaling_factor: float = 1.0, model_class=GeminiOneZoneNoiseModel
):
    """
    Creates a noise model with only a specific noise type enabled
    """

    noise_param_map = {
        "local_px": "local_px",
        "local_py": "local_py",
        "local_pz": "local_pz",
        "local_loss": "local_loss_prob",
        "global_px": "global_px",
        "global_py": "global_py",
        "global_pz": "global_pz",
        "global_loss": "global_loss_prob",
        "cz_paired_px": "cz_paired_gate_px",
        "cz_paired_py": "cz_paired_gate_py",
        "cz_paired_pz": "cz_paired_gate_pz",
        "cz_paired_loss": "cz_gate_loss_prob",
        "cz_unpaired_px": "cz_unpaired_gate_px",
        "cz_unpaired_py": "cz_unpaired_gate_py",
        "cz_unpaired_pz": "cz_unpaired_gate_pz",
        "cz_unpaired_loss": "cz_unpaired_loss_prob",
        "mover_px": "mover_px",
        "mover_py": "mover_py",
        "mover_pz": "mover_pz",
        "mover_loss": "move_loss_prob",
        "sitter_px": "sitter_px",
        "sitter_py": "sitter_py",
        "sitter_pz": "sitter_pz",
        "sitter_loss": "sit_loss_prob",
        "local_unaddressed_px": "local_unaddressed_px",
        "local_unaddressed_py": "local_unaddressed_py",
        "local_unaddressed_pz": "local_unaddressed_pz",
        "local_unaddressed_loss": "local_unaddressed_loss_prob",
    }

    if noise_type not in noise_param_map:
        raise ValueError(
            f"Unknown noise type. The availabe types are {list(noise_param_map.keys())}"
        )

    # Initialize all noise to zero
    kwargs = {
        "scaling_factor": scaling_factor,
        "local_px": 0.0,
        "local_py": 0.0,
        "local_pz": 0.0,
        "local_loss_prob": 0.0,
        "global_px": 0.0,
        "global_py": 0.0,
        "global_pz": 0.0,
        "global_loss_prob": 0.0,
        "cz_paired_gate_px": 0.0,
        "cz_paired_gate_py": 0.0,
        "cz_paired_gate_pz": 0.0,
        "cz_gate_loss_prob": 0.0,
        "cz_unpaired_gate_px": 0.0,
        "cz_unpaired_gate_py": 0.0,
        "cz_unpaired_gate_pz": 0.0,
        "cz_unpaired_loss_prob": 0.0,
        "mover_px": 0.0,
        "mover_py": 0.0,
        "mover_pz": 0.0,
        "move_loss_prob": 0.0,
        "sitter_px": 0.0,
        "sitter_py": 0.0,
        "sitter_pz": 0.0,
        "sit_loss_prob": 0.0,
        "local_unaddressed_px": 0.0,
        "local_unaddressed_py": 0.0,
        "local_unaddressed_pz": 0.0,
        "local_unaddressed_loss_prob": 0.0,
    }

    default_model = model_class()
    param_name = noise_param_map[noise_type]
    kwargs[param_name] = getattr(default_model, param_name) * scaling_factor

    return model_class(**kwargs)


def analyze_noise_channels(ker, noise_source, noise_model=_cirq_gemini_two_zone_noise):
    """Tests importance of different noise channels"""

    ### Uses a Cirq backend
    if noise_source == "cirq_heuristic_model":

        # MSD_enc = MSD_encoding_X(np.pi, 0)
        # stim_circ = bloqade.stim.Circuit(MSD_enc)
        # sampler = stim_circ.compile_sampler()
        # samples = sampler.sample(shots=100)
        # result = 1 - 2 * samples.astype(int)
        # import numpy as np

        # print(f"ExpVal:{np.mean(np.array([i[0]*i[1]*i[5] for i in result]))}")
        clean_circuit = cirq_utils.emit_circuit(ker)
        noisy_circuit = transform_circuit(clean_circuit, noise_model)
        simulator = cirq.Simulator()
        clean_result = simulator.run(clean_circuit, repetitions=100)
        clean_measurement_key = list(clean_result.measurements.keys())[0]
        noisy_result = simulator.run(noisy_circuit, repetitions=100)
        noisy_measurement_key = list(noisy_result.measurements.keys())[0]

        return tuple(
            [
                clean_result.histogram(key=clean_measurement_key),
                noisy_result.histogram(key=noisy_measurement_key),
            ]
        )

    ### Uses a QuEra tsim backend
    if noise_source == "custom":
        clean_circuit = ker
        sampler = clean_circuit.compile_sampler()
        samples = sampler.sample(shots=100)
        return samples

    raise ValueError("Unknown parameters")


def test_individual_noise_type(
    ker,
    noise_type: str,
    shots: int = 100,
    model_class=GeminiOneZoneNoiseModel,
    scaling_factor: float = 1.0,
) -> Dict[str, object]:
    """
    Test the impact of a single noise type on the circuit.
    """
    clean_circuit = cirq_utils.emit_circuit(ker)

    # Create isolated noise model
    noise_model = _isolated_noise_model(noise_type, scaling_factor, model_class)
    noisy_circuit = transform_circuit(clean_circuit, noise_model)

    # Run simulations
    simulator = cirq.Simulator()
    clean_result = simulator.run(clean_circuit, repetitions=shots)
    noisy_result = simulator.run(noisy_circuit, repetitions=shots)

    clean_measurement_key = list(clean_result.measurements.keys())[0]
    noisy_measurement_key = list(noisy_result.measurements.keys())[0]

    clean_histogram = clean_result.histogram(key=clean_measurement_key)
    noisy_histogram = noisy_result.histogram(key=noisy_measurement_key)

    # Calculate error rate by fraction of states not in clean distribution
    error_count = sum(
        count
        for state, count in noisy_histogram.items()
        if state not in clean_histogram
    )
    error_rate = error_count / shots

    return {
        "clean_histogram": clean_histogram,
        "noisy_histogram": noisy_histogram,
        "noise_type": noise_type,
        "error_rate": error_rate,
    }


def compare_all_noise_types(
    ker,
    shots: int = 100,
    model_class=GeminiOneZoneNoiseModel,
    scaling_factor: float = 1.0,
) -> Dict[str, float]:
    """
    Test all noise types and return a ranking of their impact.

    Args:
        ker: Kernel/circuit to test
        shots: Number of measurement shots per test
        model_class: Noise model class to use
        scaling_factor: Scaling factor for noise rates

    Returns:
        Dictionary mapping noise types to their error rates, sorted by impact (descending)
    """
    noise_types = [
        "local_px",
        "local_py",
        "local_pz",
        "local_loss",
        "local_unaddressed_px",
        "local_unaddressed_py",
        "local_unaddressed_pz",
        "local_unaddressed_loss",
        "global_px",
        "global_py",
        "global_pz",
        "global_loss",
        "cz_paired_px",
        "cz_paired_py",
        "cz_paired_pz",
        "cz_paired_loss",
        "cz_unpaired_px",
        "cz_unpaired_py",
        "cz_unpaired_pz",
        "cz_unpaired_loss",
        "mover_px",
        "mover_py",
        "mover_pz",
        "mover_loss",
        "sitter_px",
        "sitter_py",
        "sitter_pz",
        "sitter_loss",
    ]

    results = {}
    for noise_type in noise_types:
        try:
            result = test_individual_noise_type(
                ker, noise_type, shots, model_class, scaling_factor
            )
            results[noise_type] = result["error_rate"]
            print(f"✓ {noise_type}: {result['error_rate']*100:.2f}% error rate")
        except Exception as e:
            print(f"✗ {noise_type}: Failed - {e}")

    # Sort by error rate (descending)
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    return sorted_results


# ker = None # Replace with Pranav's stuff
# print(analyze_noise_channels(ker, _cirq_gemini_two_zone_noise))
