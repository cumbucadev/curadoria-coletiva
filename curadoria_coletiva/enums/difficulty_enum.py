from enum import Enum


class DifficultyEnum(str, Enum):
    """
    Enum representing levels of difficulty for learning materials.

    Attributes:
    - BEGINNER: Suitable for individuals with no prior knowledge of the topic.
    - INTERMEDIATE: Best for learners who have basic familiarity with the subject.
    - ADVANCED: Targeted at those with solid foundational knowledge, ready for more complex concepts.
    - EXPERT: Designed for learners with deep expertise, looking for highly specialized content.
    """

    BEGINNER = "iniciante"
    INTERMEDIATE = "intermediário"
    ADVANCED = "avançado"
    EXPERT = "expert"

    def __str__(self):
        return self.value
