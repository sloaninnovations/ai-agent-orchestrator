from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import prompt, planner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wordpress-1281112-5549543.cloudwaysapps.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router, prefix="/prompt", tags=["Prompt"])
app.include_router(planner.router, prefix="/planner", tags=["Planner"])

@app.get("/")
def root():
    return {"status": "ok"}
