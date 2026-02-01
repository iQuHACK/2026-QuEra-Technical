"""Syndrome evaluation and post-selection for quantum color codes.

This module provides utilities for evaluating syndromes from measurement
results and performing post-selection on color code states to verify
error-free executions.
"""

from typing import Any

from bloqade.types import Qubit, MeasurementResult
from kirin.dialects.ilist import IList

import logging

logger = logging.getLogger(__name__)

FAULTY_QUBIT_MAP = {
    '000':-1,
    '100':0,
    '101':1,
    '111':2,
    '110':3,
    '011':4,
    '001':5,
    '010':6,
}

class SyndromeError(ValueError):
    """Custom exception raised when syndrome evaluation fails post-selection.
    
    This exception is raised when one or more plaquette syndromes indicate
    an error has occurred, meaning the state does not pass post-selection
    criteria for error-free execution.
    """
    pass


def extract_syndrome(group, log_expectation=False) -> int:
    """Compute the parity of measurement results in a plaquette group.
    
    This function calculates the syndrome for a plaquette by summing all
    measurement results in the group and returning the parity (mod 2).
    A return value of 0 indicates even parity (no error detected), while
    1 indicates odd parity (error detected).
    
    :param group: List of measurement results (0 or 1) for qubits in a plaquette
    :param log_expectation: If True, logs the -1/+1 mapping of 1/0 results
    :return: Parity of the group (0 for even, 1 for odd)
    :rtype: int
    
    :Example:
    
    >>> extract_syndrome([0, 1, 0, 1])
    0
    >>> extract_syndrome([1, 1, 1])
    1
    """
    if log_expectation:
        for i in group:
            logger.debug(f"Measurement result {i} mapped to expectation value {1 if i == 0 else -1}")
    t = 0
    for i in group:
        t = t + i
    return (t % 2)


def result_is_valid(results: IList[MeasurementResult, Any]) -> bool:
    """Check if measurement results pass post-selection criteria.
    
    This function evaluates the syndromes for blue, red, and green plaquettes
    of a 7-qubit color code. Returns True if all syndromes are zero (even parity),
    indicating an error-free measurement. Returns False if any syndrome is non-zero.
    
    :param results: Measurement results from all 7 qubits in the color code
    :type results: IList[MeasurementResult, Any]
    :return: True if all syndromes pass (all zeros), False otherwise
    :rtype: bool
    
    :Example:
    
    >>> results = IList([0, 0, 0, 0, 0, 0, 0])
    >>> is_valid = result_is_valid(results)
    >>> print(is_valid)
    True
    """
    blue = [results[0], results[1], results[2], results[3]]
    red = [results[2], results[3], results[4], results[6]]
    green = [results[1], results[2], results[4], results[5]]
    logical_observable = [results[0], results[1], results[5]]
    logger.debug(f"Measurement results - Blue: {blue}, Red: {red}, Green: {green}")
    logger.debug(f"Logical observable measurements: {logical_observable}")

    logger.debug("Evaluating blue syndrome...")
    resultat_blue = extract_syndrome(blue, log_expectation=False)
    logger.debug("Evaluating red syndrome...")
    resultat_red = extract_syndrome(red, log_expectation=False)
    logger.debug("Evaluating green syndrome...")
    resultat_green = extract_syndrome(green, log_expectation=False)
    logger.debug("Evaluating logical observable syndrome...")
    resultat_logical_observable = extract_syndrome(logical_observable, log_expectation=False)
    logger.debug(f"Syndromes - Blue: {resultat_blue}, Red: {resultat_red}, Green: {resultat_green}")
    logger.debug(f"Logical observable syndrome: {resultat_logical_observable}")
    is_valid = True
    if(resultat_blue == 1 or resultat_red == 1 or resultat_green == 1):
        is_valid = False
    return is_valid


def evaluate_syndromes(results: IList[MeasurementResult, Any]) -> tuple[int, int, int]:
    """Evaluate and return syndromes for all three color code plaquettes.

    This function evaluates the syndromes for blue, red, and green plaquettes
    of a 7-qubit color code. Each syndrome is computed as the parity of its
    respective plaquette measurements. A syndrome of 0 indicates even parity
    (no error detected), while 1 indicates odd parity (error detected).

    :param results: Measurement results from all 7 qubits in the color code
    :type results: IList[MeasurementResult, Any]
    :return: Tuple of (blue_syndrome, red_syndrome, green_syndrome)
    :rtype: tuple[int, int, int]

    :Example:

    >>> results = IList([0, 0, 0, 0, 0, 0, 0])
    >>> syndromes = evaluate_syndromes(results)
    >>> print(syndromes)
    (0, 0, 0)
    """
    blue = [results[0], results[1], results[2], results[3]]
    red = [results[2], results[3], results[4], results[6]]
    green = [results[1], results[2], results[4], results[5]]

    blue_plaquette_syndrome = extract_syndrome(blue)
    red_plaquette_syndrome = extract_syndrome(red)
    green_plaquette_syndrome = extract_syndrome(green)

    return (blue_plaquette_syndrome, red_plaquette_syndrome, green_plaquette_syndrome)

def evaluate_faulty_qubit(syndrome_brg) -> int:
    syndrome_str = "".join(syndrome_brg)
    return FAULTY_QUBIT_MAP[syndrome_str]