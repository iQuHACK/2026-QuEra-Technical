from bloqade import squin

payload = {
    "a": (squin.depolarize, 0.5),
}

def poi(q, label):
    """
    Implements a 'point of interest' gate.

    Args
        qubit: qubit to add label to
        label: label for point of interest
        noise_channel: noise channel.
    """

    noise_channel, probability = payload.get(label)
    return noise_channel(p=probability, qubit=q)





    