from enum import Enum


class PaceEnum(str, Enum):
    """
    Enum representing the pace of educational materials.

    - FAST: Fast-paced learning.
    - MEDIUM: Medium-paced learning.
    - SLOW: Slow-paced learning.
    """

    FAST = "rápido"
    MEDIUM = "médio"
    SLOW = "lento"

    def __str__(self):
        return self.value
