# v1.0 - Initiate project planning from a user goal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from backend.services.planning_agent import plan_project
from backend.models.status_tracker import set_status

router = APIRouter()

class PlanningRequest(BaseModel):
    goal: str

@router.post("/planner/initiate")
def initiate_project(req: PlanningRequest):
    project_id = str(uuid4())
    try:
        plan = plan_project(req.goal, project_id)
		set_status(project_id, "planning", "Plan generated", {"plan": plan})

        return {
            "project_id": project_id,
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
