from bloqade import squin
from typing import Tuple, Callable, Any, Optional


NOISE_CHANNELS = {
    "depolarize": (squin.depolarize, 0.5),
    "amplitude_damping": (squin.qubit_loss, 0.5),
    # can add more
}

### Example payload
poi_noises_payload = {
    "a": (squin.depolarize, 0.5),
    "interesting_area": (squin.qubit_loss, 0.5)
}

def poi(q, label, custom_probability: Optional[float] = None):
    """
    Implements a 'point of interest' gate.

    Args
        qubit: qubit to add label to
        label: label for point of interest
        noise_channel: noise channel.
    """

    noise_channel, default_prob = poi_noises_payload.get(label, (None, None))
    probability = custom_probability if custom_probability is not None else default_prob
    if noise_channel is not None:
        return noise_channel(p=probability, qubit=q)




    