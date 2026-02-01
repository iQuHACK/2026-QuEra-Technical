"""Main entry point for quantum error detection experiments.

This module runs error detection experiments using the kernel builders
from kernel_builder.py.
"""

import argparse

from kirin import enable_stracetrace
from bloqade.pyqrack import StackMemorySimulator
from syndrome_evals import evaluate_syndromes, result_is_valid
from kernel_builder import x_error_detection, xz_error_detection, z_error_detection, n_sean_qubits
import json
import time

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def main(args) -> None:
    """Run quantum error detection experiments.
    
    This function sets up the quantum emulator and executes the error detection
    kernels, displaying the measurement results.
    
    :Example:
    
    >>> main()
    X error detection results:
    [...]
    """
    enable_stracetrace()
    # Run X error detection
    emulator = StackMemorySimulator(min_qubits=n_sean_qubits * 2)
    
    task = emulator.task(xz_error_detection)
    nb_result = 10
    valid = 0
    data = []
    for i in range(nb_result):
        results = task.run()
        logger.debug(f"Run {i+1}/{nb_result} results: {results}")
        if isinstance(results,tuple):
            logger.debug(f"X error detection results: {results[0]}")
            logger.debug(f"Z error detection results: {results[1]}")
            logger.debug("Validating x results...")
            x_is_valid = result_is_valid(results[0])
            logger.debug("Validating z results...")
            z_is_valid = result_is_valid(results[1])
            logger.debug(f"X results valid: {x_is_valid}")
            logger.debug(f"Z results valid: {z_is_valid}")
            if x_is_valid and z_is_valid:
                valid += 1
            # TODO add else to evaluate syndromes and infer which qubit is wrong

        else:
            if result_is_valid(results):
                                # part that log the data
                colors = evaluate_syndromes(results[0])
                data.append({
                    "check":"x_error",
                    "blue":colors[0],
                    "red":colors[1],
                    "green":colors[2],
                    "results": [int(result) for result in results[0]]
                })
                colors = evaluate_syndromes(results[1])
                data.append({
                    "check":"z_error",
                    "blue":colors[0],
                    "red":colors[1],
                    "green":colors[2],
                    "results": [int(result) for result in results[1]]
                })
                data.append({
                    "check":"logical",
                    "results": [int(result) for result in results[2]]
                })
                logger.debug(f"Error detection results: {results}")
                valid += 1
            colors = evaluate_syndromes(results)
            data.append({
                "blue":colors[0],
                "red":colors[1],
                "green":colors[2],
                "results": [int(result) for result in results]
            })
        
    with open(f"data{time.time()}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"valid : {valid}, invalid : {nb_result-valid}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Quantum error detection experiments using color codes"
    )
    
    args = parser.parse_args()
    
    main(args)
