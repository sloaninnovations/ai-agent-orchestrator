from fastapi import FastAPI
from datetime import datetime
from uuid import uuid4

app = FastAPI()

@app.get("/time")
def read_time():
    return {"time": datetime.now().isoformat()}

@app.get("/uuid")
def read_uuid():
    return {"uuid": str(uuid4())}