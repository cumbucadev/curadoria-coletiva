import sys
import yaml
from pydantic import ValidationError
from typing import Set, List, Dict, Any
from curadoria_coletiva.material_model import Material
from curadoria_coletiva.collect_materials import collect_materials


def validate_materials_from_yaml(yaml_file: str) -> List[Dict[str, Any]]:
    """Reads materials from a YAML file, validates each material, and returns them as a list."""

    unique_titles: Set[str] = set()
    validated_materials: List[Dict[str, Any]] = []

    materials_data = _load_yaml_file(yaml_file)

    for material_data in materials_data:
        try:
            _validate_material(material_data, unique_titles)
            validated_materials.append(material_data)
            print(f"Valid material found: {material_data.get('titulo')}")
        except ValidationError as e:
            print(f"Validation error in material {material_data.get('titulo')}: {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"Value error in material {material_data.get('titulo')}: {e}")
            sys.exit(1)

    return validated_materials


def _load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """Reads a YAML file and returns its data."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []  # Return an empty list if file is empty
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")
        return []


def _validate_material(material_data: Dict[str, Any], unique_titles: Set[str]) -> None:
    """Validates the material data and checks for duplicate titles.

    This method checks if the title of the material is unique and validates
    the material data against the Pydantic model. It raises a ValueError if
    a duplicate title is found, and a ValidationError if the material data is
    invalid.

    Args:
        material_data (Dict[str, Any]): The data for the material to validate.
        unique_titles (Set[str]): A set of titles that have already been validated.

    Raises:
        ValueError: If the title is duplicated.
        ValidationError: If the material data does not conform to the Pydantic model.
    """
    title = material_data.get("titulo").lower()

    if title in unique_titles:
        raise ValueError(f"Duplicated title found: {title}")

    unique_titles.add(title)

    try:
        Material.validate(material_data)
    except ValidationError as e:
        raise e  # Re-raise the ValidationError for the caller to handle


if __name__ == "__main__":
    input_yaml_file = "curadoria_coletiva/all_materials.yml"
    collect_materials("curadoria_coletiva/materials", input_yaml_file)
    validate_materials_from_yaml(input_yaml_file)
