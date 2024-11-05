from enum import Enum


class LearningStyleEnum(str, Enum):
    """
    Enum representing different learning styles to categorize materials by how they are best understood.

    Attributes:
    - VISUAL: Best suited for visual learners who prefer diagrams, videos, and visual content.
    - AUDITORY: Suitable for auditory learners who prefer listening, such as through lectures and podcasts.
    - KINESTHETIC: Ideal for kinesthetic learners who benefit from hands-on practice and physical engagement.
    """

    VISUAL = "visual"
    AUDITORY = "auditivo"
    KINESTHETIC = "cinestésico"

    def __str__(self):
        return self.value
