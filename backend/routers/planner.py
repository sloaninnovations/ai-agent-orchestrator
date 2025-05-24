# v1.0 - Initiate project planning from a user goal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from backend.services.planning_agent import plan_project
from backend.models.status_tracker import status_by_id

router = APIRouter()

class PlanningRequest(BaseModel):
    goal: str

@router.post("/planner/initiate")
def initiate_project(req: PlanningRequest):
    project_id = str(uuid4())
    try:
        plan = plan_project(req.goal, project_id)
        status_by_id[project_id] = {
            "stage": "planning",
            "message": "Plan generated",
            "plan": plan
        }
        return {
            "project_id": project_id,
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
