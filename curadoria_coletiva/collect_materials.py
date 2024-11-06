import os
import yaml
from typing import List, Dict, Any


def collect_materials(directory_path: str, output_file: str) -> None:
    """Reads all YAML files in a directory, validates each material,
    and collects them into a list, ensuring there are no duplicate titles.
    Adds 'directory/filename' to each material for reference."""

    all_materials: List[Dict[str, Any]] = []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".yml", ".yaml")):
            file_path = os.path.join(directory_path, filename)
            materials_data = _load_yaml_file(file_path)

            for material_data in materials_data:
                material_data['file_path'] = f"{os.path.basename(directory_path)}/{filename}"

                all_materials.append(material_data)


    _save_all_materials_to_yaml(all_materials, output_file)


def _load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """Reads a YAML file and returns its data."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []  # Return an empty list if file is empty
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {file_path}: {e}")
        return []


def _save_all_materials_to_yaml(
    materials: List[Dict[str, Any]], output_file: str
) -> None:
    """Saves the collected materials to a YAML file with UTF-8 encoding."""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("# auto-generated file, please don't change it\n\n")

        yaml.dump(materials, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"All materials saved to {output_file}")
