from enum import Enum


class SubjectEnum(str, Enum):
    """
    Enum representing different subjects covered in educational materials.
    """

    BASIC_MATH = "matemática básica"
    CLOUD_COMPUTING = "computação em nuvem"
    CSS = "css"
    DATA_SCIENCE = "ciência de dados"
    DATABASES = "bancos de dados"
    DEVOPS = "devops"
    HTML = "html"
    JAVASCRIPT = "javascript"
    MACHINE_LEARNING = "aprendizado de máquina"
    MOBILE_DEVELOPMENT = "desenvolvimento mobile"
    PROGRAMMING_BASICS = "programação básica"
    PYTHON = "python"
    SOFTWARE_ENGINEERING = "engenharia de software"
    WEB_DEVELOPMENT = "desenvolvimento web"

    def __str__(self):
        return self.value
