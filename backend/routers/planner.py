# File: backend/routers/planner.py

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
import json
import logging

from backend.services.planning_agent import plan_project
from backend.models.status_tracker import set_status, get_status

router = APIRouter()

class PlanningRequest(BaseModel):
    goal: str

@router.post("/initiate")
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

@router.post("/execute")
async def execute_project(req: Request, bg: BackgroundTasks):
    try:
        body = await req.json()
        project_id = body.get("project_id")
        if not project_id:
            raise HTTPException(status_code=400, detail="Missing 'project_id' in request body.")

        plan_info = get_status(project_id)
        if not plan_info or "data" not in plan_info or "plan" not in plan_info["data"]:
            raise HTTPException(status_code=404, detail="Plan not found for the given project_id.")

        plan = json.loads(plan_info["data"]["plan"])
        milestones = plan.get("Milestones", [])
        if not milestones:
            raise HTTPException(status_code=400, detail="No milestones found in the plan.")

        bg.add_task(run_milestones, project_id, milestones)
        set_status(project_id, "executing", "Milestone build started")
        return {"project_id": project_id, "status": "started", "milestones": milestones}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

async def run_milestones(project_id: str, milestones: list):
    # Implement your milestone execution logic here
    pass
