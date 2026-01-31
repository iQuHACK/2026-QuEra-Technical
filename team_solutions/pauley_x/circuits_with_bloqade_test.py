from typing import Any

import numpy as np
import bloqade.types
from kirin.ir import Method
from bloqade.types import Qubit, MeasurementResult

# Some types we will use, useful for type hints
from kirin.dialects.ilist import IList

from bloqade import squin

Register = IList[Qubit, Any]

