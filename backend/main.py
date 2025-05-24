# v1.3 - Add CORS, Prompt, and Planner routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import prompt
from backend.routers import planner

app = FastAPI()

# Allow WordPress frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wordpress-1281112-5549543.cloudwaysapps.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the /prompt and /planner endpoints
app.include_router(prompt.router, prefix="/prompt", tags=["Prompt"])
app.include_router(planner.router, prefix="/planner", tags=["Planner"])

@app.get("/")
def root():
    return {"status": "ok"}
