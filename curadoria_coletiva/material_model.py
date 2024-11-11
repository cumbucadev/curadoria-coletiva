from pydantic import BaseModel, conset, conint
from curadoria_coletiva.enums import (
    FormatEnum,
    LanguageEnum,
    LearningStyleEnum,
    PaceEnum,
    SubjectEnum,
    DifficultyEnum,
)


class Comment(BaseModel):
    """
    Represents a comment made by a user, including their GitHub username
    and the text of their comment.

    Attributes:
        usuario (str): The GitHub username of the user making the comment.
        texto (str): The text content of the comment provided by the user.
    """

    usuario: str
    texto: str


class Material(BaseModel):
    """
    Represents an educational material with various attributes to guide mentors in curating
    resources for mentees.

    Attributes:
        titulo (str): The title of the material.
        autoria (Optional[str]): The author, creator, or organization responsible for the material.
        url (Optional[str]): A URL link to the source of the material, if available.
        assuntos (set of SubjectEnum): A set of subjects covered in the material.
        formato (FormatEnum): The format of the material, such as video, blog post, or book.
        minutos_necessarios (int): Estimated time in minutes required to cover the material.
        prerequisitos (set of SubjectEnum): A set of prerequisite subjects required to understand
        the material.
        ritmo (PaceEnum): The pace of the material, e.g., fast, medium, or slow.
        estilo_aprendizagem (LearningStyleEnum): The preferred learning style catered to, such as
        visual, auditory, or kinesthetic.
        idioma (LanguageEnum): The language in which the material is presented.
        nivel_dificuldade (Optional[DifficultyEnum]): The difficulty level of the material, if specified.
        eh_gratuito (bool): Indicates whether the material is free to access.
        recomendado_por (set of str): A set of GitHub usernames of people that recommend the
        material,
        comments (list of Comment): A list of comments from users with their GitHub usernames.
    """

    titulo: str
    autoria: str
    url: str
    assuntos: conset(SubjectEnum, min_length=1)
    formato: FormatEnum
    minutos_necessarios: conint(gt=0)
    prerequisitos: conset(SubjectEnum) = set()
    ritmo: PaceEnum
    estilo_aprendizagem: LearningStyleEnum
    idioma: LanguageEnum
    nivel_dificuldade: DifficultyEnum
    eh_gratuito: bool
    recomendado_por: conset(str, min_length=1)
    comentarios: list[Comment] = []

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Introdução ao Python",
                "autoria": "Jane Doe",
                "url": "https://example.com/python-course",
                "assuntos": {SubjectEnum.PYTHON, SubjectEnum.PROGRAMMING_BASICS},
                "formato": FormatEnum.VIDEO,
                "minutos_necessarios": 90,
                "prerequisitos": {SubjectEnum.BASIC_MATH},
                "ritmo": PaceEnum.MEDIUM,
                "estilo_aprendizagem": LearningStyleEnum.VISUAL,
                "idioma": LanguageEnum.EN,
                "nivel_dificuldade": DifficultyEnum.BEGINNER,
                "eh_gratuito": True,
                "eu_recomendo": {"camilamaia"},
                "comments": [
                    {
                        "usuario": "camilamaia",
                        "texto": "Adoro o capítulo 5! Ele explica conceitos complexos de forma clara e acessível.",
                    },
                    {
                        "usuario": "joaodasilva",
                        "texto": "Material excelente para iniciantes, muito didático.",
                    },
                ],
            }
        }
