"""Generate a color-code circuit diagram and write it to an SVG file.

This module builds a 7-qubit color-code circuit using the project's
`color_code_factory` and the `bloqade` framework, renders it as an SVG
diagram, and writes the result to disk.

The project guidelines require Sphinx-style docstrings and type hints
for public functions; this module follows those conventions.

Example
-------
Run from the repository root::

    python -m src.circuit_diagram_generator

"""

from typing import Optional
import logging

from bloqade import squin
from bloqade.tsim import Circuit

from kernel_builder import color_code_factory, xz_error_detection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@squin.kernel
def main() -> None:
    """Squin kernel that allocates 7 qubits and applies the color code.

    This function is decorated with ``squin.kernel`` and is intended to be
    passed to :class:`bloqade.tsim.Circuit` to produce a visual diagram of
    the circuit.

    Returns
    -------
    None
        This kernel performs in-place operations on allocated qubits.
    """
    # q = squin.qalloc(7)
    xz_error_detection()


def generate_colorcode_circuit(input_circuit = main, output_path: str = "colorcode_circuit.svg", height: int = 500) -> None:
    """Render the circuit defined by :func:`main` and write it to ``output_path``.

    Parameters
    ----------
    output_path : str
        Filesystem path where the SVG will be written. Defaults to
        ``colorcode_circuit.svg`` in the current working directory.
    height : int
        Height in pixels to pass to ``circuit.diagram`` when rendering.

    Raises
    ------
    OSError
        If writing the output file fails.
    """
    circuit = Circuit(input_circuit)
    colorcode_circuit = str(circuit.diagram(height=height))

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(colorcode_circuit)
        logger.info("Wrote color code circuit diagram to %s", output_path)
    except OSError as exc:
        logger.error("Failed to write circuit diagram to %s: %s", output_path, exc)
        raise


if __name__ == "__main__":
    generate_colorcode_circuit(output_path="xz_circuit.svg")