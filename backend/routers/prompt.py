# v2.0 - Integrate code generation with file saving
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.code_generator import generate_code_project
from backend.services.file_writer import save_project_files

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def submit_prompt(data: PromptRequest):
    try:
        result = generate_code_project(data.prompt)
        path = save_project_files(result["project_id"], result["files"])
        return {
            "project_id": result["project_id"],
            "saved_to": path,
            "message": result["message"],
            "files": list(result["files"].keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
