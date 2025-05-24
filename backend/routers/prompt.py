# v4.0 - Track project status through each stage
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.code_generator import generate_code_project
from backend.services.file_writer import save_project_files
from backend.services.github_committer import commit_project_to_github
from backend.models.status_tracker import set_status

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def submit_prompt(data: PromptRequest):
    try:
        # Stage 1: Generate
        result = generate_code_project(data.prompt)
        project_id = result["project_id"]
        set_status(project_id, "generated", result["message"], {"files": list(result["files"].keys())})

        # Stage 2: Save to disk
        path = save_project_files(project_id, result["files"])
        set_status(project_id, "saved", "Files written to disk", {"path": path})

        # Stage 3: Push to GitHub
        github_result = commit_project_to_github(project_id, path)
        set_status(project_id, "committed", "Files committed to GitHub", github_result)

        return {
            "project_id": project_id,
            "message": result["message"],
            "files": list(result["files"].keys()),
            "saved_to": path,
            "github_commit": github_result
        }

    except Exception as e:
        set_status(project_id, "error", str(e))
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Path
from backend.models.status_tracker import get_status

@router.get("/status/{project_id}")
def check_status(project_id: str = Path(..., title="Project ID")):
    return get_status(project_id)
