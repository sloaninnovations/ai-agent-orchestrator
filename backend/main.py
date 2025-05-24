# v1.1 - Registering prompt router
from fastapi import FastAPI
from backend.routers import prompt


app = FastAPI()

# Register the /prompt endpoint
app.include_router(prompt.router, prefix="/prompt", tags=["Prompt"])

@app.get("/")
def root():
    return {"status": "ok"}
