"""Kernel builders for quantum error detection using color codes.

This module provides kernel functions for building various error detection
circuits based on 7-qubit color codes with transversal gate operations.
"""

from typing import Any
from kirin import enable_stracetrace

from bloqade.types import Qubit, MeasurementResult
from kirin.dialects.ilist import IList
from bloqade import squin
from syndrome_evals import FAULTY_QUBIT_MAP

from syndrome_evals import evaluate_syndromes, evaluate_faulty_qubit

import logging

logger = logging.getLogger(__name__)


n_sean_qubits = 7

enable_stracetrace()

@squin.kernel
def color_code_factory(qubits: IList[Qubit, Any]) -> IList[Qubit, Any]:
    """Prepare a 7-qubit color code state using controlled-Z and sqrt(Y) gates.
    
    This function implements the encoding circuit for a 7-qubit color code,
    applying a sequence of CZ gates and sqrt(Y) rotations to prepare the
    logical state from physical qubits.
    
    :param qubits: List of 7 qubits to encode into the color code
    :type qubits: IList[Qubit, Any]
    :return: The encoded qubits in color code state
    :rtype: IList[Qubit, Any]
    
    :Example:
    
    >>> qubits = squin.qalloc(7)
    >>> encoded_qubits = color_code_factory(qubits)
    """  
    squin.broadcast.sqrt_y_adj(qubits[0:-1])

    squin.cz(qubits[1], qubits[2])
    squin.cz(qubits[3], qubits[4])
    squin.cz(qubits[5], qubits[6])
    squin.sqrt_y(qubits[6])
    
    squin.cz(qubits[0], qubits[3])
    squin.cz(qubits[2], qubits[5])
    squin.cz(qubits[4], qubits[6])
    squin.broadcast.sqrt_y(qubits[2:])

    squin.cz(qubits[0], qubits[1])
    squin.cz(qubits[2], qubits[3])
    squin.cz(qubits[4], qubits[5])

    squin.broadcast.sqrt_y(IList([qubits[1], qubits[2], qubits[4]]))

    return qubits


@squin.kernel
def x_error_detection() -> IList[MeasurementResult, Any]:
    """Execute transversal controlled-X gate for X-error detection.
    
    This kernel implements a fault-tolerant transversal CX gate between two
    7-qubit color code blocks for detecting X errors. The first block encodes
    an arbitrary state (X|+⟩), while the second encodes the |+⟩ state. After
    applying transversal CX gates between corresponding qubits, Z-basis
    measurements are performed on the second block.
    
    :return: Measurement results from the second color code block in Z basis
    :rtype: IList[MeasurementResult, Any]
    
    :Example:
    
    >>> from bloqade.pyqrack import StackMemorySimulator
    >>> emulator = StackMemorySimulator(min_qubits=14)
    >>> task = emulator.task(x_error_detection)
    >>> results = task.run()
    >>> print(results)
    """
    qubits_1 = squin.qalloc(n_sean_qubits)
    # put arbitrary state
    squin.x(qubits_1[-1])
    squin.h(qubits_1[-1])
    qubits_1 = color_code_factory(qubits_1)

    # put state + on ancillary registers
    qubits_2 = squin.qalloc(n_sean_qubits)
    squin.h(qubits_2[-1])
    qubits_2 = color_code_factory(qubits_2)

    # transversal CX
    for index in range(len(qubits_1)):
        squin.cx(qubits_1[index], qubits_2[index])
    
    bits = squin.broadcast.measure(qubits_2)
    return bits


@squin.kernel
def z_error_detection() -> IList[MeasurementResult, Any]:
    """Execute transversal controlled-X gate for Z-error detection.
    
    This kernel implements a fault-tolerant transversal CX gate between two
    7-qubit color code blocks for detecting Z errors. The first block encodes
    an arbitrary state (X|+⟩), while the second encodes the |+⟩ state. After
    applying transversal CX gates between corresponding qubits, X-basis
    measurements (via Hadamard then Z-basis measurement) are performed on the
    second block.
    
    :return: Measurement results from the second color code block in X basis
    :rtype: IList[MeasurementResult, Any]
    
    :Example:
    
    >>> from bloqade.pyqrack import StackMemorySimulator
    >>> emulator = StackMemorySimulator(min_qubits=14)
    >>> task = emulator.task(z_error_detection)
    >>> results = task.run()
    >>> print(results)
    """
    qubits_1 = squin.qalloc(n_sean_qubits)
    # put arbitrary state
    squin.x(qubits_1[-1])
    squin.h(qubits_1[-1])
    qubits_1 = color_code_factory(qubits_1)

    # put state + on ancillary registers
    qubits_2 = squin.qalloc(n_sean_qubits)
    qubits_2 = color_code_factory(qubits_2)

    # transversal CX
    for index in range(len(qubits_1)):
        squin.cx(qubits_2[index], qubits_1[index])
    
    # Apply Hadamard gates for X-basis measurement
    squin.broadcast.h(qubits_2)
    
    bits = squin.broadcast.measure(qubits_2)
    return bits


