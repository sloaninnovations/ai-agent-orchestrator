# v1.0 - Save generated files to disk
import os

BASE_DIR = "projects"

def save_project_files(project_id: str, files: dict) -> str:
    project_path = os.path.join(BASE_DIR, project_id)
    os.makedirs(project_path, exist_ok=True)

    for filename, content in files.items():
        file_path = os.path.join(project_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())

    return project_path
