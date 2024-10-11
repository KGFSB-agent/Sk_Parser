import os
import csv
from pathlib import Path


def write_csv(technologies, csv_path):
    """
    Writes a dictionary with data about each news to a CSV file.

    Args:
        technologies (dict): A dictionary with data about each technology.
        csv_path (str): The file path for the CSV file.

    Returns:
        None
    """
    output_dir = Path(os.path.dirname(csv_path))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check if file already exists to avoid rewriting headers
    file_exists = os.path.exists(csv_path)

    headers = {
        "main_sector": "Главная отрасль",
        "title": "Название технологии",
        "sectors": "Сопутствующие отрасли",
        "readiness_lvl": "Уровень готовности технологии",
        "description": "Описание технологии",
        "advantages_of_the_technology": "Преимущества технологии",
        "references": "Референсы",
        "technology_url": "Ссылка"
    }

    with open(csv_path, "a", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers.keys())

        # Write headers only if the file is newly created
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(technologies)
