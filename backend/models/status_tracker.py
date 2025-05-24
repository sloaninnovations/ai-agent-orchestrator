# v1.0 - Simple in-memory project status tracker
from typing import Dict

# {project_id: {stage, message, files, github_result}}
_project_status: Dict[str, dict] = {}

def set_status(project_id: str, stage: str, message: str = "", data: dict = None):
    _project_status[project_id] = {
        "stage": stage,
        "message": message,
        "data": data or {}
    }

def get_status(project_id: str) -> dict:
    return _project_status.get(project_id, {
        "stage": "unknown",
        "message": "Project not found"
    })
