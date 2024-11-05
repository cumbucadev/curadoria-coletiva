from enum import Enum


class LanguageEnum(str, Enum):
    """
    Enum representing the available languages for educational materials.

    - EN: English language.
    - PT_BR: Brazilian Portuguese language.
    """

    EN = "english"
    PT_BR = "português (BR)"

    def __str__(self):
        return self.value
