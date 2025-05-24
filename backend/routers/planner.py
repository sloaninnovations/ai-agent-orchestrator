# v1.1 - Planner routes: /initiate and /execute for autonomous builds
from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from uuid import uuid4
import httpx
import asyncio
import json

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
    body = await req.json()
    project_id = body["project_id"]
    plan_info = get_status(project_id)

    if not plan_info["data"] or "plan" not in plan_info["data"]:
        raise HTTPException(status_code=404, detail="Plan not found")

    try:
        print("Raw plan_info:", plan_info)
        plan = json.loads(plan_info["data"]["plan"])
        milestones = plan.get("Milestones", [])

        bg.add_task(run_milestones, project_id, milestones)
        set_status(project_id, "executing", "Milestone build started")
        return {"project_id": project_id, "status": "started", "milestones": milestones}

    except Exception as e:
        import traceback
        print("Error during plan execution:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

async def run_milestones(project_id: str, milestones: list):
    async with httpx.AsyncClient() as client:
        for i, milestone in enumerate(milestones):
            try:
                set_status(project_id, "building", f"Milestone {i+1}: {milestone}")
                res = await client.post(
                    "https://ai-agent-orchestrator.onrender.com/prompt",
                    json={"prompt": milestone}
                )
                _ = res.json()  # could add validation
                await asyncio.sleep(10)  # pacing
            except Exception as e:
                set_status(project_id, "error", f"Failed at milestone {i+1}", {"error": str(e)})
                return

    set_status(project_id, "complete", "All milestones generated")
