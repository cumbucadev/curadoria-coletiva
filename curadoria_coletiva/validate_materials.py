import os
import yaml
from pydantic import ValidationError
from typing import Set, List, Dict, Any
from material import Material


def validate_and_collect_materials(directory_path: str) -> List[Dict[str, Any]]:
    """Reads all YAML files in a directory, validates each material,
    and collects them into a list, ensuring there are no duplicate titles."""

    unique_titles: Set[str] = set()
    all_materials: List[Dict[str, Any]] = []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".yml", ".yaml")):
            file_path = os.path.join(directory_path, filename)
            materials_data = _load_yaml_file(file_path)

            for material_data in materials_data:
                try:
                    _validate_material(material_data, unique_titles)
                    all_materials.append(material_data)
                    print(f"Valid material found in: {filename}")
                except ValidationError as e:
                    print(f"Validation error in file {filename}: {e}")
                except ValueError as e:
                    print(f"Value error in file {filename}: {e}")

    return all_materials


def _load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """Reads a YAML file and returns its data."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []  # Return an empty list if file is empty
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {file_path}: {e}")
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


def save_all_materials_to_yaml(
    materials: List[Dict[str, Any]], output_file: str
) -> None:
    """Saves the collected materials to a YAML file with UTF-8 encoding."""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("# auto-generated file, please don't change it\n\n")
        yaml.dump(materials, file, default_flow_style=False, allow_unicode=True)

    print(f"All materials saved to {output_file}")


if __name__ == "__main__":
    directory = "materials"
    all_materials = validate_and_collect_materials(directory)
    save_all_materials_to_yaml(all_materials, "all_materials.yml")
