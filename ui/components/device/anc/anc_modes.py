from enum import IntEnum


class AncMode(IntEnum):
    """
    Values correspond to the protocol bit flags used by the backend.
    """
    OFF = 1
    TRANSPARENCY = 2
    ADAPTIVE = 4
    NOISE_CANCELLATION = 16
