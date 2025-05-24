# v1.0 - Create ZIP archive from project directory
import os
import zipfile

BASE_DIR = "projects"

def create_zip_for_project(project_id: str) -> str:
    project_path = os.path.join(BASE_DIR, project_id)
    if not os.path.exists(project_path):
        raise FileNotFoundError("Project folder not found")

    zip_path = os.path.join(BASE_DIR, f"{project_id}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, project_path)
                zipf.write(full_path, arcname)

    return zip_path
