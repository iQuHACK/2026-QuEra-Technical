from bloqade import squin
from typing import Dict, Tuple, Optional, Callable

POI_CONFIG: Dict[str, Tuple[str, float]] = {}

def configure_poi(config: Dict[str, Tuple[str, float]]):
    global POI_CONFIG
    POI_CONFIG = config.copy()
    # poi_kernels = dict()
    # for x in POI_CONFIG.keys():
    #     poi_kernels[x] = get_poi_kernel(x)
    # return poi_kernels
    

def get_poi_kernel(label: str):
    
    config = POI_CONFIG.get(label, ("none", 0.0))
    noise_type, prob = config
    
    if noise_type == "depolarize":
        @squin.kernel
        def _poi(q):
            squin.depolarize(prob, q)
        return _poi
    elif noise_type == "qubit_loss":
        @squin.kernel
        def _poi(q):
            squin.qubit_loss(prob, q)
        return _poi
    else:
        @squin.kernel
        def _poi(q):
            squin.u3(0, 0, 0, q)
        return _poi