@squin.kernel
def xz_error_detection() -> tuple[IList[MeasurementResult, Any], IList[MeasurementResult, Any], IList[MeasurementResult, Any]]:
    """Execute combined X and Z error detection protocol.
    
    This kernel implements a comprehensive error detection protocol that
    combines both X and Z error detection mechanisms. It performs transversal
    operations on multiple color code blocks to detect and identify both
    types of errors in the encoded quantum state.
    
    :return: Combined measurement results for X and Z error detection
    :rtype: tuple[IList[MeasurementResult, Any], IList[MeasurementResult, Any], IList[MeasurementResult, Any]]
    
    :Example:
    
    >>> from bloqade.pyqrack import StackMemorySimulator
    >>> emulator = StackMemorySimulator(min_qubits=21)
    >>> task = emulator.task(xz_error_detection)
    >>> results = task.run()
    >>> print(results)
    """

    qubits_1 = squin.qalloc(n_sean_qubits)
    squin.depolarize(1.0, qubits_1[0])

    # put arbitrary state
    squin.x(qubits_1[-1])
    squin.h(qubits_1[-1])
    qubits_1 = color_code_factory(qubits_1)

    # put state + on ancillary registers
    qubits_2 = squin.qalloc(n_sean_qubits)
    squin.h(qubits_2[-1])
    qubits_2 = color_code_factory(qubits_2)

    # transversal CX
    for index in range(len(qubits_1)):
        squin.cx(qubits_1[index], qubits_2[index])
    
    bits_x = squin.broadcast.measure(qubits_2)

    for index in range(len(qubits_2)):
        squin.reset(qubits_2[index])

    qubits_2 = color_code_factory(qubits_2)

    squin.z(qubits_2[0])

    # transversal CX
    for index in range(len(qubits_1)):
        squin.cx(qubits_2[index], qubits_1[index])

    # Apply Hadamard gates for X-basis measurement
    squin.broadcast.h(qubits_2)

    bits_z = squin.broadcast.measure(qubits_2)

    
    blue = bits_x[0] ^ bits_x[1] ^ bits_x[2] ^ bits_x[3]
    red = bits_x[2] ^ bits_x[3] ^ bits_x[4] ^ bits_x[6]
    green = bits_x[1] ^ bits_x[2] ^ bits_x[4] ^ bits_x[5]

    if blue == 1 and red == 0 and green == 0:
        squin.x(qubits_1[0])
    elif blue == 1 and red == 0 and green == 1:
        squin.x(qubits_1[1])
    elif blue == 1 and red == 1 and green == 1:
        squin.x(qubits_1[2])
    elif blue == 1 and red == 1 and green == 0:
        squin.x(qubits_1[3])
    elif blue == 0 and red == 1 and green == 1:
        squin.x(qubits_1[4])
    elif blue == 0 and red == 0 and green == 1:
        squin.x(qubits_1[5])
    elif blue == 0 and red == 1 and green == 0:
        squin.x(qubits_1[6])
    
    blue = bits_z[0] ^ bits_z[1] ^ bits_z[2] ^ bits_z[3]
    red = bits_z[2] ^ bits_z[3] ^ bits_z[4] ^ bits_z[6]
    green = bits_z[1] ^ bits_z[2] ^ bits_z[4] ^ bits_z[5]

    if blue == 1 and red == 0 and green == 0:
        squin.z(qubits_1[0])
    elif blue == 1 and red == 0 and green == 1:
        squin.z(qubits_1[1])
    elif blue == 1 and red == 1 and green == 1:
        squin.z(qubits_1[2])
    elif blue == 1 and red == 1 and green == 0:
        squin.z(qubits_1[3])
    elif blue == 0 and red == 1 and green == 1:
        squin.z(qubits_1[4])
    elif blue == 0 and red == 0 and green == 1:
        squin.z(qubits_1[5])
    elif blue == 0 and red == 1 and green == 0:
        squin.z(qubits_1[6])



    bits_psi = squin.broadcast.measure(IList([qubits_1[0], qubits_1[1], qubits_1[5]]))

    return (bits_x, bits_z, bits_psi, blue, red, green)