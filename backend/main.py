# v1.2 - Add CORS for WordPress domain + prompt router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import prompt

app = FastAPI()

# Allow WordPress frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wordpress-1281112-5549543.cloudwaysapps.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the /prompt endpoint
app.include_router(prompt.router, prefix="/prompt", tags=["Prompt"])

@app.get("/")
def root():
    return {"status": "ok"}
