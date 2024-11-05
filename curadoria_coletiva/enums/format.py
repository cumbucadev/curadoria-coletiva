from enum import Enum


class FormatEnum(str, Enum):
    """
    Enum representing the possible formats for educational materials.

    - VIDEO: Material in video format.
    - BLOG: Blog post, typically in article format.
    - BOOK: Material in book or e-book format.
    - ARTICLE: An article, often part of a journal or magazine.
    - ONLINE_COURSE: A structured course available online, often with modules and assessments.
    - PODCAST: Audio material that discusses topics in a conversational format.
    - TUTORIAL: A guide that provides step-by-step instructions for a specific task.
    - DOCUMENT: A general document, which may include reports, whitepapers, or similar resources.
    """

    VIDEO = "vídeo"
    BLOG = "blog post"
    BOOK = "livro"
    ARTICLE = "artigo"
    ONLINE_COURSE = "curso online"
    PODCAST = "podcast"
    TUTORIAL = "tutorial"
    DOCUMENT = "documento"

    def __str__(self):
        return self.value
