# v1.1 - Uses code_generator to return mocked code files
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.code_generator import generate_code_project

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def submit_prompt(data: PromptRequest):
    try:
        result = generate_code_project(data.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
