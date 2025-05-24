# v3.0 - Add GitHub commit step
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.code_generator import generate_code_project
from backend.services.file_writer import save_project_files
from backend.services.github_committer import commit_project_to_github

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def submit_prompt(data: PromptRequest):
    try:
        result = generate_code_project(data.prompt)
        path = save_project_files(result["project_id"], result["files"])
        github_result = commit_project_to_github(result["project_id"], path)

        return {
            "project_id": result["project_id"],
            "message": result["message"],
            "files": list(result["files"].keys()),
            "saved_to": path,
            "github_commit": github_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
