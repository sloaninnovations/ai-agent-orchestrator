from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
import json
import httpx
import asyncio

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
        plan_str = json.dumps(plan) if isinstance(plan, dict) else plan
        set_status(project_id, "planning", "Plan generated", {"plan": plan_str})
        return {"project_id": project_id, "plan": plan}
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
        plan_raw = plan_info.get("data", {}).get("plan")

        if not plan_raw:
            raise HTTPException(status_code=404, detail="Plan not found for the given project_id.")

        try:
            plan = json.loads(plan_raw)
        except Exception:
            plan = plan_raw  # fallback if already a dict

        milestones = (
			plan.get("Milestones") or
			plan.get("4. Milestones") or
			[]
		)
        if not milestones:
            raise HTTPException(status_code=400, detail="No milestones found in the plan.")

        bg.add_task(run_milestones, project_id, milestones)
        set_status(project_id, "executing", "Milestone build started")
        return {"project_id": project_id, "status": "started", "milestones": milestones}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_milestones(project_id: str, milestones: list):
    async with httpx.AsyncClient() as client:
        for i, milestone in enumerate(milestones):
            try:
                set_status(project_id, "building", f"Milestone {i+1}: {milestone}")
                await client.post(
                    "https://ai-agent-orchestrator.onrender.com/prompt",
                    json={"prompt": milestone}
                )
                await asyncio.sleep(10)
            except Exception as e:
                set_status(project_id, "error", f"Failed at milestone {i+1}", {"error": str(e)})
                return
        set_status(project_id, "complete", "All milestones built")
