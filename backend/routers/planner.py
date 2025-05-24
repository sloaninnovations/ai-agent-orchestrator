from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from uuid import uuid4
import httpx
import asyncio
import json
import logging

from backend.services.planning_agent import plan_project
from backend.models.status_tracker import set_status, get_status

router = APIRouter()
logger = logging.getLogger(__name__)

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
        logger.error(f"Error in initiate_project: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate project.")

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
        logger.error(f"HTTPException in execute_project: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in execute_project: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

async def run_milestones(project_id: str, milestones: list):
    async with httpx.AsyncClient() as client:
        for i, milestone in enumerate(milestones):
            try:
                set_status(project_id, "building", f"Milestone {i+1}: {milestone}")
                res = await client.post(
                    "https://ai-agent-orchestrator.onrender.com/prompt",
                    json={"prompt": milestone}
                )
                res.raise_for_status()
                await asyncio.sleep(10)  # pacing
            except Exception as e:
                set_status(project_id, "error", f"Failed at milestone {i+1}", {"error": str(e)})
                logger.error(f"Error in run_milestones at milestone {i+1}: {e}")
                return

    set_status(project_id, "complete", "All milestones generated")
